#!/usr/bin/env python3
"""Editorial content and visualization source must survive the build."""

from __future__ import annotations

import sys
import re
import tempfile
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

    def test_sentence_edit_is_not_hidden_by_related_nav_exclusion(self) -> None:
        note = self.notes[0]
        built_path = build.DIST / note["slug"] / "index.html"
        built = built_path.read_text(encoding="utf-8")
        unchanged_fixture = self.fixture[note["slug"]]
        baseline = signatures.signature(built, strip_bar=True)
        self.assertEqual(
            baseline["text"],
            unchanged_fixture["text"],
            "generated-chrome exclusion must preserve the unchanged essay text",
        )
        first_paragraph, count = re.subn(
            r"(<p\b[^>]*>.*?)(</p>)",
            lambda match: match.group(1) + " Changed sentence." + match.group(2),
            built,
            count=1,
            flags=re.I | re.S,
        )
        self.assertEqual(count, 1, "built essay must have a paragraph to edit")
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_copy = Path(temporary_directory) / "edited-article.html"
            temporary_copy.write_text(first_paragraph, encoding="utf-8")
            edited = signatures.signature(
                temporary_copy.read_text(encoding="utf-8"), strip_bar=True
            )
        with self.assertRaises(AssertionError):
            self.assertEqual(
                edited["text"],
                unchanged_fixture["text"],
                "the exact-ID related-nav exclusion must not hide essay edits",
            )


if __name__ == "__main__":
    unittest.main()
