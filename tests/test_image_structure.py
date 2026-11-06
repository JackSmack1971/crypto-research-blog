import struct
import base64
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch

import build
from image_validation import MAX_BYTES, inspect_image


def chunk(kind, payload):
    return struct.pack('>I', len(payload)) + kind + payload + struct.pack('>I', zlib.crc32(kind + payload))


def png(width=1200, height=630, pixels=None):
    if pixels is None:
        pixels = (b'\0' + b'\0\0\0' * width) * height
    header = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', header) + chunk(b'IDAT', zlib.compress(pixels)) + chunk(b'IEND', b'')


class ImageStructureTest(unittest.TestCase):
    def test_real_png_and_all_existing_jpegs(self):
        self.assertEqual(inspect_image(png(), 'image/png'), (1200, 630))
        for image in (build.ROOT / 'assets/featured').glob('*.jpg'):
            with self.subTest(image=image.name):
                self.assertEqual(inspect_image(image.read_bytes(), 'image/jpeg'), (1200, 630))

    def test_wrong_intrinsic_size_is_rejected_despite_catalog_dimensions(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'assets/featured/example.png'
            path.parent.mkdir(parents=True)
            path.write_bytes(png(1, 1))
            entry = dict(image='assets/featured/example.png', image_alt='alt', image_width=1200, image_height=630)
            with patch.object(build, 'ROOT', Path(temp)), self.assertRaisesRegex(SystemExit, 'intrinsic dimensions'):
                build.featured_image(entry, 'example')

    def test_corrupt_png_crc_compressed_data_filters_and_scanline_length(self):
        good = png()
        bad_crc = bytearray(good)
        bad_crc[-1] ^= 1
        bad_compressed = good[:33] + chunk(b'IDAT', b'not zlib') + chunk(b'IEND', b'')
        for raw in (bytes(bad_crc), bad_compressed, png(pixels=b'\0'),
                    png(pixels=(b'\5' + b'\0' * 3600) * 630), good[:-5], good + b'extra'):
            with self.subTest(length=len(raw)), self.assertRaises(ValueError):
                inspect_image(raw, 'image/png')

    def test_truncated_and_placeholder_jpegs_fail(self):
        real = (build.ROOT / 'assets/featured/deepbook-supply-transparency.jpg').read_bytes()
        for raw in (real[:-2], real[:200] + b'\xff\xd9',
                    b'\xff\xd8\xff\xe0' + b'\0' * 32 + b'\xff\xd9'):
            with self.assertRaises(ValueError):
                inspect_image(raw, 'image/jpeg')
        # Mutate only the actual JPEG SOF dimensions, retaining valid framing.
        marker = next(m for m in (b'\xff\xc0', b'\xff\xc2') if m in real)
        position = real.index(marker) + 5
        wrong = real[:position] + struct.pack('>HH', 1, 1) + real[position + 4:]
        with self.assertRaisesRegex(ValueError, 'intrinsic dimensions'):
            inspect_image(wrong, 'image/jpeg')

    def test_webp_missing_payload_and_bad_chunk_length_fail(self):
        for payload in (b'', b'VP8 ' + struct.pack('<I', 100) + b'\0' * 10,
                        b'VP8L' + struct.pack('<I', 4) + b'\x2f\0\0\0'):
            raw = b'RIFF' + struct.pack('<I', len(payload) + 4) + b'WEBP' + payload
            with self.assertRaises(ValueError):
                inspect_image(raw, 'image/webp')

    def test_oversized_payload_is_rejected_before_inspection(self):
        with self.assertRaisesRegex(ValueError, '8 MiB'):
            inspect_image(b'\0' * (MAX_BYTES + 1), 'image/jpeg')

    def test_real_webp_lossy_alpha_and_lossless_headers(self):
        # Decoder-generated solid artwork, no runtime decoder dependency.
        for encoded in ('UklGRowFAABXRUJQVlA4IIAFAACwpACdASqwBHYCPm02mUmkIyKhIAgAgA2JaW7hd2EbQAnsA99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJiAAA/v/rAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'UklGRtYFAABXRUJQVlA4WAoAAAAQAAAArwQAdQIAQUxQSDAAAAABBxARERASJP5fbyOi/xn/+c9//vOf//znP//5z3/+85///Oc///nPf/7zn//8PwdWUDgggAUAALCkAJ0BKrAEdgI+bTaZSaQjIqEgCACADYlpbuF3YRtACewD32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99snIe+2TkPfbJyHvtk5D32ych77ZOQ99smIAAD+/+sAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=', 'UklGRkIAAABXRUJQVlA4TDUAAAAvr0SdAAcQEf0PCAkS/6+3EdH/jP/85z//+c9//vOf//znP//5z3/+85///Oc///nPf/6fAwA='):
            self.assertEqual(inspect_image(base64.b64decode(encoded), "image/webp"), (1200, 630))
