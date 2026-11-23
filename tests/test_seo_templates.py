"""Regression coverage for generated SEO schema and Netlify caching rules."""

import json
import unittest

import build


def schemas(html):
    return [json.loads(match.group(2)) for match in build.LD_JSON_RE.finditer(html)]


def typed_entities(data, schema_type):
    if isinstance(data, list):
        return [entity for item in data for entity in typed_entities(item, schema_type)]
    if not isinstance(data, dict):
        return []
    types = data.get("@type", [])
    if isinstance(types, str):
        types = [types]
    found = [data] if schema_type in types else []
    return found + typed_entities(data.get("@graph", []), schema_type)


class SeoTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = build.load_site()
        cls.notes = build.load_notes()
        build.main()

    def test_every_article_has_topic_breadcrumbs_and_publisher_logo(self):
        for note in self.notes:
            page = build.DIST / note["slug"] / "index.html"
            data = schemas(page.read_text(encoding="utf-8"))
            breadcrumbs = [
                entity
                for schema in data
                for entity in typed_entities(schema, "BreadcrumbList")
            ]
            self.assertEqual(len(breadcrumbs), 1, note["slug"])
            self.assertEqual(
                breadcrumbs[0]["itemListElement"],
                [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": self.site["url"] + "/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": note["topic_label"],
                        "item": f"{self.site['url']}/topics/{note['topic']}/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": note["title"],
                        "item": f"{self.site['url']}/{note['slug']}/",
                    },
                ],
                note["slug"],
            )
            posts = [post for schema in data for post in build.blog_postings(schema)]
            self.assertEqual(len(posts), 1, note["slug"])
            self.assertEqual(
                posts[0]["publisher"]["logo"],
                {
                    "@type": "ImageObject",
                    "url": self.site["url"] + "/favicon.svg",
                },
                note["slug"],
            )

    def test_homepage_has_website_schema(self):
        index = (build.DIST / "index.html").read_text(encoding="utf-8")
        websites = [
            entity
            for schema in schemas(index)
            for entity in typed_entities(schema, "WebSite")
        ]
        self.assertEqual(
            websites,
            [
                {
                    "@type": "WebSite",
                    "name": self.site["title"],
                    "url": self.site["url"] + "/",
                }
            ],
        )

    def test_build_emits_document_and_asset_cache_rules(self):
        headers = (build.DIST / "_headers").read_text(encoding="utf-8")
        self.assertEqual(headers, build.NETLIFY_HEADERS)
        self.assertIn("/*\n  Cache-Control: public, max-age=300, stale-while-revalidate=86400", headers)
        for path in ("/feed.xml", "/sitemap.xml", "/robots.txt"):
            self.assertIn(path + "\n  Cache-Control: public, max-age=300, must-revalidate", headers)


if __name__ == "__main__":
    unittest.main()
