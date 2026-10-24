# Mini Language Model, from scratch

**Projet pédagogique | Python 3 · statistiques de langage · génération de texte**

Construire un modèle de langage *étape par étape*, sans poids préentraînés et sans dépendances externes. Le premier jalon est un modèle **bigramme de caractères** : il apprend à prédire le caractère suivant à partir d'un corpus en français.

> Il ne s'agit pas encore d'un réseau de neurones ni d'un grand modèle de langage. L'objectif est de comprendre les mécanismes avant d'implémenter un modèle plus avancé.

## Exécution

```bash
python lecon01.py
```

Le programme entraîne un modèle sur `corpus.txt`, affiche des prédictions probabilistes, génère quelques exemples et exporte ses paramètres appris dans `modele_bigram.json`.

**Prérequis :** Python 3.10+ ; bibliothèque standard uniquement. Travail et apprentissage prévus dans PyCharm.

## Fonctionnement

1. Lecture et normalisation du texte.
2. Comptage des transitions entre caractères adjacents.
3. Estimation de probabilités conditionnelles.
4. Génération par échantillonnage pseudo-aléatoire reproductible.
5. Export JSON du modèle entraîné.

## Leçon 02 : apprendre plutôt que compter

```bash
python lecon02.py
```

Cette deuxième leçon entraîne une petite matrice de scores par descente de
gradient, avec une fonction de perte (cross-entropy). Elle compare l'erreur
avant et après l'entraînement, génère du texte reproductible et exporte
`modele_bigram_entrainable.json`. Le programme n'utilise aucune dépendance
externe et se lance dans PyCharm comme la première leçon. Ce n'est pas encore
un réseau neuronal avec des embeddings ou de l'attention.

## Feuille de route

- [x] Leçon 01 : corpus, transitions et génération bigramme
- [x] Leçon 02 : paramètres entraînables, softmax, fonction de perte et descente de gradient
- [ ] Leçon 03 : gradient et optimisation
- [ ] Leçon 04 : embeddings et fenêtre de contexte
- [ ] Leçon 05 : mécanisme d'attention
- [ ] Leçon 06 : mini-Transformer autorégressif

## Intérêt technique

Démarche incrémentale, expérimentation reproductible, Python, statistiques, apprentissage automatique et communication pédagogique.
