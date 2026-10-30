# Audit GitHub / passation agent — 2026-10-30

Inventaire effectué sur GitHub (branches et PR ouvertes). **Ce document ne certifie pas le résultat des tests ni l'absence de différences fonctionnelles.**

- Dépôt : `goldaj/mini-llm-from-scratch`, défaut : `main`.
- PR ouvertes : aucune.

## Branches recensées (4)
- `chatgpt/review-20261024`
- `feat/lesson02-trainable-softmax-20261029`
- `feat/lesson03-context-embeddings-20261029`
- `main` (défaut)

## Recommandations pour l'agent suivant
- Vérifier reproductibilité des gradients, seeds, jeux de validation et leçons 01–03 avant tout nettoyage de branches.
- Comparer SHA, ascendance et diffs de chaque branche ; inspecter les PR closes et les références de versions.
- Préserver données, assets et tests. Aucune suppression par intuition ; aucune fusion de production sans validation.
- Rejouer les tests adaptés au dépôt, puis compléter cette fiche avec preuves et décisions par branche.

**État :** inventaire vérifié ; qualification détaillée des diffs non terminée.
