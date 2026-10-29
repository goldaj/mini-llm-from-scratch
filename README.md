# Mini Language Model, from scratch

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
```

Le modèle de la leçon 2 est une couche linéaire one-hot vers softmax : **pas un Transformer et pas encore un LLM moderne**. La séparation entraînement/validation se fait par phrases/lignes distinctes, pas par caractères contigus, afin de limiter la fuite de données. Les caractères de validation absents du vocabulaire d'entraînement ne peuvent pas être évalués : le rapport indique la couverture.

Leçon détaillée : [docs/LECON02.md](docs/LECON02.md). Les sorties de modèles générées sont personnelles et non destinées au dépôt.

## Prochaines leçons
Après les trois premières leçons, prochaine étape : attention causale puis Transformer minimal, avec tests anti-fuite et campagnes multi-seed. Leçon 03 est un MLP à contexte fixe, pas de l'attention.
