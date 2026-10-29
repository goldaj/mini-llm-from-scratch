"""Leçon 03: causal context, numerical gradients and behaviour (stdlib only)."""
import math
import unittest

from lecon03 import BOS, EOS, CharMLP, examples_for_lines, experiment, generate

CORPUS = "\n".join([
    "le chat regarde la lune", "le chat dort dans le jardin", "le chien court",
    "la lune est grande", "le soleil se lève", "le vent souffle",
    "le robot apprend", "la machine apprend vite", "les oiseaux chantent",
    "la pluie tombe", "le ciel est bleu", "je regarde le ciel",
    "le chat aime le soleil", "la lumière traverse les arbres", "les fleurs sont belles",
])


class LessonThreeTests(unittest.TestCase):
    def test_context_does_not_see_future_chars(self):
        tokens = [BOS, EOS, "a", "b", "c"]
        index = {token: n for n, token in enumerate(tokens)}
        first, attempted = examples_for_lines(["ab"], index, 3)
        self.assertEqual(attempted, 3)
        self.assertEqual(first[0], ((0, 0, 0), 2))
        self.assertEqual(first[1], ((0, 0, 2), 3))
        self.assertEqual(first[2], ((0, 2, 3), 1))
        known, attempted = examples_for_lines(["acz"], index, 3)
        self.assertEqual((len(known), attempted), (2, 4))

    def test_gradient_finite_difference_for_all_layers(self):
        model = CharMLP.new([BOS, EOS, "a", "b"], 2, 2, 3, seed=4)
        context, target = (0, 2), 3
        gradients = model.gradients(context, target)
        eps = 1e-6
        checks = [
            (model.embedding[0], 1, gradients["embedding"][1]),
            (model.embedding[2], 0, gradients["embedding"][2]),
            (model.w1[1], 2, gradients["w1"][1][2]),
            (model.b1, 0, gradients["b1"][0]),
            (model.w2[2], 3, gradients["w2"][2][3]),
            (model.b2, 3, gradients["b2"][3]),
        ]
        for values, idx, expected in checks:
            old = values[idx]
            values[idx] = old + eps
            plus = model.loss(context, target)
            values[idx] = old - eps
            minus = model.loss(context, target)
            values[idx] = old
            self.assertAlmostEqual((plus - minus) / (2 * eps), expected, delta=1e-8)

    def test_training_reduces_loss_and_compares_to_baselines(self):
        report, payload = experiment(CORPUS, epochs=10, seed=7, length=25)
        self.assertEqual(report["model"], "char_context_embedding_mlp")
        self.assertLess(report["training_nll"], report["initial_training_nll"])
        self.assertGreater(report["validation_examples"], 0)
        self.assertLessEqual(report["validation_coverage"], 1)
        self.assertTrue(math.isfinite(report["validation_perplexity"]))
        self.assertEqual(report["parameters"], 733)
        self.assertEqual(payload["format_version"], 1)
        self.assertEqual(len(payload["embedding"]), report["vocabulary"])
        self.assertEqual(report, experiment(CORPUS, epochs=10, seed=7, length=25)[0])

    def test_generate_is_reproducible_and_no_bos(self):
        model = CharMLP.new([BOS, EOS, "a", "b"], 2, 2, 4, seed=5)
        result = generate(model, length=20, seed=10)
        self.assertEqual(result, generate(model, length=20, seed=10))
        self.assertNotIn(BOS, result)
        with self.assertRaises(ValueError):
            generate(model, length=-1, seed=1)

    def test_rejects_invalid_network_shapes(self):
        with self.assertRaises(ValueError):
            CharMLP.new([BOS, EOS], 3, 4, 16, 7)
        with self.assertRaises(ValueError):
            experiment(CORPUS, epochs=0)
        with self.assertRaises(ValueError):
            experiment(CORPUS, learning_rate=float("nan"))


if __name__ == "__main__":
    unittest.main()
