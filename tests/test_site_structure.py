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
                "guid": item.findtext("guid") or "",
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
        catalog[0].pop("topic")
        with patch.object(build, "load_json", return_value=catalog):
            with self.assertRaisesRegex(SystemExit, "topic must be one of"):
                build.load_notes()

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
            self.assertEqual(
                item["guid"],
                f"{self.site['rss_guid_origin'].rstrip('/')}/{entry['slug']}/",
            )
            self.assertEqual(item["title"], entry["title"])
            self.assertEqual(item["description"], entry["dek"])

    def test_deploy_job_stays_on_main_without_browser_install(self) -> None:
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
        self.assertIn("needs: [build, content-check]", deploy)
        self.assertNotIn("chromium", workflow.lower())
        self.assertNotIn("playwright", workflow.lower())

    @staticmethod
    def related_note(slug: str, date_value: str, topic: str, assets: list[str], research_type: str) -> dict:
        return {
            "slug": slug,
            "date": date_value,
            "topic": topic,
            "assets": assets,
            "research_type": research_type,
        }

    def test_rank_related_notes_uses_weight_date_and_catalog_ties(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", ["BTC", "ETH"], "snapshot")
        shared = self.related_note("shared", "2026-01-02", "other", ["BTC"], "other")
        topic_and_type = self.related_note("topic-type", "2026-01-03", "alpha", [], "snapshot")
        tie_earlier = self.related_note("tie-earlier", "2026-01-04", "other", ["ETH"], "other")
        tie_later = self.related_note("tie-later", "2026-01-04", "alpha", [], "snapshot")
        notes = [source, shared, tie_earlier, tie_later, topic_and_type]
        result = build.rank_related_notes(source, notes)
        self.assertEqual(result["variant"], "related")
        self.assertEqual([item["slug"] for item in result["notes"]], ["tie-earlier", "tie-later", "topic-type"])

    def test_render_related_notes_renders_related_markup_and_escapes_catalog_values(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", ["BTC"], "snapshot")
        candidate = self.related_note('candidate" data-x="1', '2026-01-02" data-x="1', "alpha", ["BTC"], "snapshot")
        candidate["title"] = 'A <Note> "quoted" & checked'
        expected = (
            '<nav id="cr-related" aria-label="More notes"><div class="cr-related-inner">'
            '<h2>Related notes</h2><ul><li><a href="../candidate&quot; data-x=&quot;1/">'
            'A &lt;Note&gt; &quot;quoted&quot; &amp; checked</a> '
            '<time datetime="2026-01-02&quot; data-x=&quot;1">'
            '2026-01-02&quot; data-x=&quot;1</time></li></ul>'
            '<a href="../">All notes</a></div></nav>'
        )
        with patch.object(
            build,
            "rank_related_notes",
            return_value={"variant": "related", "notes": [candidate]},
        ):
            self.assertEqual(build.render_related_notes(source, [source, candidate]), expected)

    def test_render_related_notes_uses_latest_notes_when_scores_are_zero(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", [], "snapshot")
        candidate = self.related_note("candidate", "2026-01-02", "other", [], "other")
        candidate["title"] = "Latest & safest"
        self.assertEqual(
            build.render_related_notes(source, [source, candidate]),
            '<nav id="cr-related" aria-label="More notes"><div class="cr-related-inner">'
            '<h2>Latest notes</h2><ul><li><a href="../candidate/">'
            'Latest &amp; safest</a> <time datetime="2026-01-02">2026-01-02</time></li></ul>'
            '<a href="../">All notes</a></div></nav>',
        )

    def test_render_related_notes_omits_latest_heading_for_single_article(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", [], "snapshot")
        self.assertEqual(
            build.render_related_notes(source, [source]),
            '<nav id="cr-related" aria-label="More notes"><div class="cr-related-inner">'
            '<a href="../">All notes</a></div></nav>',
        )

    def test_rank_related_notes_one_shared_asset_beats_same_topic(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", ["BTC"], "snapshot")
        same_topic = self.related_note("topic", "2026-01-03", "alpha", [], "other")
        one_asset = self.related_note("asset", "2026-01-02", "other", ["BTC"], "other")
        result = build.rank_related_notes(source, [source, same_topic, one_asset])
        self.assertEqual(result["notes"][0], one_asset)

    def test_rank_related_notes_two_shared_assets_beat_topic_and_type(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", ["BTC", "ETH"], "snapshot")
        topic_type = self.related_note("topic-type", "2026-01-03", "alpha", [], "snapshot")
        two_assets = self.related_note("two-assets", "2026-01-02", "other", ["BTC", "ETH"], "other")
        result = build.rank_related_notes(source, [source, topic_type, two_assets])
        self.assertEqual(result["notes"][0], two_assets)

    def test_rank_related_notes_equal_score_uses_newer_date(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", ["BTC"], "snapshot")
        asset = self.related_note("asset", "2026-01-02", "other", ["BTC"], "other")
        topic_type = self.related_note("topic-type", "2026-01-03", "alpha", [], "snapshot")
        result = build.rank_related_notes(source, [source, asset, topic_type])
        self.assertEqual(result["notes"][0], topic_type)

    def test_rank_related_notes_excludes_self_by_slug(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", ["BTC"], "snapshot")
        duplicate_slug = self.related_note("source", "2026-01-03", "alpha", ["BTC"], "snapshot")
        neighbour = self.related_note("neighbour", "2026-01-02", "alpha", ["BTC"], "snapshot")
        result = build.rank_related_notes(source, [source, duplicate_slug, neighbour])
        self.assertEqual([entry["slug"] for entry in result["notes"]], ["neighbour"])

    def test_rank_related_notes_equal_dates_keep_passed_catalog_order(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", ["BTC"], "snapshot")
        later_position = self.related_note("later-position", "2026-01-03", "other", ["BTC"], "other")
        earlier_position = self.related_note("earlier-position", "2026-01-03", "alpha", [], "snapshot")
        result = build.rank_related_notes(source, [source, later_position, earlier_position])
        self.assertEqual([entry["slug"] for entry in result["notes"]], ["later-position", "earlier-position"])

    def test_rank_related_notes_zero_score_falls_back_to_latest(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", [], "snapshot")
        old = self.related_note("old", "2026-01-01", "other", [], "other")
        newest_first = self.related_note("newest-first", "2026-01-03", "other", [], "other")
        newest_second = self.related_note("newest-second", "2026-01-03", "other", [], "other")
        middle = self.related_note("middle", "2026-01-02", "other", [], "other")
        result = build.rank_related_notes(source, [source, old, newest_first, newest_second, middle])
        self.assertEqual(result["variant"], "latest")
        self.assertEqual([entry["slug"] for entry in result["notes"]], ["newest-first", "newest-second", "middle"])

    def test_rank_related_notes_returns_fewer_than_three_candidates(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", [], "snapshot")
        candidate = self.related_note("candidate", "2026-01-02", "alpha", [], "snapshot")
        result = build.rank_related_notes(source, [source, candidate])
        self.assertEqual(len(result["notes"]), 1)
        self.assertIs(result["notes"][0], candidate)

    def test_rank_related_notes_no_candidates(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", [], "snapshot")
        result = build.rank_related_notes(source, [source])
        self.assertEqual(result, {"variant": "none", "notes": []})

    def test_rank_related_notes_exact_shape_and_original_entries(self) -> None:
        source = self.related_note("source", "2026-01-01", "alpha", [], "snapshot")
        candidates = [
            self.related_note(f"candidate-{index}", f"2026-01-0{index + 2}", "alpha", [], "snapshot")
            for index in range(4)
        ]
        result = build.rank_related_notes(source, [source, *candidates])
        self.assertEqual(set(result), {"variant", "notes"})
        self.assertLessEqual(len(result["notes"]), 3)
        for entry in result["notes"]:
            self.assertTrue(any(entry is candidate for candidate in candidates))


if __name__ == "__main__":
    write_metadata()
