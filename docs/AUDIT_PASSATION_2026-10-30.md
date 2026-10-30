# Audit indépendant branches et passation — goldaj/mini-llm-from-scratch

2026-10-30. GitHub inspecté (refs/PR/README/AGENTS). Ni entraînement de modèle ni test local effectué.

## Branches
`main`: `1c745906c169c24da80b124aa550a8c1e786b7ab`.
- `chatgpt/review-20261024` — `behind`, 0 commits exclusifs / 14 derrière. Historique intégré, nettoyage conditionnel des références.
- `feat/lesson02-trainable-softmax-20261029` — `behind`, 0 commits exclusifs / 20 derrière. Historique intégré, nettoyage conditionnel des références.
- `feat/lesson03-context-embeddings-20261029` — `behind`, 0 commits exclusifs / 1 derrière. Historique intégré, nettoyage conditionnel des références.

## PR
- [#3](https://github.com/goldaj/mini-llm-from-scratch/pull/3) : closed, fusionnée ; feat: lesson 03 causal context MLP with trainable embeddings and gradient tests
- [#2](https://github.com/goldaj/mini-llm-from-scratch/pull/2) : closed, fusionnée ; feat: leçon 02 trainable softmax bigram with gradient descent and held-out evaluation
- [#1](https://github.com/goldaj/mini-llm-from-scratch/pull/1) : closed, fusionnée ; [ChatGPT] Stabiliser le modèle bigramme et les tests

## Code et documentation
Racine : `.github`, `.gitignore`, `AGENTS.md`, `README.md`, `corpus.txt`, `docs`, `lecon01.py`, `lecon02.py`, `lecon03.py`, `tests`.

README : # Mini Language Model, from scratch

Projet pédagogique Python/PyCharm pour construire progressivement un modèle de langage, **sans modèle préentraîné et sans dépendances**.

## Exécuter dans PyCharm

- **Leçon 1 :** ouvrir `lecon01.py` puis cliquer Run (bigramme par comptage).
- **Leçon 2 :** ouvrir `lecon02.py` puis cliquer Run. Cette fois, les probabilités proviennent de **poids numériques entraînables** appris par gradient et softmax, avec perte d'entropie croisée sur le texte. Le programme affiche la perte d'entraînement, la perte de validation, la perplexité et un exemple généré, puis exporte `modele_softmax.json`.

- **Leçon 3 :** ouvrir `lecon03.py` puis cliquer Run : embeddings entraînables, contexte causal de 3 caractères, couche cachée tanh, comparaison à un unigramme et bigramme lissés sur la même validation. Documentation : [Leçon 03](docs/LECON03.md).

Depuis le terminal :

```bash
python lecon02.py --epochs 200 --learning-rate 2 --seed 7
python lecon03.py --epochs 10 --context 3 --dim 4 --hidden 16 --seed 7
python -m unittest discover -s tests -v
``

AGENTS : # AGENTS.md — Mini LLM from Scratch

## Avant de travailler
1. Lire `README.md` et les documents techniques pertinents, puis **`docs/CHATGPT_PROJECT_HISTORY.md`** pour les demandes, décisions et lacunes du contexte.
2. POC pédagogique de modèle de langage construit de zéro : leçon 01 bigramme de caractères, corpus français, transitions statistiques, génération et export JSON.
3. Travailler dans PyCharm et non VS Code. Procéder par étapes courtes et compréhensibles, répondre aux interruptions puis redonner la suite utile sous la réponse. Ne pas présenter le bigramme comme un Transformer ou un LLM avancé.

## Exécution et vérification
- `python lecon01.py` (Python 3.10+, bibliothèque standard).
- Utiliser de petites modifications contrôlables. Ne pas écraser ni supprimer des fichiers ou anci

## Questions d'expérience scientifique
1. Reproduire bigramme softmax et embeddings avec graines fixes ; comparer à une baseline et mesurer la baisse de loss sur jeu tenu à part.
2. Vérifier gradients via différences finies, absence d'information future et comportement pour tokens rares ou inconnus.
3. Séparer résultats pédagogiques sur corpus minuscule et affirmations sur la qualité d'un LLM à grande échelle.
4. Vérifier coûts CPU/RAM et versions de dépendances sur PyCharm, conserver des exemples rapides à lancer.
5. Les trois anciennes branches sont intégrées à l'historique de `main`. Ne pas ouvrir de PR redondante ; contrôler les workflows avant retrait des refs.
