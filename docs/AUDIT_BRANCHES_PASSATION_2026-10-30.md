# Passation GitHub : branches, PR, audit critique — 30/10/2026

**Objet :** Cours progressif de modélisation du langage hors ligne, PyCharm. Méthode : inspection du README, de AGENTS.md, des refs et PR GitHub. Aucun test métier exécuté dans cette passe.

## Inventaire exhaustif des branches (référence `main`)
- `chatgpt/review-20261024` — `1028be4707b0c7c4b73fd619bf15683615fc1299` (branche historique : vérifier l'ascendance à nouveau avant nettoyage)
- `feat/lesson02-trainable-softmax-20261029` — `046614d48e950a3eedcc03d5a52009e958b34c83` (branche historique : vérifier l'ascendance à nouveau avant nettoyage)
- `feat/lesson03-context-embeddings-20261029` — `a84ec06872aa19ed0b12c456df8dad56ddaa7413` (comparée en direct : behind, ahead 0, behind 3)
- `main` — `849a6994a76458a0561cc07d0f31b58f817367aa` (conserver, branche par défaut)

## PR (3)
- [#3](https://github.com/goldaj/mini-llm-from-scratch/pull/3) : fusionnée, `feat/lesson03-context-embeddings-20261029` vers `main`.
- [#2](https://github.com/goldaj/mini-llm-from-scratch/pull/2) : fusionnée, `feat/lesson02-trainable-softmax-20261029` vers `main`.
- [#1](https://github.com/goldaj/mini-llm-from-scratch/pull/1) : fusionnée, `chatgpt/review-20261024` vers `main`.

## Analyse critique
Comparer réellement Leçon 01 bigramme par comptages, Leçon 02 softmax entraînable, Leçon 03 MLP causal à embeddings. Mesurer par split bloqué hors échantillon, gradients, seed, stabilité, sans présenter le MLP comme un Transformer. Préserver les leçons antérieures.

## Plan de reprise
Relire docs/LECON02.md/LECON03.md, exécuter unittest, effectuer des contrôles de gradients numériques et conserver un lancement simple dans PyCharm.

## Règles
Lire README (# Mini Language Model, from scratch), AGENTS.md et docs/CHATGPT_PROJECT_HISTORY.md. Ne pas inférer d'une PR fusionnée que les tests manuels ont été exécutés. Aucun merge/suppression de branches ni changement de programme réalisé ici. Les branches encore visibles ne sont pas des PR ouvertes.
