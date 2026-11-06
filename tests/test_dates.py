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
