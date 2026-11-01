"""Focused coverage for social-image publishing and legacy compatibility."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build


class FeaturedImageTest(unittest.TestCase):
    def test_existing_articles_without_images_remain_unchanged(self):
        notes = build.load_notes()
        self.assertTrue(notes)
        self.assertTrue(all(note["image"] is None for note in notes))
        head = build.article_extra_head(notes[0], build.load_site())
        self.assertNotIn('property="og:image"', head)
        self.assertIn('content="summary"', head)

    def test_featured_image_generates_social_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            directory = root / "assets" / "featured"
            directory.mkdir(parents=True)
            # Small byte-level JPEG fixture. Tests header validation and publishing,
            # not artwork quality or a complete decoder.
            (directory / "example.jpg").write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 32 + b"\xff\xd9")
            entry = {
                "image": "assets/featured/example.jpg",
                "image_alt": 'Bitcoin "market" analysis',
                "image_width": 1200,
                "image_height": 630,
                "image_mime_type": "image/jpeg",
            }
            with patch.object(build, "ROOT", root):
                image = build.featured_image(entry, "example")
            note = dict(build.load_notes()[0], image=image)
            rendered = build.article_extra_head(note, build.load_site())
            expected = build.load_site()["url"] + "/assets/featured/example.jpg"
            self.assertIn('property="og:image" content="' + expected + '"', rendered)
            self.assertIn('name="twitter:image" content="' + expected + '"', rendered)
            self.assertIn('name="twitter:card" content="summary_large_image"', rendered)
            self.assertIn('property="og:image:alt" content="Bitcoin &quot;market&quot; analysis"', rendered)
            self.assertIn('"image": "' + expected + '"', rendered)

    def test_invalid_paths_missing_files_and_alt_are_rejected(self):
        for value in ("../secret.jpg", "/assets/featured/a.jpg", "assets/featured/../escape.jpg", "https://example.com/a.jpg"):
            with self.subTest(value=value), self.assertRaises(SystemExit):
                build.featured_image({"image": value, "image_alt": "alt"}, "example")
        with self.assertRaises(SystemExit):
            build.featured_image({"image": "assets/featured/missing.jpg", "image_alt": "alt"}, "example")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            p = root / "assets" / "featured" / "example.jpg"
            p.parent.mkdir(parents=True)
            p.write_bytes(b"not a jpeg")
            with patch.object(build, "ROOT", root), self.assertRaises(SystemExit):
                build.featured_image({"image": "assets/featured/example.jpg", "image_alt": "alt"}, "example")
            p.write_bytes(b"\xff\xd8\xff" + b"\x00" * 24 + b"\xff\xd9")
            with patch.object(build, "ROOT", root), self.assertRaises(SystemExit):
                build.featured_image({"image": "assets/featured/example.jpg"}, "example")
            with patch.object(build, "ROOT", root), self.assertRaises(SystemExit):
                build.featured_image({"image": "assets/featured/example.jpg", "image_alt": "alt", "image_width": 800}, "example")


if __name__ == "__main__":
    unittest.main()
