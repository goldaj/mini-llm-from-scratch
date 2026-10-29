"""Leçon 02 : apprendre des paramètres numériques avec softmax et gradient.

Ce réseau n'a pas de couche cachée : un caractère est encodé en one-hot,
multiplié implicitement par une matrice W, puis normalisé par softmax.
Pas de modèle préentraîné, pas de bibliothèque externe.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path


def split_corpus(text: str, validation_ratio: float = 0.2, seed: int = 7):
    """Découpe par lignes avant de construire les paires pour limiter la fuite."""
    lines = [line.rstrip("\r") for line in text.lower().splitlines() if len(line.strip()) >= 2]
    if len(lines) < 5:
        raise ValueError("Le corpus doit avoir au moins cinq lignes de deux caractères")
    indices = list(range(len(lines)))
    random.Random(seed).shuffle(indices)
    valid_count = max(1, round(len(lines) * validation_ratio))
    valid = set(indices[:valid_count])
    train_lines = [line for i, line in enumerate(lines) if i not in valid]
    val_lines = [line for i, line in enumerate(lines) if i in valid]
    return train_lines, val_lines


def pairs(lines: list[str], index: dict[str, int]):
    return [(index[a], index[b]) for line in lines for a, b in zip(line, line[1:])]


def softmax(logits: list[float]) -> list[float]:
    peak = max(logits)
    weights = [math.exp(logit - peak) for logit in logits]
    total = sum(weights)
    return [w / total for w in weights]


def cross_entropy(matrix: list[list[float]], examples: list[tuple[int, int]]) -> float:
    if not examples:
        raise ValueError("No character pairs to evaluate")
    loss = 0.0
    for before, after in examples:
        probabilities = softmax(matrix[before])
        loss -= math.log(max(1e-15, probabilities[after]))
    return loss / len(examples)


def train(examples: list[tuple[int, int]], vocabulary_size: int, epochs: int = 200,
          learning_rate: float = 2.0, seed: int = 7):
    """Full-batch optimization of a trainable logit matrix (one-hot linear layer)."""
    if vocabulary_size < 2 or epochs <= 0 or learning_rate <= 0:
        raise ValueError("Invalid training settings")
    randomizer = random.Random(seed)
    matrix = [[randomizer.uniform(-0.01, 0.01) for _ in range(vocabulary_size)]
              for _ in range(vocabulary_size)]
    counts = [[0] * vocabulary_size for _ in range(vocabulary_size)]
    for a, b in examples:
        counts[a][b] += 1
    totals = [sum(row) for row in counts]
    history = []
    for epoch in range(epochs):
        for a in range(vocabulary_size):
            if not totals[a]:
                continue
            probabilities = softmax(matrix[a])
            # Gradient exact de la perte moyenne par ligne :
            # dL/dW[a][b] = p(b|a) - frequence_empirique(b|a)
            for b in range(vocabulary_size):
                gradient = probabilities[b] - counts[a][b] / totals[a]
                matrix[a][b] -= learning_rate * gradient
        if epoch == 0 or (epoch + 1) % max(1, epochs // 10) == 0 or epoch == epochs - 1:
            history.append({"epoch": epoch + 1, "train_nll": round(cross_entropy(matrix, examples), 6)})
    return matrix, history


def generate(matrix: list[list[float]], characters: list[str], prefix: str,
             length: int = 160, temperature: float = 1.0, seed: int = 7) -> str:
    if not prefix or length < 0 or not (0 < temperature <= 5):
        raise ValueError("Amorce, longueur ou température invalides")
    index = {character: number for number, character in enumerate(characters)}
    if prefix[-1] not in index:
        raise ValueError("Le dernier caractère de l'amorce est absent du corpus")
    rng = random.Random(seed)
    output = prefix
    for _ in range(length):
        probabilities = softmax([v / temperature for v in matrix[index[output[-1]]]])
        char = rng.choices(characters, weights=probabilities, k=1)[0]
        output += char
    return output


def experiment(text: str, epochs: int = 200, learning_rate: float = 2.0,
               seed: int = 7, length: int = 100):
    train_lines, val_lines = split_corpus(text, seed=seed)
    # Le vocabulaire est établi sur les lignes d'entraînement uniquement.
    chars = sorted(set("".join(train_lines)))
    index = {char: i for i, char in enumerate(chars)}
    train_pairs = pairs(train_lines, index)
    # Exclure les caractères réellement inobservés de l'évaluation,
    # en signalant explicitement les paires non évaluables.
    heldout = [(a, b) for line in val_lines for a, b in zip(line, line[1:])]
    val_pairs = [(index[a], index[b]) for a, b in heldout if a in index and b in index]
    if not train_pairs or not val_pairs:
        raise ValueError("Pas assez de transitions d'entraînement/validation connues")
    matrix, history = train(train_pairs, len(chars), epochs, learning_rate, seed)
    train_nll = cross_entropy(matrix, train_pairs)
    val_nll = cross_entropy(matrix, val_pairs)
    baseline_nll = math.log(len(chars))  # Modèle uniforme, non entraîné.
    root = chars[0]
    samples = generate(matrix, chars, root, length=length, seed=seed)
    report = {
        "model": "trainable_char_softmax_bigram",
        "vocabulary": len(chars),
        "train_pairs": len(train_pairs),
        "validation_pairs": len(val_pairs),
        "validation_coverage": round(len(val_pairs) / len(heldout), 4),
        "epochs": epochs,
        "learning_rate": learning_rate,
        "train_nll": round(train_nll, 6),
        "validation_nll": round(val_nll, 6),
        "uniform_validation_nll": round(baseline_nll, 6),
        "validation_perplexity": round(math.exp(val_nll), 4),
        "history": history,
        "example": samples,
    }
    model = {"format_version": 1, "vocab": chars, "matrix": matrix,
             "training": {"epochs": epochs, "learning_rate": learning_rate, "seed": seed}}
    return report, model


def main(argv=None):
    parser = argparse.ArgumentParser(description="Leçon 02 — optimisation d'un softmax bigramme")
    parser.add_argument("--corpus", type=Path, default=Path(__file__).parent / "corpus.txt")
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--learning-rate", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--length", type=int, default=100)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "modele_softmax.json")
    args = parser.parse_args(argv)
    if args.epochs < 1 or args.epochs > 10000 or not math.isfinite(args.learning_rate) or not 0 < args.learning_rate <= 5 or not 0 <= args.length <= 10000:
        parser.error("epochs (1..10000), learning rate (0..5] or length (0..10000) invalid")
    text = args.corpus.read_text(encoding="utf-8")
    report, model = experiment(text, args.epochs, args.learning_rate, args.seed, args.length)
    args.output.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Modèle sauvegardé :", args.output)


if __name__ == "__main__":
    main()
