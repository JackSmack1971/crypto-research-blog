#!/usr/bin/env python3
"""Content and visualization signatures for the research notes.

The fixtures are a reviewed baseline. Rebuild them only after an intentional
content change, then look at the diff before committing:

    python3 tests/signatures.py --write

A failing check must not refresh these files on its own.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "content-signatures.json"
CONTENT = ROOT / "content"
DIST = ROOT / "dist"

HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCK_TAGS = {"p", "li", "blockquote", "figcaption", "caption"}


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _collapse(value: str) -> str:
    return " ".join(value.split())


class SemanticExtractor(HTMLParser):
    """Visible editorial structure, ignoring style, script, and SVG markup."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.svg = 0
        self.headings: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.blocks: list[dict[str, str]] = []
        self.tables: list[list[list[str]]] = []
        self.alts: list[str] = []
        self._stack: list[dict] = []
        self._table: list[list[str]] | None = None
        self._row: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in ("script", "style"):
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "svg":
            self.svg += 1
            return
        if self.svg:
            return
        values = {key.lower(): (value or "") for key, value in attrs}
        if tag == "img":
            alt = _collapse(values.get("alt", ""))
            if alt:
                self.alts.append(alt)
        if tag == "table":
            self._table = []
        elif tag == "tr" and self._table is not None:
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._stack.append({"kind": "cell", "tag": tag, "parts": []})
        elif tag in HEADING_TAGS:
            self._stack.append({"kind": "heading", "tag": tag, "parts": []})
        elif tag in BLOCK_TAGS:
            self._stack.append({"kind": "block", "tag": tag, "parts": []})
        elif tag == "a":
            self._stack.append({"kind": "link", "href": values.get("href", ""), "parts": []})

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
            return
        if self.skip:
            return
        if tag == "svg" and self.svg:
            self.svg -= 1
            return
        if self.svg:
            return
        frame = self._stack[-1] if self._stack else None
        if frame and (
            (frame["kind"] == "cell" and tag == frame["tag"])
            or (frame["kind"] == "heading" and tag == frame["tag"])
            or (frame["kind"] == "block" and tag == frame["tag"])
            or (frame["kind"] == "link" and tag == "a")
        ):
            frame = self._stack.pop()
            text = _collapse("".join(frame["parts"]))
            if frame["kind"] == "heading":
                self.headings.append({"tag": frame["tag"], "text": text})
            elif frame["kind"] == "block" and text:
                self.blocks.append({"tag": frame["tag"], "text": text})
            elif frame["kind"] == "cell":
                if self._row is not None:
                    self._row.append(text)
            elif frame["kind"] == "link":
                self.links.append({"href": frame["href"], "text": text})
            if self._stack and text:
                self._stack[-1]["parts"].append(text)
            return
        if tag == "tr" and self._row is not None and self._table is not None:
            self._table.append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            self.tables.append(self._table)
            self._table = None

    def handle_data(self, data: str) -> None:
        if self.skip or self.svg or not self._stack:
            return
        self._stack[-1]["parts"].append(data)


def _svgs(html: str) -> list[str]:
    return re.findall(r"<svg\b.*?</svg>", html, flags=re.I | re.S)


def _img_srcs(html: str) -> list[str]:
    srcs = []
    for tag in re.findall(r"<img\b[^>]*>", html, flags=re.I | re.S):
        match = re.search(r'\bsrc\s*=\s*["\']([^"\']*)["\']', tag, flags=re.I)
        if match:
            srcs.append(match.group(1))
    return srcs


def _scripts(html: str) -> list[str]:
    found = []
    for match in re.finditer(r"<script\b([^>]*)>(.*?)</script>", html, flags=re.I | re.S):
        if "ld+json" in match.group(1).lower():
            continue
        found.append(match.group(2))
    return found


def editorial_body(html: str, *, strip_bar: bool) -> str:
    body = build.body_inner(html)
    if strip_bar:
        body = build.strip_site_bar(body)
    return body


def signature(html: str, *, strip_bar: bool) -> dict:
    body = editorial_body(html, strip_bar=strip_bar)
    parser = SemanticExtractor()
    parser.feed(body)
    parser.close()
    svgs = _svgs(body)
    images = _img_srcs(body)
    scripts = _scripts(body)
    return {
        "text": build.visible_text(body),
        "headings": parser.headings,
        "links": parser.links,
        "blocks": parser.blocks,
        "tables": parser.tables,
        "alts": parser.alts,
        "svgCount": len(svgs),
        "svgSha256": [_sha(svg) for svg in svgs],
        "imageCount": len(images),
        "imageSha256": [_sha(src) for src in images],
        "scriptCount": len(scripts),
        "scriptSha256": [_sha(script) for script in scripts],
    }


def article_sources() -> list[dict]:
    catalog = json.loads((CONTENT / "articles.json").read_text(encoding="utf-8"))
    notes = []
    for entry in catalog:
        path = CONTENT / entry["source"]
        notes.append(
            {
                "slug": entry["slug"],
                "date": entry["date"],
                "title": entry["title"],
                "source": path,
                "html": path.read_text(encoding="utf-8"),
            }
        )
    return notes


def collect() -> dict:
    payload = {}
    for note in article_sources():
        payload[note["slug"]] = signature(note["html"], strip_bar=False)
    return payload


def write_fixture() -> None:
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(json.dumps(collect(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {FIXTURE.relative_to(ROOT)}")


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def first_difference(left: str, right: str) -> str:
    if left == right:
        return ""
    limit = min(len(left), len(right))
    for index in range(limit):
        if left[index] != right[index]:
            start = max(0, index - 48)
            return (
                f"at {index}: {left[start:index + 48]!r} != {right[start:index + 48]!r}"
            )
    return f"length {len(left)} != {len(right)}"


if __name__ == "__main__":
    if "--write" not in sys.argv:
        raise SystemExit("usage: python3 tests/signatures.py --write")
    write_fixture()
