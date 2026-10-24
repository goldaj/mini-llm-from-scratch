# Contexte ChatGPT pour Mini LLM from Scratch

**Initialisé le 2026-10-24. Couverture : partielle, sauf les sources originales référencées explicitement.** Codex doit lire ce fichier après `AGENTS.md` et avant toute reprise du projet. Une mémoire reconstruite n'est pas la totalité du chat.

## Projet confirmé par le dépôt
- Dépôt : `goldaj/mini-llm-from-scratch`.
- Objet : POC pédagogique de modèle de langage construit de zéro : leçon 01 bigramme de caractères, corpus français, transitions statistiques, génération et export JSON.
- Contraintes : Travailler dans PyCharm et non VS Code. Procéder par étapes courtes et compréhensibles, répondre aux interruptions puis redonner la suite utile sous la réponse. Ne pas présenter le bigramme comme un Transformer ou un LLM avancé.
- Validation : `python lecon01.py` (Python 3.10+, bibliothèque standard).

## Échanges attestés ou sources à lire

2026-10-13 — Utilisateur (verbatim connu) : « Non. On va utiliser pyCharm. Parce que c'est ce que j'ai l'habitude d'utiliser. »

2026-10-13 — Utilisateur (verbatim connu) : « Je vais souvent faire des commentaires sur le milieu de ta réponse. Il faudra que tu me répondes et que tu me remettes tout le reste de ta réponse au-dessous, afin que je n'ai pas à scroller et recoller les morceaux moi-même. »

Réponse de l'assistant : texte exact indisponible ici.

2026-10-24 — Utilisateur (verbatim, heure non vérifiable) : « je te demande de lire mes repo git où tu es le dernier utilisateur, de rajouter un AGENTS.md pertinent s'il n'y en a pas. Mais en plus, tu rajoutera un document repérable par codex (peut être le référencer dans le AGENTS.md justement ?) où tu mets l'intégralité de nos échanges liés à ce projet. Mes questions, tes réponses (de sorte à les différencier) et les horodatages si tu les as. »

## Limites de couverture, fidélité et mise à jour
- Les passages marqués `verbatim` sont des extraits exacts disponibles dans le contexte ; les résumés ne doivent **jamais** être cités comme du dialogue mot pour mot. Aucune réponse complète de l'assistant n'a été inventée.
- Pour obtenir l'intégralité des questions, réponses et horodatages : intégrer un export authentique des conversations pertinentes ; conserver l'ordre et le rôle des messages, et expurger avant publication les éléments sensibles et hors projet.
- En intervention future, ajouter en bas les nouveaux dialogues sourcés et les décisions vérifiées, sans effacer les entrées précédentes. Ce journal et `AGENTS.md` sont versionnés dans Git.

## 2026-10-24 — Revue parallèle (heure inconnue)

**Utilisateur (verbatim, extrait)** : « Tu vas refaire la même chose sur TOUT mon repo git. Tu vas commencer par les projets les plus gros, regarder ce que tu peux faire dessus et le faire sur ta branch ».

**Assistant (résumé reconstruit)** : correction de l'accès à un caractère absent (évite de modifier le vocabulaire appris pendant une requête), refus d'une longueur négative, nouveaux tests pédagogiques et CI. Branche `chatgpt/review-20261024`; aucune modification de `main`.

**Validation** : résultats de CI à vérifier, aucun test exécuté localement via le connecteur GitHub. Confiance élevée pour le correctif ciblé ; ne pas confondre prototype statistique bigramme et LLM entraîné. Codex doit vérifier le diff avant fusion.
