"""Shared reading navigation and homepage hierarchy preserve editorial authority."""
from html.parser import HTMLParser
import re
import unittest

import build


class Elements(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.items = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.items.append((tag, dict(attrs)))


class EditorialDesignTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notes = build.load_notes()
        cls.site = build.load_site()

    def test_outline_preserves_source_markup_and_avoids_id_collisions(self):
        source = ('<body><div id="cr-section-2"></div>'
                  '<h2 id="original">Facts &amp; <em>limits</em></h2>'
                  '<h2 class="sources">Sources</h2>'
                  '<script>const template = "<h2>Not a section</h2>";</script></body>')
        html, outline = build.article_outline(source)
        self.assertEqual(outline, [('original', 'Facts & limits'), ('cr-section-2-section', 'Sources')])
        self.assertEqual(html.replace(' id="cr-section-2-section"', ''), source)
        self.assertEqual(build.article_outline(html), (html, outline))

    def test_every_section_guide_target_exists_once(self):
        for note in self.notes:
            with self.subTest(slug=note['slug']):
                html, outline = build.article_outline(note['html'])
                elements = Elements(html).items
                ids = [attrs.get('id') for _, attrs in elements if attrs.get('id')]
                headings = [attrs.get('id') for tag, attrs in elements if tag == 'h2']
                self.assertTrue(outline)
                self.assertEqual([target for target, _ in outline], headings)
                for target, _ in outline:
                    self.assertEqual(ids.count(target), 1)
                # Undo precisely the new heading attributes; the rest is byte-for-byte source.
                source_ids = {attrs.get('id') for _, attrs in Elements(note['html']).items}
                for target, _ in outline:
                    if target not in source_ids:
                        html = html.replace(f' id="{target}"', '', 1)
                self.assertEqual(html, note['html'])

    def test_article_body_attributes_survive_shared_scope(self):
        note = dict(self.notes[0])
        note['html'] = re.sub(r'<body\b[^>]*>', "<body class='essay' data-view='reading'>", note['html'], count=1)
        rendered = build.render_article(note, self.site, self.notes)
        body = next(attrs for tag, attrs in Elements(rendered).items if tag == 'body')
        self.assertEqual(body['class'].split(), ['cr-article', 'essay'])
        self.assertEqual(body['data-view'], 'reading')
        self.assertIn('href="../#notes"', rendered)

    def test_latest_research_follows_chronology_independently_of_feature(self):
        site = dict(self.site, featured_slug=self.notes[-1]['slug'])
        home = build.render_home(self.notes, site)
        latest = re.search(r'<section class="latest wrap".*?</section>', home, re.S).group()
        self.assertEqual(re.findall(r'data-latest-slug="([^"]+)"', latest),
                         [note['slug'] for note in self.notes[:3]])
        feature = re.search(r'<section class="feature wrap".*?</section>', home, re.S).group()
        self.assertIn(self.notes[-1]['title'], build.visible_text(feature))
        self.assertIn('id="methodology"', home)

    def test_one_article_still_has_feature_latest_and_working_archive(self):
        note = self.notes[0]
        home = build.render_home([note], dict(self.site, featured_slug=note['slug']))
        self.assertIn(f'data-latest-slug="{note["slug"]}"', home)
        self.assertIn('1 investigation', home)
        self.assertNotIn('class="entry"', home)


if __name__ == '__main__':
    unittest.main()
