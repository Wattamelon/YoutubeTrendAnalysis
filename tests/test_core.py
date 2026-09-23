"""Tests for deterministic core logic without API or database access."""

import unittest

from src.preprocessing import clean_comment
from src.ranking import aggregate_scores, compare_rankings
from src.related_keywords import related_keywords


class CoreModuleTests(unittest.TestCase):
    def test_clean_comment_normalizes_aliases_and_removes_urls(self):
        self.assertEqual(
            clean_comment("<b>BTS</b> https://example.com", "Music"),
            "방탄소년단",
        )

    def test_ranking_and_movement(self):
        ranking = aggregate_scores(
            [
                {"combined_score": {"BTS": 3, "music": 1}},
                {"combined_score": {"BTS": 2}},
            ]
        )
        self.assertEqual(ranking[0], {"keyword": "BTS", "score": 5.0})

        movement = compare_rankings(
            ranking,
            [{"keyword": "music"}, {"keyword": "BTS"}],
        )
        self.assertEqual(movement[0]["movement"], "rising")

    def test_related_keywords_uses_video_level_cooccurrence(self):
        related = related_keywords(
            "A",
            [["A", "B", "C", "D", "E"], ["A", "B", "C", "D", "E"]],
            min_cooccurrence=2,
        )
        self.assertEqual(related[0]["keyword"], "B")


if __name__ == "__main__":
    unittest.main()
