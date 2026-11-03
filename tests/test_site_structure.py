#!/usr/bin/env python3
"""Routes, canonical URLs, RSS, and the Pages deploy gate."""

from __future__ import annotations

import json
import re
import sys
import unittest
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import build  # noqa: E402
import signatures  # noqa: E402

METADATA = ROOT / "tests" / "fixtures" / "metadata.json"
TITLE_RE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.I | re.S)
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)"')


def setUpModule() -> None:
    build.main()


def raw_title(html: str) -> str:
    match = TITLE_RE.search(html)
    return " ".join(match.group(1).split()) if match else ""


def canonical(html: str) -> str:
    match = CANONICAL_RE.search(html)
    return match.group(1) if match else ""


def meta(html: str, name: str) -> str:
    values = build.meta_values(html, name)
    return values[0] if values else ""


def page_metadata(html: str) -> dict[str, str]:
    return {
        "title": raw_title(html),
        "description": meta(html, "description"),
        "canonical": canonical(html),
        "og:title": meta(html, "og:title"),
        "og:description": meta(html, "og:description"),
        "og:url": meta(html, "og:url"),
        "og:type": meta(html, "og:type"),
        "twitter:card": meta(html, "twitter:card"),
    }


def rss_items() -> list[dict[str, str]]:
    channel = ET.parse(build.DIST / "feed.xml").getroot().find("channel")
    items = []
    for item in channel.findall("item"):
        items.append(
            {
                "title": item.findtext("title") or "",
                "link": item.findtext("link") or "",
                "description": item.findtext("description") or "",
            }
        )
    return items


def write_metadata() -> None:
    build.main()
    site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    catalog = json.loads((ROOT / "content" / "articles.json").read_text(encoding="utf-8"))
    articles = {}
    for entry in catalog:
        html = (build.DIST / entry["slug"] / "index.html").read_text(encoding="utf-8")
        articles[entry["slug"]] = page_metadata(html)
    index = (build.DIST / "index.html").read_text(encoding="utf-8")
    payload = {
        "home": page_metadata(index),
        "articles": articles,
        "rss": rss_items(),
    }
    METADATA.parent.mkdir(parents=True, exist_ok=True)
    METADATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {METADATA.relative_to(ROOT)}")


class SiteStructureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "content" / "articles.json").read_text(encoding="utf-8"))
        cls.metadata = json.loads(METADATA.read_text(encoding="utf-8"))
        cls.base = cls.site["url"].rstrip("/")

    def test_required_files_exist(self) -> None:
        for relative in (
            "index.html",
            "404.html",
            "feed.xml",
            "sitemap.xml",
            "robots.txt",
            "favicon.svg",
            "design-system.css",
            "search.js",
            "search-index.json",
        ):
            self.assertTrue((build.DIST / relative).is_file(), relative)
        for entry in self.catalog:
            self.assertTrue((build.DIST / entry["slug"] / "index.html").is_file(), entry["slug"])

    def test_article_urls_and_metadata_match_baseline(self) -> None:
        self.assertEqual([entry["slug"] for entry in self.catalog], list(self.metadata["articles"]))
        for entry in self.catalog:
            slug = entry["slug"]
            html = (build.DIST / slug / "index.html").read_text(encoding="utf-8")
            actual = page_metadata(html)
            self.assertEqual(actual, self.metadata["articles"][slug], slug)
            self.assertEqual(actual["canonical"], f"{self.base}/{slug}/")
            self.assertEqual(actual["og:url"], f"{self.base}/{slug}/")
            self.assertIn('href="../"', html)
            self.assertIn('href="../design-system.css"', html)
            self.assertNotIn("site-bar.css", html)

    def test_homepage_loads_shared_tokens(self) -> None:
        index = (build.DIST / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="design-system.css"', index)
        tokens = (build.DIST / "design-system.css").read_text(encoding="utf-8")
        for token in ("--cr-bg:", "--cr-ink:", "--cr-muted:", "--cr-accent:", "--cr-measure:", "--cr-container:"):
            self.assertIn(token, tokens)
        self.assertIn('class="cr-home"', index)
        self.assertIn("#cr-sitebar", tokens)
        without_comments = re.sub(r"/\*.*?\*/", "", tokens, flags=re.S)
        self.assertNotIn("!important", without_comments)

    def test_homepage_lists_catalog_copy(self) -> None:
        index = (build.DIST / "index.html").read_text(encoding="utf-8")
        self.assertEqual(page_metadata(index), self.metadata["home"])
        self.assertIn(f'<link rel="canonical" href="{self.base}/">', index)
        for entry in self.catalog:
            self.assertIn(f'href="{entry["slug"]}/"', index)
            self.assertIn(escape(entry["title"]), index)
            self.assertIn(escape(entry["dek"]), index)

    def test_featured_story_and_search_index_are_complete(self) -> None:
        index = (build.DIST / "index.html").read_text(encoding="utf-8")
        featured_slug = self.site["featured_slug"]
        featured = next(entry for entry in self.catalog if entry["slug"] == featured_slug)
        self.assertIn('class="feature wrap"', index)
        self.assertEqual(index.count('class="entry"'), len(self.catalog) - 1)
        self.assertNotIn(f'class="entry" data-slug="{featured_slug}"', index)
        search_data = json.loads((build.DIST / "search-index.json").read_text(encoding="utf-8"))
        self.assertEqual({row["slug"] for row in search_data}, {row["slug"] for row in self.catalog})
        for entry in self.catalog:
            self.assertIn(entry["topic"], build.TOPICS)
            self.assertIn(entry["research_type"], build.RESEARCH_TYPES)
            self.assertIsInstance(entry["assets"], list)
        self.assertIn('aria-live="polite"', index)
        self.assertIn('data-empty-state', index)

    def test_article_canonicals_follow_configured_domain(self) -> None:
        for entry in self.catalog:
            html = (build.DIST / entry["slug"] / "index.html").read_text(encoding="utf-8")
            self.assertEqual(canonical(html), f'{self.base}/{entry["slug"]}/')

    def test_invalid_taxonomy_values_fail_with_actionable_errors(self) -> None:
        catalog = json.loads((ROOT / "content" / "articles.json").read_text(encoding="utf-8"))
        catalog[0]["topic"] = "unapproved-topic"
        with patch.object(build, "load_json", return_value=catalog):
            with self.assertRaisesRegex(SystemExit, "topic must be one of"):
                build.load_notes()

        catalog[0]["topic"] = "protocol-research"
        catalog[0]["assets"] = ["lowercase"]
        with patch.object(build, "load_json", return_value=catalog):
            with self.assertRaisesRegex(SystemExit, "uppercase ticker symbols"):
                build.load_notes()

    def test_unknown_featured_slug_fails_the_build(self) -> None:
        notes = build.load_notes()
        with self.assertRaisesRegex(SystemExit, "does not match an article"):
            build.select_featured(notes, {"featured_slug": "missing-article"})

    def test_rss_matches_baseline(self) -> None:
        items = rss_items()
        self.assertEqual(items, self.metadata["rss"])
        for entry, item in zip(self.catalog, items):
            self.assertEqual(item["link"], f"{self.base}/{entry['slug']}/")
            self.assertEqual(item["title"], entry["title"])
            self.assertEqual(item["description"], entry["dek"])

    def test_deploy_job_stays_on_main(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        concurrency = workflow.split("jobs:", 1)[0]
        self.assertIn("pages-deploy", concurrency)
        self.assertIn("format('pages-{0}', github.ref)", concurrency)
        self.assertIn("cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}", concurrency)
        self.assertNotIn('group: "pages"', concurrency)
        self.assertIn("actions/upload-pages-artifact@v3", workflow)
        self.assertIn("actions/deploy-pages@v4", workflow)
        self.assertIn("github.ref == 'refs/heads/main'", workflow)
        self.assertIn("github.event_name != 'pull_request'", workflow)
        deploy = workflow.split("deploy:", 1)[1]
        self.assertIn(
            "if: github.ref == 'refs/heads/main' && github.event_name != 'pull_request'",
            deploy,
        )
        self.assertIn("needs: [build, styling-check]", deploy)


if __name__ == "__main__":
    write_metadata()
