"""Leçon 02 : aucun téléchargement, aucune GPU, aucun modèle externe."""
import math
import unittest

from lecon02 import corpus_pairs, softmax, train, generate, negative_log_likelihood


class TrainableBigramTests(unittest.TestCase):
    def test_probabilities_sum_to_one_even_with_extreme_logits(self):
        probabilities = softmax([500.0, 501.0, -200.0])
        self.assertAlmostEqual(sum(probabilities), 1.0)
        self.assertTrue(all(math.isfinite(x) for x in probabilities))

    def test_training_reduces_error_on_simple_corpus(self):
        vocab, logits, before, after = train("abababababababababab", epochs=100)
        self.assertLess(after, before * 0.3)
        self.assertEqual(vocab, ["a", "b"])
        output = generate(vocab, logits, "a", length=20, seed=7)
        self.assertEqual(output, "ababababababababababa")
        self.assertEqual(output, generate(vocab, logits, "a", length=20, seed=7))

    def test_error_guards(self):
        with self.assertRaises(ValueError):
            corpus_pairs("x")
        with self.assertRaises(ValueError):
            train("ab", epochs=-1)
        with self.assertRaises(ValueError):
            train("ab", learning_rate=0)
        with self.assertRaises(ValueError):
            generate(["a"], [[1.0]], "z")
        with self.assertRaises(ValueError):
            generate(["a"], [[1.0]], "a", -1)


if __name__ == "__main__":
    unittest.main()
