"""Balance and determinism of the auto-generated "Related notes" links (IMN-002).

Each article links to 3 others, so the average inbound count is 3. The bound
below (twice the average) is deliberately generous: it forbids runaway hubs
without forcing irrelevant links.
"""
import unittest
from collections import Counter

import build

LINKS_PER_NOTE = 3
MAX_INBOUND = 6  # 2 x the average of LINKS_PER_NOTE


def inbound_counts(notes):
    counts = Counter({note["slug"]: 0 for note in notes})
    for note in notes:
        for target in build.rank_related_notes(note, notes)["notes"]:
            counts[target["slug"]] += 1
    return counts


class RelatedLinkBalanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notes = build.load_notes()

    def test_every_article_receives_at_least_one_related_link(self):
        counts = inbound_counts(self.notes)
        orphans = sorted(slug for slug, count in counts.items() if count == 0)
        self.assertEqual(orphans, [])

    def test_inbound_related_links_stay_within_bound(self):
        counts = inbound_counts(self.notes)
        worst = counts.most_common(1)[0]
        self.assertLessEqual(worst[1], MAX_INBOUND, worst)

    def test_each_article_gets_three_distinct_non_self_links(self):
        for note in self.notes:
            slugs = [n["slug"] for n in build.rank_related_notes(note, self.notes)["notes"]]
            self.assertEqual(len(slugs), LINKS_PER_NOTE, note["slug"])
            self.assertEqual(len(set(slugs)), LINKS_PER_NOTE, note["slug"])
            self.assertNotIn(note["slug"], slugs)

    def test_result_is_deterministic_and_independent_of_call_order(self):
        forward = {n["slug"]: [r["slug"] for r in build.rank_related_notes(n, self.notes)["notes"]] for n in self.notes}
        again = {n["slug"]: [r["slug"] for r in build.rank_related_notes(n, self.notes)["notes"]] for n in self.notes}
        backward = {}
        for n in reversed(self.notes):
            backward[n["slug"]] = [r["slug"] for r in build.rank_related_notes(n, self.notes)["notes"]]
        self.assertEqual(forward, again)
        self.assertEqual(forward, backward)

    def test_rendered_pages_contain_the_ranked_links(self):
        for note in self.notes[:5]:
            html = build.render_related_notes(note, self.notes)
            for target in build.rank_related_notes(note, self.notes)["notes"]:
                self.assertIn(f'href="../{target["slug"]}/"', html)


if __name__ == "__main__":
    unittest.main()
