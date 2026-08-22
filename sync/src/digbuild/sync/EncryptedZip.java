package digbuild.sync;

import java.io.Closeable;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.channels.SeekableByteChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.zip.CRC32;
import java.util.zip.DataFormatException;
import java.util.zip.Inflater;

/**
 * Reads the pack zip -- which java.util.zip cannot, because it is encrypted.
 *
 * The pack has always been published as one ZipCrypto archive (7z
 * -mem=ZipCrypto in the workflow) and the password has always been printed on
 * the wiki's install page. Reading that same file is what lets this mod exist
 * without changing anything about how the pack is published.
 *
 * ZipCrypto is PKWARE's original stream cipher: three keys seeded from the
 * password, each plaintext byte folding back into them. Weak, and irrelevantly
 * so -- the password is public and the point is packaging, not secrecy.
 *
 * The central directory is walked by hand rather than through ZipFile because
 * every entry's data is encrypted; only the directory itself is plain.
 */
final class EncryptedZip implements Closeable {

    record Entry(String name, long crc, long size, long compressedSize,
                 int method, long localHeaderOffset, boolean encrypted) {}

    private static final int EOCD_SIG = 0x06054b50;
    private static final int CENTRAL_SIG = 0x02014b50;
    private static final int LOCAL_SIG = 0x04034b50;

    private final SeekableByteChannel channel;
    private final List<Entry> entries;

    private EncryptedZip(SeekableByteChannel channel, List<Entry> entries) {
        this.channel = channel;
        this.entries = entries;
    }

    List<Entry> entries() {
        return entries;
    }

    @Override
    public void close() throws IOException {
        channel.close();
    }

    static EncryptedZip open(Path file) throws IOException {
        SeekableByteChannel ch = Files.newByteChannel(file);
        try {
            return new EncryptedZip(ch, readCentralDirectory(ch));
        } catch (IOException | RuntimeException e) {
            ch.close();
            throw e;
        }
    }

    private static ByteBuffer read(SeekableByteChannel ch, long position, int length)
            throws IOException {
        ByteBuffer buf = ByteBuffer.allocate(length).order(ByteOrder.LITTLE_ENDIAN);
        ch.position(position);
        while (buf.hasRemaining()) {
            if (ch.read(buf) < 0) throw new IOException("unexpected end of zip");
        }
        return buf.flip();
    }

    private static List<Entry> readCentralDirectory(SeekableByteChannel ch) throws IOException {
        // The end-of-central-directory record is last, but a zip comment may
        // follow it, so it is found by scanning backwards over the tail.
        long size = ch.size();
        int tailLength = (int) Math.min(size, 66_000);
        ByteBuffer tail = read(ch, size - tailLength, tailLength);

        int eocd = -1;
        for (int i = tailLength - 22; i >= 0; i--) {
            if (tail.getInt(i) == EOCD_SIG) {
                eocd = i;
                break;
            }
        }
        if (eocd < 0) throw new IOException("not a zip file: no end-of-central-directory record");

        int count = tail.getShort(eocd + 10) & 0xffff;
        long directorySize = tail.getInt(eocd + 12) & 0xffffffffL;
        long directoryOffset = tail.getInt(eocd + 16) & 0xffffffffL;

        ByteBuffer dir = read(ch, directoryOffset, (int) directorySize);
        List<Entry> out = new ArrayList<>(count);

        for (int i = 0; i < count; i++) {
            if (dir.getInt() != CENTRAL_SIG) throw new IOException("corrupt central directory");
            dir.position(dir.position() + 4);           // versions
            int flags = dir.getShort() & 0xffff;
            int method = dir.getShort() & 0xffff;
            dir.position(dir.position() + 4);           // mod time and date
            long crc = dir.getInt() & 0xffffffffL;
            long compressed = dir.getInt() & 0xffffffffL;
            long uncompressed = dir.getInt() & 0xffffffffL;
            int nameLength = dir.getShort() & 0xffff;
            int extraLength = dir.getShort() & 0xffff;
            int commentLength = dir.getShort() & 0xffff;
            dir.position(dir.position() + 8);           // disk number, attributes
            long localOffset = dir.getInt() & 0xffffffffL;

            byte[] name = new byte[nameLength];
            dir.get(name);
            dir.position(dir.position() + extraLength + commentLength);

            out.add(new Entry(new String(name, StandardCharsets.UTF_8), crc, uncompressed,
                    compressed, method, localOffset, (flags & 1) != 0));
        }
        return out;
    }

    /** The entry's bytes: decrypted if it needs it, inflated if it needs that. */
    byte[] contents(Entry entry, String password) throws IOException {
        ByteBuffer header = read(channel, entry.localHeaderOffset(), 30);
        if (header.getInt(0) != LOCAL_SIG) throw new IOException("corrupt entry " + entry.name());
        int nameLength = header.getShort(26) & 0xffff;
        int extraLength = header.getShort(28) & 0xffff;

        long dataOffset = entry.localHeaderOffset() + 30 + nameLength + extraLength;
        if (entry.compressedSize() > Integer.MAX_VALUE) {
            throw new IOException(entry.name() + " is too large to read in one piece");
        }
        byte[] data = read(channel, dataOffset, (int) entry.compressedSize()).array();

        if (entry.encrypted()) data = decrypt(data, password, entry);

        byte[] out = switch (entry.method()) {
            case 0 -> data;                     // stored
            case 8 -> inflate(data, entry);     // deflate, which -mx=1 produces
            default -> throw new IOException(
                    "unsupported compression method " + entry.method() + " in " + entry.name());
        };

        CRC32 crc = new CRC32();
        crc.update(out);
        if (crc.getValue() != entry.crc()) {
            throw new IOException(entry.name() + " failed its checksum");
        }
        return out;
    }

    private static byte[] inflate(byte[] data, Entry entry) throws IOException {
        // nowrap: a zip entry carries a raw deflate stream with no zlib header.
        Inflater inflater = new Inflater(true);
        try {
            inflater.setInput(data);
            byte[] out = new byte[(int) entry.size()];
            int written = 0;
            while (written < out.length) {
                int n = inflater.inflate(out, written, out.length - written);
                if (n == 0) throw new IOException("truncated deflate stream in " + entry.name());
                written += n;
            }
            return out;
        } catch (DataFormatException e) {
            // Overwhelmingly the wrong password: ZipCrypto's check byte is one
            // byte wide, so one wrong password in 256 gets past it and fails
            // here instead.
            throw new IOException("could not decompress " + entry.name()
                    + " -- is the password right?", e);
        } finally {
            inflater.end();
        }
    }

    /**
     * PKWARE traditional encryption.
     *
     * Twelve bytes of header come first; the last of them is a one-byte check
     * against the entry's CRC, which is how a wrong password is caught here
     * rather than as unexplained corruption later.
     */
    private static byte[] decrypt(byte[] data, String password, Entry entry) throws IOException {
        if (password == null || password.isEmpty()) {
            throw new IOException(entry.name() + " is encrypted and no password is configured");
        }
        if (data.length < 12) throw new IOException("truncated entry " + entry.name());

        int[] keys = {0x12345678, 0x23456789, 0x34567890};
        for (byte b : password.getBytes(StandardCharsets.UTF_8)) updateKeys(keys, b);

        byte[] out = new byte[data.length - 12];
        for (int i = 0; i < data.length; i++) {
            byte plain = (byte) (data[i] ^ streamByte(keys));
            updateKeys(keys, plain);
            if (i == 11 && (plain & 0xff) != ((entry.crc() >>> 24) & 0xff)) {
                throw new IOException("wrong password for " + entry.name());
            }
            if (i >= 12) out[i - 12] = plain;
        }
        return out;
    }

    private static void updateKeys(int[] keys, byte b) {
        keys[0] = crc32(keys[0], b);
        keys[1] = keys[1] + (keys[0] & 0xff);
        keys[1] = keys[1] * 134775813 + 1;
        keys[2] = crc32(keys[2], (byte) (keys[1] >>> 24));
    }

    private static int streamByte(int[] keys) {
        int temp = (keys[2] | 2) & 0xffff;
        return ((temp * (temp ^ 1)) >>> 8) & 0xff;
    }

    private static final int[] CRC_TABLE = new int[256];

    static {
        for (int i = 0; i < 256; i++) {
            int c = i;
            for (int k = 0; k < 8; k++) c = (c & 1) != 0 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
            CRC_TABLE[i] = c;
        }
    }

    private static int crc32(int crc, byte b) {
        return (crc >>> 8) ^ CRC_TABLE[(crc ^ b) & 0xff];
    }
}
