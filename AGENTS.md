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
