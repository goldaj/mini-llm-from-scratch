# AGENTS.md — Mini LLM from Scratch

## Avant de travailler
1. Lire `README.md` et les documents techniques pertinents, puis **`docs/CHATGPT_PROJECT_HISTORY.md`** pour les demandes, décisions et lacunes du contexte.
2. POC pédagogique de modèle de langage construit de zéro : leçon 01 bigramme de caractères, corpus français, transitions statistiques, génération et export JSON.
3. Travailler dans PyCharm et non VS Code. Procéder par étapes courtes et compréhensibles, répondre aux interruptions puis redonner la suite utile sous la réponse. Ne pas présenter le bigramme comme un Transformer ou un LLM avancé.

## Exécution et vérification
- `python lecon01.py` (Python 3.10+, bibliothèque standard).
- Utiliser de petites modifications contrôlables. Ne pas écraser ni supprimer des fichiers ou anciennes versions sans demande explicite.
- Distinguer hypothèses, code présent, essais effectivement exécutés et éléments encore à valider.

## Passation à Codex et archivage permanent
- **Document de référence de la conversation :** `docs/CHATGPT_PROJECT_HISTORY.md` ; il peut être incomplet et le dit explicitement.
- Après chaque intervention, mettre à jour ce document si une décision, une contrainte, une étape ou un nouveau contexte pertinent change. Référencer les nouveaux messages de l'utilisateur et de l'assistant lorsque leur texte exact est accessible.
- Format : date ISO et fuseau si connus, rôle `Utilisateur` ou `Assistant`, mention `verbatim` seulement pour un texte exact. Sinon `résumé reconstruit, non verbatim`. Ne pas inventer d'heure ni de citation.
- Si l'historique intégral n'est pas disponible, le signaler et demander un export réel plutôt que fabriquer une transcription. Préserver les exports existants sans les réécrire.
- Exclure secrets, identifiants, données personnelles et contenus non destinés à la publication. Le niveau de visibilité de ce dépôt s'applique aussi aux documents ajoutés.

## Leçon 02 (2026-10-29)

`lecon02.py` ajoute un vrai modèle bigramme linéaire avec gradient et softmax, évaluation par lignes tenues à l'écart et génération. Lire `docs/LECON02.md`, tester `python -m unittest discover -s tests -v` et garder le chemin pédagogique PyCharm. Ne pas appeler ce modèle un Transformer et ne pas retirer `lecon01.py`. Préserver le caractère hors ligne et la confidentialité des corpus.

## Leçon 03 — contexte causal et embeddings (2026-10-29)

- Branche empilée `feat/lesson03-context-embeddings-20261029`, base `feat/lesson02-trainable-softmax-20261029` (PR #2). Ne pas fusionner indépendamment avant le parent.
- `lecon03.py` : vrai MLP de caractères, embeddings, contexte 3 (1–5), tanh et rétropropagation explicite, NLL validation et références unigramme/bigramme lissés sur les mêmes exemples.
- Lire `docs/LECON03.md`. Les cinq tests `tests/test_lecon03.py` contrôlent notamment les gradients par différences finies et l'absence de tokens futurs.
- Tests : `python -m unittest discover -s tests -v` puis `python lecon03.py --epochs 3 --length 10 --output /tmp/modele_context_mlp.json`. Sur Windows, choisir un chemin de sortie sous un répertoire temporaire.
- Aucun réseau, aucun jeu de données privé, aucune API externe. Pas d'attention ni de Transformer : ne pas présenter ce MLP pédagogique comme un LLM moderne.
- Le corpus jouet comporte 15 lignes ; les mesures de NLL, perplexité et gain face aux baselines **restent à exécuter et contrôler**. Aucune statistique de validation n'est certifiée pour cette branche, même sur un split unique.
- Réviser les états CI/PR avant toute intégration ; passage à la leçon 04 : attention causale, évaluation multi-seed et tests anti-fuite.
