import unittest
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

import build


def identities(notes, site):
    channel = ET.fromstring(build.render_feed(notes, site)).find('channel')
    return {item.findtext('guid'): item.findtext('pubDate') for item in channel.findall('item')}


class RssStabilityTest(unittest.TestCase):
    def test_inserting_and_reordering_notes_preserves_dates_and_guids(self):
        notes, site = build.load_notes(), build.load_site()
        before = identities(notes, site)
        for date in (notes[0]['date'], '2026-12-01'):
            new = dict(notes[0], slug='new-note', date=date)
            after = identities([new, *notes], site)
            self.assertEqual({guid: after[guid] for guid in before}, before)
        self.assertEqual(identities(list(reversed(notes)), site), before)
        for published in before.values():
            stamp = parsedate_to_datetime(published)
            self.assertEqual((stamp.hour, stamp.minute, stamp.second), (18, 0, 0))

    def test_same_day_items_keep_catalog_order(self):
        notes, site = build.load_notes(), build.load_site()
        notes = [dict(note, date='2026-11-05') for note in notes[:3]]
        channel = ET.fromstring(build.render_feed(notes, site)).find('channel')
        self.assertEqual([item.findtext('link') for item in channel.findall('item')],
                         [f"{site['url']}/{note['slug']}/" for note in notes])
