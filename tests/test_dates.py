import copy
import unittest
from unittest.mock import patch

import build


class DateTest(unittest.TestCase):
    def test_dates_require_padding_and_a_calendar_date(self):
        for date in ('2026-9-5', '2026-09-5', '2026-9-05', '2026-02-29',
                     '2026-13-01', '2026-00-01', '2026-11-31', '２０２６-09-05'):
            with self.subTest(date=date), self.assertRaisesRegex(SystemExit, 'YYYY-MM-DD'):
                build.pretty_date(date)
        self.assertEqual(build.pretty_date('2024-02-29'), 'February 29, 2024')

    def test_catalog_rejects_non_padded_dates_before_sorting(self):
        catalog = copy.deepcopy(build.load_json(build.CONTENT / 'articles.json'))
        catalog[0]['date'] = '2026-9-5'
        with patch.object(build, 'load_json', return_value=catalog):
            with self.assertRaisesRegex(SystemExit, 'YYYY-MM-DD'):
                build.load_notes()

    def test_september_october_november_order_and_same_day_stability(self):
        catalog = copy.deepcopy(build.load_json(build.CONTENT / 'articles.json'))[:4]
        for entry, date in zip(catalog, ('2026-09-05', '2026-11-01', '2026-10-01', '2026-11-01')):
            entry['date'] = date
        with patch.object(build, 'load_json', return_value=catalog):
            notes = build.load_notes()
        self.assertEqual([n['slug'] for n in notes], [catalog[i]['slug'] for i in (1, 3, 2, 0)])
        self.assertIn('<lastmod>2026-11-01</lastmod>', build.render_sitemap(notes, build.load_site()))


class UpdatedFieldTest(unittest.TestCase):
    def catalog(self):
        return copy.deepcopy(build.load_json(build.CONTENT / 'articles.json'))

    def notes_with(self, **changes):
        catalog = self.catalog()
        # Last entry is the oldest article; give it an edit date.
        target = catalog[-1]
        target.update(changes)
        with patch.object(build, 'load_json', return_value=catalog):
            return build.load_notes(), target['slug']

    def test_shipped_catalog_has_no_updated_values(self):
        self.assertFalse([e for e in self.catalog() if e.get('updated')])
        notes = build.load_notes()
        self.assertTrue(all(n['updated'] == '' for n in notes))

    def test_without_updated_modified_date_equals_publication_date(self):
        site = build.load_site()
        notes = build.load_notes()
        for note in notes[:5]:
            self.assertEqual(build.article_posting(note, site)['dateModified'], note['date'])
            self.assertNotIn('>Updated ', build.article_bar(site, note, []))

    def test_updated_drives_lastmod_datemodified_and_visible_line(self):
        notes, slug = self.notes_with(updated='2026-11-15')
        note = next(n for n in notes if n['slug'] == slug)
        site = build.load_site()
        sitemap = build.render_sitemap(notes, site)
        self.assertIn(f'<loc>{site["url"]}/{slug}/</loc>\n    <lastmod>2026-11-15</lastmod>', sitemap)
        self.assertEqual(build.article_posting(note, site)['dateModified'], '2026-11-15')
        self.assertIn('Updated November 15, 2026', build.article_bar(site, note, []))
        built = build.render_article(note, site, notes)
        self.assertIn('"dateModified": "2026-11-15"', built.replace('":"', '": "'))

    def test_without_updated_every_lastmod_is_a_publication_date(self):
        import re
        notes = build.load_notes()
        sitemap = build.render_sitemap(notes, build.load_site())
        published = {n['date'] for n in notes}
        self.assertLessEqual(set(re.findall(r'<lastmod>([^<]+)</lastmod>', sitemap)), published)

    def test_invalid_or_earlier_updated_dates_fail_the_build(self):
        for value in ('2026-9-5', '2026-02-30', 'yesterday'):
            with self.subTest(value=value), self.assertRaisesRegex(SystemExit, 'YYYY-MM-DD'):
                self.notes_with(updated=value)
        with self.assertRaisesRegex(SystemExit, 'earlier than its publication date'):
            self.notes_with(updated='2000-01-01')
