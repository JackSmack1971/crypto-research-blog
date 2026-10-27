#!/usr/bin/env python3
"""Editorial content and visualization source must survive the build."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import build  # noqa: E402
import signatures  # noqa: E402


def setUpModule() -> None:
    build.main()


class ContentIntegrityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = signatures.load_fixture()
        cls.notes = signatures.article_sources()

    def test_fixture_covers_every_article(self) -> None:
        slugs = [note["slug"] for note in self.notes]
        self.assertEqual(list(self.fixture), slugs)

    def test_source_matches_reviewed_baseline(self) -> None:
        for note in self.notes:
            current = signatures.signature(note["html"], strip_bar=False)
            expected = self.fixture[note["slug"]]
            self.assertEqual(
                current["text"],
                expected["text"],
                f"{note['slug']} text drifted from the baseline: "
                f"{signatures.first_difference(current['text'], expected['text'])}",
            )
            for field in ("headings", "links", "blocks", "tables", "alts"):
                self.assertEqual(current[field], expected[field], f"{note['slug']} {field}")
            for field in ("svgCount", "svgSha256", "imageCount", "imageSha256", "scriptCount", "scriptSha256"):
                self.assertEqual(current[field], expected[field], f"{note['slug']} {field}")

    def test_build_preserves_source_signature(self) -> None:
        for note in self.notes:
            built_path = build.DIST / note["slug"] / "index.html"
            built = built_path.read_text(encoding="utf-8")
            current = signatures.signature(built, strip_bar=True)
            expected = signatures.signature(note["html"], strip_bar=False)
            self.assertEqual(
                current["text"],
                expected["text"],
                f"{note['slug']} build changed article text: "
                f"{signatures.first_difference(current['text'], expected['text'])}",
            )
            for field in (
                "headings",
                "links",
                "blocks",
                "tables",
                "alts",
                "svgSha256",
                "imageSha256",
                "scriptSha256",
            ):
                self.assertEqual(current[field], expected[field], f"{note['slug']} built {field}")


if __name__ == "__main__":
    unittest.main()
