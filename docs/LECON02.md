# Leçon 02 : un modèle avec de vrais poids entraînables

Ouvrir `lecon02.py` dans **PyCharm**, puis l'exécuter. Pas de `pip install` nécessaire.

### Étape 1 : transformation
Chaque caractère courant est encodé en vecteur *one-hot* : 1 sur la position du caractère, 0 ailleurs. Multiplier par la matrice W choisit une ligne de poids. Ces nombres servent de **logits**, convertis en probabilités par **softmax**.

### Étape 2 : erreur
La vraie lettre suivante sert de cible. La **cross-entropy** = -log(probabilité de la bonne lettre). On optimise les poids pour diminuer cette perte. Une perte moyenne de L correspond à une **perplexité** de exp(L). Une perplexité de 10 signifie approximativement 10 choix équiprobables, pas une précision de 90 %.

### Étape 3 : apprendre
Le code calcule le gradient exact, pour un caractère courant a :

`gradient(W[a][b]) = softmax(W[a])[b] - fréquence observée(b | a)`.

Puis il modifie `W[a][b] -= learning_rate * gradient` pendant plusieurs époques. C'est une descente de gradient pleine sur toutes les paires, pas une méthode magique. Le taux d'apprentissage est paramétrable.

### Étape 4 : vraie vérification
Le corpus est séparé **par lignes avant la création de paires** : la validation contient des phrases non utilisées dans l'optimisation. Une mesure sur le seul corpus d'entraînement serait trompeuse. Le programme rapporte les pertes train/validation, la perplexité et la perte d'une prédiction uniforme non entraînée. Attention : le vocabulaire ne contient que les caractères vus à l'entraînement ; la couverture des caractères de validation est explicitement donnée. Cette leçon n'utilise pas de réseau avec état caché ni de contexte de plusieurs tokens.

### Exercice
1. Exécuter avec `--epochs 20`, puis `--epochs 200`, noter l'évolution train et validation.
2. Comparer `--learning-rate 0.1` et `--learning-rate 2`.
3. Changer `--seed` ; observer la variation de la validation.
4. Lire `tests/test_lecon02.py` pour comprendre les contrôles automatiques.

### Prochaines étapes Codex
1. Ajout d'une vérification de gradient par différences finies, confrontant gradient analytique et numérique.
2. Couche embedding de dimension inférieure au vocabulaire, avec rétropropagation explicite.
3. Fenêtre contextuelle de longueur n>1 puis auto-attention, sans donner le nom de « Transformer » au modèle bigramme actuel.
4. Corpus plus grand mais légalement réutilisable, évaluation répétée sur plusieurs seeds, comparaison aux bigrammes statistiques de la leçon 1.
5. Prévoir que l'utilisation pédagogique reste faisable dans PyCharm et sur CPU standard. Aucun poids préentraîné.
