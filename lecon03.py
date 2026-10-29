"""Leçon 03 : embeddings + contexte de trois caractères, MLP manuel.

Aucun modèle externe et aucune bibliothèque tierce : chaque dérivée est explicite.
Utiliser PyCharm ou : python lecon03.py --epochs 15
"""
from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path

from lecon02 import split_corpus

BOS, EOS = "<BOS>", "<EOS>"


def examples_for_lines(lines: list[str], index: dict[str, int], context: int):
    examples = []
    attempted = 0
    for line in lines:
        sequence = [BOS] * context + list(line) + [EOS]
        for position in range(context, len(sequence)):
            attempted += 1
            window = sequence[position - context:position + 1]
            if all(token in index for token in window):
                examples.append((tuple(index[token] for token in window[:-1]), index[window[-1]]))
    return examples, attempted


@dataclass
class CharMLP:
    vocab: list[str]
    context: int
    dim: int
    hidden: int
    embedding: list[list[float]]
    w1: list[list[float]]
    b1: list[float]
    w2: list[list[float]]
    b2: list[float]

    @classmethod
    def new(cls, vocab: list[str], context: int, dim: int, hidden: int, seed: int):
        if len(vocab) < 4 or not 1 <= context <= 5 or not 1 <= dim <= 16 or not 1 <= hidden <= 64:
            raise ValueError("Invalid vocabulary or network shape")
        rnd = random.Random(seed)
        def matrix(rows, cols):
            return [[rnd.uniform(-0.1, 0.1) for _ in range(cols)] for _ in range(rows)]
        return cls(vocab, context, dim, hidden, matrix(len(vocab), dim),
                   matrix(context * dim, hidden), [0.0] * hidden,
                   matrix(hidden, len(vocab)), [0.0] * len(vocab))

    def forward(self, sequence: tuple[int, ...]):
        if len(sequence) != self.context or any(not 0 <= token < len(self.vocab) for token in sequence):
            raise ValueError("Invalid context window")
        x = [value for token in sequence for value in self.embedding[token]]
        hidden_values = [math.tanh(self.b1[j] + sum(x[i] * self.w1[i][j]
                         for i in range(len(x)))) for j in range(self.hidden)]
        logits = [self.b2[k] + sum(hidden_values[j] * self.w2[j][k]
                  for j in range(self.hidden)) for k in range(len(self.vocab))]
        peak = max(logits)
        exp_values = [math.exp(v - peak) for v in logits]
        total = sum(exp_values)
        return x, hidden_values, [v / total for v in exp_values]

    def loss(self, sequence: tuple[int, ...], target: int) -> float:
        return -math.log(max(1e-300, self.forward(sequence)[2][target]))

    def gradients(self, sequence: tuple[int, ...], target: int):
        """Exact chain rule: dL/dlogits = softmax - one_hot(target)."""
        x, h, prob = self.forward(sequence)
        delta_out = prob.copy()
        delta_out[target] -= 1.0
        delta_hidden = [(1 - h[j] * h[j]) * sum(self.w2[j][k] * delta_out[k]
                        for k in range(len(self.vocab))) for j in range(self.hidden)]
        delta_x = [sum(self.w1[i][j] * delta_hidden[j] for j in range(self.hidden))
                   for i in range(len(x))]
        return {
            "embedding": delta_x,
            "w1": [[x[i] * delta_hidden[j] for j in range(self.hidden)] for i in range(len(x))],
            "b1": delta_hidden,
            "w2": [[h[j] * delta_out[k] for k in range(len(self.vocab))] for j in range(self.hidden)],
            "b2": delta_out,
        }

    def step(self, sequence: tuple[int, ...], target: int, learning_rate: float):
        grads = self.gradients(sequence, target)
        for position, token in enumerate(sequence):
            for d in range(self.dim):
                # Repeated tokens accumulate gradients across their positions.
                self.embedding[token][d] -= learning_rate * grads["embedding"][position * self.dim + d]
        for i in range(self.context * self.dim):
            for j in range(self.hidden):
                self.w1[i][j] -= learning_rate * grads["w1"][i][j]
        for j in range(self.hidden):
            self.b1[j] -= learning_rate * grads["b1"][j]
            for k in range(len(self.vocab)):
                self.w2[j][k] -= learning_rate * grads["w2"][j][k]
        for k in range(len(self.vocab)):
            self.b2[k] -= learning_rate * grads["b2"][k]

    def parameters(self) -> int:
        return (len(self.vocab) * self.dim + self.context * self.dim * self.hidden
                + self.hidden + self.hidden * len(self.vocab) + len(self.vocab))

    def export(self):
        return {"format_version": 1, "architecture": "character_embedding_tanh_mlp",
                "vocab": self.vocab, "context": self.context, "dim": self.dim,
                "hidden": self.hidden, "embedding": self.embedding, "w1": self.w1,
                "b1": self.b1, "w2": self.w2, "b2": self.b2}


def mean_nll(model: CharMLP, data) -> float:
    if not data:
        raise ValueError("No evaluable examples")
    return sum(model.loss(x, y) for x, y in data) / len(data)


def baselines(training, validation, vocab_size: int):
    """Same validation samples for count-bigram and unigram, Laplace alpha=1."""
    unigrams = [1] * vocab_size
    bigrams = [[1] * vocab_size for _ in range(vocab_size)]
    for context, target in training:
        unigrams[target] += 1
        bigrams[context[-1]][target] += 1
    total = sum(unigrams)
    totals = [sum(row) for row in bigrams]
    uni = sum(-math.log(unigrams[y] / total) for _, y in validation) / len(validation)
    bi = sum(-math.log(bigrams[x[-1]][y] / totals[x[-1]])
             for x, y in validation) / len(validation)
    return uni, bi


def generate(model: CharMLP, length: int, seed: int) -> str:
    if not 0 <= length <= 10000:
        raise ValueError("Invalid generation length")
    rnd = random.Random(seed)
    context = [0] * model.context  # BOS index 0, reserved by experiment()
    output = []
    for _ in range(length):
        probabilities = model.forward(tuple(context))[2]
        probabilities[0] = 0.0  # Never generate BOS (context-only marker).
        selected = rnd.choices(range(len(model.vocab)), weights=probabilities, k=1)[0]
        if model.vocab[selected] == EOS:
            break
        output.append(model.vocab[selected])
        context = context[1:] + [selected]
    return "".join(output)


def experiment(text: str, *, context=3, dim=4, hidden=16, epochs=15,
               learning_rate=0.05, seed=7, length=100):
    if type(epochs) is not int or not 1 <= epochs <= 300 or not math.isfinite(learning_rate) or not 0 < learning_rate <= 1:
        raise ValueError("Invalid training settings")
    train_lines, val_lines = split_corpus(text, seed=seed)
    vocab = [BOS, EOS] + sorted(set("".join(train_lines)))
    index = {token: i for i, token in enumerate(vocab)}
    train_data, _ = examples_for_lines(train_lines, index, context)
    val_data, attempted = examples_for_lines(val_lines, index, context)
    if not train_data or not val_data:
        raise ValueError("No known train or validation contexts")
    model = CharMLP.new(vocab, context, dim, hidden, seed)
    initial = mean_nll(model, train_data)
    rng = random.Random(seed + 1)
    history = []
    for epoch in range(epochs):
        shuffled = train_data.copy()
        rng.shuffle(shuffled)
        for sequence, target in shuffled:
            model.step(sequence, target, learning_rate)
        history.append({"epoch": epoch + 1, "train_nll": round(mean_nll(model, train_data), 6)})
    training_nll = mean_nll(model, train_data)
    validation_nll = mean_nll(model, val_data)
    uni, bi = baselines(train_data, val_data, len(vocab))
    report = {
        "model": "char_context_embedding_mlp", "parameters": model.parameters(),
        "vocabulary": len(vocab), "context": context, "embedding_dim": dim,
        "hidden_units": hidden, "epochs": epochs, "learning_rate": learning_rate,
        "training_examples": len(train_data), "validation_examples": len(val_data),
        "validation_coverage": round(len(val_data) / attempted, 4),
        "initial_training_nll": round(initial, 6),
        "training_nll": round(training_nll, 6),
        "validation_nll": round(validation_nll, 6),
        "validation_perplexity": round(math.exp(validation_nll), 4),
        "unigram_validation_nll": round(uni, 6),
        "bigram_validation_nll": round(bi, 6),
        "beats_bigram_on_validation": validation_nll < bi,
        "history": history,
        "sample": generate(model, length, seed),
    }
    return report, model.export()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Leçon 03 — embeddings et contexte causal, MLP pur Python")
    parser.add_argument("--corpus", type=Path, default=Path(__file__).parent / "corpus.txt")
    parser.add_argument("--context", type=int, default=3)
    parser.add_argument("--dim", type=int, default=4)
    parser.add_argument("--hidden", type=int, default=16)
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--learning-rate", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--length", type=int, default=100)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "modele_context_mlp.json")
    args = parser.parse_args(argv)
    if not 0 <= args.length <= 10000:
        parser.error("length must be in [0, 10000]")
    report, model = experiment(args.corpus.read_text(encoding="utf-8"), context=args.context,
                               dim=args.dim, hidden=args.hidden, epochs=args.epochs,
                               learning_rate=args.learning_rate, seed=args.seed, length=args.length)
    args.output.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Modèle sauvegardé :", args.output)


if __name__ == "__main__":
    main()
