import json
import math
import tempfile
import unittest
from pathlib import Path
from lecon02 import split_corpus, softmax, train, cross_entropy, generate, experiment

CORPUS = "\n".join([
    "le chat regarde la lune", "le chat dort dans le jardin", "le chien court", "la lune est grande",
    "le soleil se lève", "le vent souffle", "le robot apprend", "la machine apprend vite",
    "les oiseaux chantent", "la pluie tombe", "le ciel est bleu", "je regarde le ciel",
    "le chat aime le soleil", "la lumière traverse les arbres", "les fleurs sont belles"
])

class LessonTwoTests(unittest.TestCase):
    def test_split_is_deterministic_and_by_line(self):
        train, valid = split_corpus(CORPUS, seed=3)
        again = split_corpus(CORPUS, seed=3)
        self.assertEqual((train, valid), again)
        self.assertEqual(len(train) + len(valid), 15)
        self.assertFalse(set(train) & set(valid))

    def test_softmax_normalized_and_stable(self):
        p = softmax([1000, 1001, 999])
        self.assertAlmostEqual(sum(p), 1)
        self.assertTrue(all(0 < x < 1 for x in p))

    def test_loss_decreases_on_training_examples(self):
        examples = [(0, 1)] * 90 + [(0, 0)] * 10 + [(1, 0)] * 50
        matrix, history = train(examples, 2, epochs=80, learning_rate=0.5)
        self.assertLess(history[-1]["train_nll"], history[0]["train_nll"])
        self.assertLess(cross_entropy(matrix, examples), 0.5)

    def test_reproducible_generation(self):
        matrix = [[1, 2], [3, 4]]
        self.assertEqual(generate(matrix, ["a", "b"], "a", 20, seed=3),
                         generate(matrix, ["a", "b"], "a", 20, seed=3))
        self.assertRaises(ValueError, generate, matrix, ["a", "b"], "z")

    def test_experiment_reports_train_and_heldout(self):
        report, model = experiment(CORPUS, epochs=50, seed=2, length=20)
        self.assertTrue(math.isfinite(report["validation_nll"]))
        self.assertEqual(report["model"], "trainable_char_softmax_bigram")
        self.assertEqual(len(model["matrix"]), report["vocabulary"])
        self.assertLess(report["train_nll"], report["uniform_validation_nll"])
        self.assertGreater(report["validation_coverage"], 0.8)
        self.assertEqual(len(report["example"]), 21)

    def test_invalid_settings_rejected(self):
        self.assertRaises(ValueError, train, [(0, 1)], 2, 0, 1)
        self.assertRaises(ValueError, split_corpus, "only one line")

if __name__ == "__main__":
    unittest.main()
