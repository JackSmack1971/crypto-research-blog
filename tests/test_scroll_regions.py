"""Keyboard access for the three horizontally scrollable article tables."""

from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser

import build


ROOT = build.ROOT
TARGETS = {
    "aero-at-0-68": ("table-scroll", "AERO unlock data table"),
    "bitcoin-buying-imbalance": ("tablewrap", "Bitcoin buying imbalance data table"),
    "token-unlock-liquidity-illusion-90-day-calendar": (
        "scroll",
        "90-day token unlock calendar data table",
    ),
}


class Elements(HTMLParser):
    def __init__(self, html: str) -> None:
        super().__init__()
        self.items: list[tuple[str, dict[str, str | None]]] = []
        self.feed(html)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.items.append((tag, dict(attrs)))


def body_inner(html: str) -> str:
    match = re.search(r"<body\b[^>]*>(.*?)</body\s*>", html, flags=re.I | re.S)
    if not match:
        raise AssertionError("article is missing a body")
    return match.group(1)


class ScrollRegionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        build.main()

    def assert_wrapper_accessible(self, slug: str) -> None:
        class_name, label = TARGETS[slug]
        page = (build.DIST / slug / "index.html").read_text(encoding="utf-8")
        matches = [
            (tag, attrs)
            for tag, attrs in Elements(page).items
            if tag == "div" and class_name in (attrs.get("class") or "").split()
        ]
        self.assertEqual(len(matches), 1, f"expected one .{class_name} wrapper")
        _, attrs = matches[0]
        self.assertEqual(attrs.get("tabindex"), "0")
        self.assertEqual(attrs.get("role"), "region")
        self.assertEqual(attrs.get("aria-label"), label)

    def test_aero_table_scroll_is_keyboard_focusable(self) -> None:
        self.assert_wrapper_accessible("aero-at-0-68")

    def test_bitcoin_tablewrap_is_keyboard_focusable(self) -> None:
        self.assert_wrapper_accessible("bitcoin-buying-imbalance")

    def test_unlock_calendar_scroll_is_keyboard_focusable(self) -> None:
        self.assert_wrapper_accessible("token-unlock-liquidity-illusion-90-day-calendar")

    def test_no_other_body_element_changes(self) -> None:
        for slug, (class_name, _) in TARGETS.items():
            with self.subTest(slug=slug):
                source = (ROOT / "content" / f"{slug}.html").read_text(encoding="utf-8")
                built = (build.DIST / slug / "index.html").read_text(encoding="utf-8")
                built_body, bar_count = re.subn(
                    r'<nav id="cr-sitebar"[^>]*>.*?</nav>',
                    "",
                    body_inner(built),
                    count=1,
                    flags=re.I | re.S,
                )
                self.assertEqual(bar_count, 1, "expected the generated site bar")

                wrapper, count = re.subn(
                    rf'<div class="{re.escape(class_name)}"[^>]*>',
                    lambda match: re.sub(
                        r'\s+(?:tabindex="[^"]*"|role="[^"]*"|aria-label="[^"]*")',
                        "",
                        match.group(0),
                    ),
                    built_body,
                    count=1,
                )
                self.assertEqual(count, 1, f"expected one generated .{class_name} wrapper")
                self.assertEqual(wrapper, body_inner(source))


if __name__ == "__main__":
    unittest.main()
