"""Tests pédagogiques sans modifier les modèles exportés."""
from __future__ import annotations

import json
import runpy
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "lecon01.py"


class BigramTests(unittest.TestCase):
    def load(self):
        with patch("pathlib.Path.write_text", return_value=0), patch("builtins.print"):
            return runpy.run_path(str(SCRIPT), run_name="bigram_test")

    def test_unseen_character_does_not_change_training_counts(self):
        scope = self.load()
        transitions = scope["transitions"]
        before = len(transitions)
        self.assertEqual(scope["probabilite"]("\0", "a"), 0.0)
        self.assertEqual(len(transitions), before)

    def test_probability_mass_and_reproducible_sampling(self):
        scope = self.load()
        counts = scope["transitions"]["q"]
        self.assertAlmostEqual(sum(scope["probabilite"]("q", char) for char in counts), 1.0)
        self.assertEqual(scope["generer"]("le ", longueur=20, graine=3),
                         scope["generer"]("le ", longueur=20, graine=3))
        with self.assertRaises(ValueError):
            scope["generer"]("le ", longueur=-1)


if __name__ == "__main__":
    unittest.main()
