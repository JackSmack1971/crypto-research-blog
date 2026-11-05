"""Bounded structural inspection, not a JPEG/WebP entropy decoder.

PNG CRCs and compressed scanlines are checked fully for non-interlaced 8-bit
RGB/RGBA artwork. JPEG marker/scan framing and WebP chunk/key-frame headers are
checked; their compressed pixels still require a decoder in artwork review.
Unsupported variants fail closed. All formats are bounded to 8 MiB/1200x630.
"""
import struct
import zlib

MAX_BYTES = 8 * 1024 * 1024
SIZE = (1200, 630)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inspect_image(raw, mime):
    require(0 < len(raw) <= MAX_BYTES, 'image exceeds the 8 MiB inspection limit')
    if mime == 'image/png':
        try:
            return png_size(raw)
        except zlib.error as error:
            raise ValueError('invalid PNG compressed data') from error
    if mime == 'image/jpeg':
        return jpeg_size(raw)
    return webp_size(raw)


def png_size(raw):
    require(raw.startswith(b'\x89PNG\r\n\x1a\n'), 'invalid PNG signature')
    offset, chunks, data = 8, [], bytearray()
    size = None
    channels = 0
    while offset < len(raw):
        require(offset + 12 <= len(raw), 'truncated PNG chunk')
        length = int.from_bytes(raw[offset:offset + 4], 'big')
        kind = raw[offset + 4:offset + 8]
        end = offset + 12 + length
        require(end <= len(raw), 'truncated PNG payload')
        payload = raw[offset + 8:end - 4]
        require(zlib.crc32(kind + payload) == int.from_bytes(raw[end - 4:end], 'big'), 'PNG CRC mismatch')
        if not chunks:
            require(kind == b'IHDR' and length == 13, 'missing PNG header')
        if kind == b'IHDR':
            require(not chunks and length == 13, 'duplicate PNG header')
            width, height, depth, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', payload)
            size = (width, height)
            require(size == SIZE, 'intrinsic dimensions must be 1200 x 630')
            require(depth == 8 and color in (2, 6) and compression == filtering == interlace == 0,
                    'PNG must be non-interlaced 8-bit RGB or RGBA')
            channels = 3 if color == 2 else 4
        elif kind == b'IDAT':
            require(not data or chunks[-1] == b'IDAT', 'nonconsecutive PNG image data')
            data.extend(payload)
        elif kind == b'IEND':
            require(length == 0 and end == len(raw) and data, 'invalid PNG end')
        elif kind[:1].isupper():
            require(kind == b'PLTE' and b'IDAT' not in chunks and length % 3 == 0,
                    'unsupported critical PNG chunk')
        chunks.append(kind)
        offset = end
    require(chunks and chunks[-1] == b'IEND', 'missing PNG end')
    stride = SIZE[0] * channels + 1
    expected = stride * SIZE[1]
    decoder = zlib.decompressobj()
    pixels = decoder.decompress(data, expected + 1)
    require(len(pixels) == expected and decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
            'invalid PNG compressed scanlines')
    require(all(pixels[i] <= 4 for i in range(0, expected, stride)), 'invalid PNG scanline filter')
    return size


def jpeg_size(raw):
    require(raw.startswith(b'\xff\xd8'), 'invalid JPEG signature')
    offset, size, scans, tables = 2, None, 0, set()
    while offset < len(raw):
        require(raw[offset] == 255, 'invalid JPEG marker boundary')
        while offset < len(raw) and raw[offset] == 255:
            offset += 1
        require(offset < len(raw), 'truncated JPEG marker')
        marker = raw[offset]
        offset += 1
        if marker == 0xD9:
            require(offset == len(raw) and size and scans and {0xDB, 0xC4} <= tables,
                    'incomplete JPEG image')
            return size
        require(marker not in (0, 0xD8) and not 0xD0 <= marker <= 0xD7, 'unexpected JPEG marker')
        require(offset + 2 <= len(raw), 'truncated JPEG segment')
        length = int.from_bytes(raw[offset:offset + 2], 'big')
        require(length >= 2 and offset + length <= len(raw), 'invalid JPEG segment length')
        segment = raw[offset + 2:offset + length]
        offset += length
        if marker in (0xC0, 0xC2):
            require(size is None and len(segment) >= 6, 'invalid JPEG frame')
            components = segment[5]
            require(segment[0] == 8 and components in (1, 3) and len(segment) == 6 + 3 * components,
                    'unsupported JPEG frame')
            size = (int.from_bytes(segment[3:5], 'big'), int.from_bytes(segment[1:3], 'big'))
            require(size == SIZE, 'intrinsic dimensions must be 1200 x 630')
        elif marker == 0xDB:
            pos = 0
            while pos < len(segment):
                table = segment[pos]
                require(table >> 4 in (0, 1) and table & 15 <= 3, 'invalid JPEG quantization table')
                pos += 1 + 64 * (1 + (table >> 4))
            require(pos == len(segment) and pos > 0, 'truncated JPEG quantization table')
            tables.add(marker)
        elif marker == 0xC4:
            pos = 0
            while pos < len(segment):
                require(pos + 17 <= len(segment), 'truncated JPEG Huffman table')
                require(segment[pos] >> 4 in (0, 1) and segment[pos] & 15 <= 3, 'invalid JPEG Huffman table')
                count = sum(segment[pos + 1:pos + 17])
                require(0 < count <= 256, 'invalid JPEG Huffman counts')
                pos += 17 + count
            require(pos == len(segment) and pos > 0, 'truncated JPEG Huffman values')
            tables.add(marker)
        elif marker == 0xDA:
            require(size and len(segment) >= 6 and len(segment) == 4 + 2 * segment[0], 'invalid JPEG scan header')
            scans += 1
            start = offset
            while offset < len(raw):
                if raw[offset] != 255:
                    offset += 1
                    continue
                require(offset + 1 < len(raw), 'truncated JPEG scan')
                following = raw[offset + 1]
                if following == 0 or 0xD0 <= following <= 0xD7:
                    offset += 2
                else:
                    break
            require(offset > start, 'empty JPEG scan')
        else:
            require(0xE0 <= marker <= 0xEF or marker in (0xFE, 0xDD), 'unsupported JPEG marker')
    raise ValueError('missing JPEG end')


def webp_size(raw):
    require(raw[:4] == b'RIFF' and raw[8:12] == b'WEBP' and
            int.from_bytes(raw[4:8], 'little') + 8 == len(raw), 'invalid WebP container')
    offset, canvas, image = 12, None, None
    chunks = []
    while offset < len(raw):
        require(offset + 8 <= len(raw), 'truncated WebP chunk')
        kind = raw[offset:offset + 4]
        length = int.from_bytes(raw[offset + 4:offset + 8], 'little')
        end = offset + 8 + length
        require(end + (length % 2) <= len(raw), 'truncated WebP payload')
        payload = raw[offset + 8:end]
        if length % 2:
            require(raw[end] == 0, 'invalid WebP padding')
        if kind == b'VP8X':
            require(not chunks and length == 10 and not payload[0] & 2, 'unsupported WebP extended header/animation')
            canvas = (1 + int.from_bytes(payload[4:7], 'little'), 1 + int.from_bytes(payload[7:10], 'little'))
        elif kind == b'VP8 ':
            require(image is None and length > 10 and payload[3:6] == b'\x9d\x01\x2a', 'invalid WebP key frame')
            tag = int.from_bytes(payload[:3], 'little')
            require(tag & 1 == 0 and tag >> 5 < length - 10, 'invalid WebP frame partition')
            image = (int.from_bytes(payload[6:8], 'little') & 0x3FFF,
                     int.from_bytes(payload[8:10], 'little') & 0x3FFF)
        elif kind == b'VP8L':
            require(image is None and length > 5 and payload[0] == 0x2F, 'invalid lossless WebP header')
            bits = int.from_bytes(payload[1:5], 'little')
            require(bits >> 29 == 0, 'unsupported lossless WebP version')
            image = (1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF))
        else:
            require(canvas and kind in (b'ALPH', b'ICCP', b'EXIF', b'XMP '), 'unsupported WebP chunk')
        chunks.append(kind)
        offset = end + length % 2
    require(image == SIZE and (canvas is None or canvas == image), 'intrinsic dimensions must be 1200 x 630')
    return image
