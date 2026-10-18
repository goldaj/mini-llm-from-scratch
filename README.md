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

## Feuille de route

- [x] Leçon 01 : corpus, transitions et génération bigramme
- [ ] Leçon 02 : paramètre entraînable et fonction de perte
- [ ] Leçon 03 : gradient et optimisation
- [ ] Leçon 04 : embeddings et fenêtre de contexte
- [ ] Leçon 05 : mécanisme d'attention
- [ ] Leçon 06 : mini-Transformer autorégressif

## Intérêt technique

Démarche incrémentale, expérimentation reproductible, Python, statistiques, apprentissage automatique et communication pédagogique.
