"""
Unit tests for the heuristic engine.
Run via terminal: python -m unittest tests/test_heuristics.py
"""

import unittest
from core.heuristics import guess_availability, mentions_any


class TestHeuristics(unittest.TestCase):

    def test_pre_1928_public_domain(self):
        result = guess_availability("movies", "Metropolis 1927")
        self.assertGreater(result["free"], result["paid"])
        self.assertTrue(any("Older than 1928" in r for r in result["reasons"]))

    def test_recent_media_paid_bias(self):
        result = guess_availability("shows", "Severance 2022")
        self.assertGreater(result["paid"], result["free"])
        self.assertTrue(any("Fairly recent" in r for r in result["reasons"]))

    def test_classic_author_boost(self):
        result = guess_availability("books", "Pride and Prejudice by Austen")
        self.assertGreaterEqual(result["free"], 85)
        self.assertTrue(any("classic author" in r for r in result["reasons"]))

    def test_classical_music_boost(self):
        result = guess_availability("music", "Beethoven Symphony No. 5")
        self.assertTrue(any("Classical music" in r for r in result["reasons"]))

    def test_mentions_any(self):
        self.assertTrue(mentions_any("a silent movie", ("noir", "silent")))
        self.assertFalse(mentions_any("modern action film", ("noir", "silent")))


if __name__ == "__main__":
    unittest.main()