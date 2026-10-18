"""Leçon 1 : notre premier modèle de langage, à partir de comptages.

Aucune bibliothèque externe, aucun modèle préentraîné.
Exécution (Windows) : py lecon01.py
"""

from collections import Counter, defaultdict
from pathlib import Path
import json
import random

# 1. Charger le texte qui servira d'exemples au modèle.
dossier = Path(__file__).resolve().parent
texte = (dossier / "corpus.txt").read_text(encoding="utf-8").lower()
if len(texte) < 2:
    raise ValueError("Le corpus doit contenir au moins deux caractères.")

# 2. Apprendre combien de fois chaque caractère suit un autre caractère.
# Exemple : transitions["q"]["u"] vaut le nombre de séquences « qu ».
transitions = defaultdict(Counter)
for actuel, suivant in zip(texte, texte[1:]):
    transitions[actuel][suivant] += 1

# 3. Convertir les comptages en probabilités.
def probabilite(actuel: str, suivant: str) -> float:
    comptes = transitions[actuel]
    total = sum(comptes.values())
    return comptes[suivant] / total if total else 0.0

# 4. Générer du texte en tirant chaque nouveau caractère selon ces probabilités.
def generer(debut: str, longueur: int = 160, graine: int = 7) -> str:
    if not debut:
        raise ValueError("L'amorce ne doit pas être vide.")
    hasard = random.Random(graine)
    resultat = debut
    actuel = debut[-1]  # Notre modèle n'utilise QUE le dernier caractère.

    for _ in range(longueur):
        comptes = transitions.get(actuel)
        if not comptes:
            break
        caracteres = list(comptes.keys())
        frequences = list(comptes.values())
        suivant = hasard.choices(caracteres, weights=frequences, k=1)[0]
        resultat += suivant
        actuel = suivant

    return resultat

# 5. Sauvegarder ce que le modèle a appris (pas le corpus lui-même).
modele = {lettre: dict(comptes) for lettre, comptes in transitions.items()}
(dossier / "modele_bigram.json").write_text(
    json.dumps(modele, ensure_ascii=False, indent=2), encoding="utf-8"
)

print(f"Corpus : {len(texte)} caractères")
print(f"Vocabulaire : {len(set(texte))} caractères distincts")
print(f"P('u' après 'q') : {probabilite('q', 'u'):.1%}")
print(f"P('a' après 'q') : {probabilite('q', 'a'):.1%}")
print("\n--- Texte généré ---")
print(generer("le "))
print("\n--- Test de la limite du modèle ---")
print(generer("un chat", 75))
print(generer("un rat", 75))
print("\nModèle sauvegardé dans modele_bigram.json")
