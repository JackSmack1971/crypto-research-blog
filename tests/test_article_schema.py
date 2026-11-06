import json
import unittest

import build


def schemas(html):
    return [json.loads(match.group(2)) for match in build.LD_JSON_RE.finditer(html)]


class ArticleSchemaTest(unittest.TestCase):
    def setUp(self):
        self.note = next(n for n in build.load_notes() if n['slug'] == 'bitcoin-open-interest-filter-test')
        self.site = build.load_site()

    def test_existing_featured_posting_is_augmented_without_duplicate(self):
        original = build.existing_blog_postings(self.note['html'], self.note['slug'])[0]
        rendered = build.render_article(self.note, self.site)
        posts = [p for data in schemas(rendered) for p in build.blog_postings(data)]
        self.assertEqual(len(posts), 1)
        post = posts[0]
        for key, value in original.items():
            self.assertEqual(post[key], value, key)
        url = f"{self.site['url']}/{self.note['slug']}/"
        self.assertEqual(post['url'], url)
        self.assertEqual(post['mainEntityOfPage'], url)
        self.assertEqual(post['image'], self.site['url'] + '/' + self.note['image']['path'])
        self.assertTrue(post['author']['name'])
        self.assertTrue(post['publisher']['name'])

    def with_schema(self, data):
        html = build.LD_JSON_RE.sub('', self.note['html'])
        html = html.replace('</head>', build.json_ld(data) + '</head>')
        return dict(self.note, html=html)

    def test_graph_and_list_forms_preserve_other_entities_and_author(self):
        post = {'@type': ['BlogPosting', 'Article'], 'author': {'@type': 'Person', 'name': 'Original author'}}
        other = {'@type': 'Organization', 'name': 'Independent entity'}
        for data in ([post, other], {'@context': 'https://schema.org', '@graph': [post, other]}):
            note = self.with_schema(data)
            result = schemas(build.render_article(note, self.site))
            posts = [p for d in result for p in build.blog_postings(d)]
            self.assertEqual(len(posts), 1)
            self.assertEqual(posts[0]['author'], post['author'])
            self.assertIn('Independent entity', json.dumps(result))
            self.assertIn('image', posts[0])

    def test_unrelated_schema_does_not_suppress_article_posting(self):
        note = self.with_schema({'@type': 'BreadcrumbList', 'itemListElement': []})
        result = schemas(build.render_article(note, self.site))
        self.assertEqual(len(result), 2)
        self.assertEqual(len([p for d in result for p in build.blog_postings(d)]), 1)

    def test_ambiguous_or_malformed_schema_fails(self):
        note = self.with_schema([{'@type': 'BlogPosting'}, {'@type': 'BlogPosting'}])
        with self.assertRaisesRegex(SystemExit, 'multiple BlogPosting'):
            build.render_article(note, self.site)
        note = dict(self.note, html=build.LD_JSON_RE.sub('<script type="application/ld+json">{bad}</script>', self.note['html']))
        with self.assertRaisesRegex(SystemExit, 'invalid JSON-LD'):
            build.render_article(note, self.site)
