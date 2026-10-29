"""Leçon 02 — apprendre des paramètres par descente de gradient.

Chaque ligne de poids prédit le caractère suivant. Rien de pré-entraîné :
le modèle apprend uniquement à partir de corpus.txt. Bibliothèque standard.
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path


def corpus_pairs(text: str):
    """Construit le vocabulaire et la matrice des transitions observées."""
    if len(text) < 2:
        raise ValueError("Au moins deux caractères sont nécessaires.")
    alphabet = sorted(set(text))
    index = {letter: i for i, letter in enumerate(alphabet)}
    counts = [[0] * len(alphabet) for _ in alphabet]
    for current, following in zip(text, text[1:]):
        counts[index[current]][index[following]] += 1
    return alphabet, counts


def softmax(logits: list[float]) -> list[float]:
    """Convertit les scores non normalisés en probabilités stables."""
    offset = max(logits)
    exp_values = [math.exp(value - offset) for value in logits]
    denominator = sum(exp_values)
    return [value / denominator for value in exp_values]


def negative_log_likelihood(logits: list[list[float]], counts: list[list[int]]) -> float:
    """Erreur moyenne : plus elle est faible, mieux le modèle prédit."""
    total = sum(sum(row) for row in counts)
    if total == 0:
        raise ValueError("Aucune transition à entraîner.")
    return -sum(
        count * math.log(max(probability, 1e-300))
        for scores, row in zip(logits, counts)
        for probability, count in zip(softmax(scores), row)
        if count
    ) / total


def train(text: str, epochs: int = 120, learning_rate: float = 0.7):
    """Gradient de la cross-entropy pour chaque caractère précédent.

    Le taux est normalisé par ligne. Les lignes sans transitions restent neutres.
    """
    if epochs < 0 or not 0 < learning_rate <= 1:
        raise ValueError("epochs >= 0 et 0 < learning_rate <= 1 attendus.")
    alphabet, counts = corpus_pairs(text)
    size = len(alphabet)
    logits = [[0.0] * size for _ in range(size)]
    initial_loss = negative_log_likelihood(logits, counts)

    for _ in range(epochs):
        for row_index, row in enumerate(counts):
            sample_count = sum(row)
            if not sample_count:
                continue
            probabilities = softmax(logits[row_index])
            for next_index, count in enumerate(row):
                # dérivée = probabilité prédite - fréquence observée
                gradient = probabilities[next_index] - count / sample_count
                logits[row_index][next_index] -= learning_rate * gradient

    return alphabet, logits, initial_loss, negative_log_likelihood(logits, counts)


def generate(alphabet: list[str], logits: list[list[float]], start: str,
             length: int = 120, seed: int = 7) -> str:
    if not start or start[-1] not in alphabet:
        raise ValueError("L'amorce doit finir par un caractère du vocabulaire.")
    if length < 0:
        raise ValueError("La longueur demandée doit être positive ou nulle.")
    lookup = {letter: i for i, letter in enumerate(alphabet)}
    rng = random.Random(seed)
    output = start
    for _ in range(length):
        distribution = softmax(logits[lookup[output[-1]]])
        next_letter = rng.choices(alphabet, weights=distribution, k=1)[0]
        output += next_letter
    return output


def main():
    root = Path(__file__).resolve().parent
    text = (root / "corpus.txt").read_text(encoding="utf-8").lower()
    alphabet, logits, before, after = train(text)
    print(f"Vocabulaire : {len(alphabet)} caractères")
    print(f"Erreur avant entraînement : {before:.4f}")
    print(f"Erreur après entraînement : {after:.4f}")
    print("Texte généré :")
    print(generate(alphabet, logits, "le ", seed=7))
    destination = root / "modele_bigram_entrainable.json"
    destination.write_text(
        json.dumps({"alphabet": alphabet, "logits": logits}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Paramètres enregistrés : {destination.name}")


if __name__ == "__main__":
    main()
