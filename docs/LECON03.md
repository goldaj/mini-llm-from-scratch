# Leçon 03 — embeddings et contexte causal de 3 caractères

## Fonctionnalité

La leçon 02 ne regardait qu'un caractère précédent. `lecon03.py` entraîne désormais un véritable réseau de neurones **multicouche** entièrement écrit en Python, sans PyTorch et sans poids préentraînés.

- Chaque symbole est projeté dans une table d'embeddings apprenables.
- Le modèle concatène les embeddings des **3 caractères précédents** (fenêtre réglable de 1 à 5).
- Une couche cachée `tanh` transforme ce contexte en logits, puis `softmax` donne une distribution du caractère suivant.
- `BOS` et `EOS` délimitent les phrases : aucun caractère futur n'entre dans le contexte.
- La rétropropagation (`gradients`) et la descente stochastique (`step`) sont écrites explicitement.
- Le programme mesure perte d'entraînement, validation, perplexité, nombre de paramètres et compare aux références unigramme et bigramme **sur exactement les mêmes exemples évaluables**.
- Les poids appris sont exportables en JSON.

## Tester dans PyCharm

1. Ouvrir le dépôt et sélectionner Python 3.10+.
2. Lancer `lecon03.py`, ou utiliser cette commande depuis le terminal PyCharm :

```bash
python lecon03.py --epochs 10 --context 3 --dim 4 --hidden 16 --seed 7
python -m unittest discover -s tests -v
```

Le modèle produit `modele_context_mlp.json` dans le répertoire du script : ne pas ajouter ce modèle ni de corpus privé à Git. Les paramètres `--context`, `--dim`, `--hidden`, `--epochs`, `--learning-rate` et `--seed` servent à expérimenter.

## Ce qui est mathématiquement appris

Pour le contexte `(c₁,c₂,c₃)`, le vecteur `x` est la concaténation des trois lignes de la table d'embeddings. La couche cachée calcule `h = tanh(x·W1 + b1)`, puis `p = softmax(h·W2 + b2)`. La perte est `-log(p[cible])`. Le gradient pour les logits est `p - one_hot(cible)` ; la règle de chaîne fait remonter l'erreur jusqu'aux embeddings. Les caractères qui apparaissent plusieurs fois dans une même fenêtre cumulent correctement leurs contributions.

Le test `test_gradient_finite_difference_for_all_layers` vérifie les dérivées analytiques par différences finies (embeddings, W1, b1, W2, b2). Cela prouve la cohérence locale des gradients testés, pas que le modèle généralise.

## Données, comparabilité et limites

Le découpage par **lignes**, avant tokenisation, est hérité de `split_corpus` de la leçon 02. Le vocabulaire est construit sur le *train* uniquement. Une transition de validation avec symbole absent (y compris dans le contexte) est exclue de la NLL ; le rapport indique la **couverture des exemples**. Même logique pour les références unigramme/bigramme. Les lignes répétées dans un petit corpus pourraient toutefois se retrouver des deux côtés du split : pour une étude plus sérieuse, regrouper les doublons par familles.

**État des preuves :** une implémentation et des tests ont été écrits, mais leur exécution intégrale n'a **pas été vérifiée** sur ce dépôt dans cette intervention. Les valeurs de perte et perplexité sont à produire réellement avec la commande ci-dessus, puis à conserver comme artefacts reproductibles. Ne pas afficher de nombres issus de calculs non exécutés.

Même un résultat sur **un seul découpage et une seule graine** ne valide ni robustesse multi-seed ni supériorité générale du réseau. Les deux références sont des modèles statistiques lissés, pas la leçon 02 optimisée ; le rapport ne prétend pas comparer à poids ou calcul égal.

**Pas d'attention ni de Transformer** : le contexte est fixe et borné. Rien n'est connecté à Internet, Twitch ou des données sensibles.

## Reprise Codex

1. Relire `AGENTS.md`, `docs/CHATGPT_PROJECT_HISTORY.md`, leçon 02 et la **PR parent #2**.
2. Continuer sur la branche empilée `feat/lesson03-context-embeddings-20261029`; ne pas fusionner avant #2.
3. Vérifier les workflows Python 3.10/3.12 (suite complète + smoke leçon 03), exécuter également dans PyCharm.
4. Approfondir la mesure scientifique : 5+ seeds, courbes de généralisation, mêmes budgets, corpus légalement réutilisable et plus large, séparation sans doublons ; rester hors données test jusqu'à protocole gelé.
5. Étape suivante : attention causale avec tests anti-fuite et masque temporel, avant toute architecture Transformer.

Pas de fusion automatique, ni remplacement des leçons antérieures.
