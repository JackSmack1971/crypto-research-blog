"""One title convention: no site or category suffix in an article's <title> (IMN-006).

Headline wording is untouched. Only a trailing "| <site/category>" or
"— <month> <category> Essay" style suffix is disallowed; an em dash or colon
inside a headline is legitimate.
"""
import html
import re
import unittest

import build

SUFFIXES = (
    " | Independent Market Notes",
    " | Crypto Research",
    " | Market Investigation",
    " | Market Essay",
    " | Crypto Market Analysis",
    " | Independent Crypto Analysis",
    " | Independent Market Analysis",
    " | Pyth Network Analysis",
    " | Independent Analysis",
    " — October 2026 Crypto Market Essay",
)

HELD_PENDING_OWNER_DECISION: set[str] = set()  # no title is currently held


def source_title(note):
    match = re.search(r"<title\b[^>]*>(.*?)</title>", note["html"], flags=re.I | re.S)
    return html.unescape(" ".join(match.group(1).split()))


class TitleConventionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notes = build.load_notes()

    def violators(self):
        found = set()
        for note in self.notes:
            title = source_title(note)
            if "|" in title or title.endswith(SUFFIXES):
                found.add(note["slug"])
        return found

    def test_only_held_titles_carry_a_suffix(self):
        self.assertEqual(self.violators(), HELD_PENDING_OWNER_DECISION)

    def test_catalog_titles_are_unchanged_by_the_convention(self):
        # Catalog titles were already suffix-free; the convention must not touch them.
        for note in self.notes:
            self.assertNotIn("|", note["title"], note["slug"])
            self.assertFalse(note["title"].endswith(SUFFIXES), note["slug"])


if __name__ == "__main__":
    unittest.main()
