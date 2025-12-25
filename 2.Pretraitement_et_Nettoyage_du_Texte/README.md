# Prétraitement et Nettoyage du Texte

Module de text mining pour le prétraitement des articles de cybersécurité.

## Fonctionnalités

- **Normalisation** : Conversion en minuscules, suppression URLs/emails
- **Tokenisation** : Découpage en mots
- **Filtrage** : Suppression ponctuation, chiffres, caractères spéciaux
- **Stop Words** : Retrait des mots non pertinents (le, la, est, un...)
- **Lemmatisation** : Réduction à la racine (courant, couraient → courir)
- **Stemming** : Alternative à la lemmatisation

## Installation

```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

## Utilisation

### Traitement automatique

```bash
python run.py
```

Lit `../data/articles_cybersecurity.json` et génère `../data/articles_preprocessed.json`.


## Structure des données

### Entrée
```json
{
  "source": "BleepingComputer",
  "titre": "New malware discovered",
  "contenu": "Full article text...",
  "date": "2025-12-25",
  "auteur": "John Doe"
}
```

### Sortie
```json
{
  "source": "BleepingComputer",
  "titre": "New malware discovered",
  "titre_tokens": ["new", "malware", "discover"],
  "contenu_original": "Full article text...",
  "contenu_tokens": ["full", "article", "text", ...],
  "nb_tokens": 234,
  "date": "2025-12-25",
  "auteur": "John Doe"
}
```

## Pipeline de traitement

1. **Normalisation**
   - Minuscules
   - Suppression URLs, emails, nombres
   - Suppression ponctuation

2. **Tokenisation**
   - Découpage en mots

3. **Filtrage**
   - Stop words (anglais)
   - Tokens < 3 caractères

4. **Lemmatisation/Stemming**
   - Réduction à la racine

## Architecture

```
2.Pretraitement_et_Nettoyage_du_Texte/
├── modules/
│   ├── __init__.py
│   ├── normalizer.py        # Normalisation du texte
│   ├── tokenizer.py         # Tokenisation
│   ├── stopwords_filter.py  # Filtrage des stop words
│   ├── lemmatizer.py        # Lemmatisation et stemming
│   └── preprocessor.py      # Orchestration du pipeline
├── run.py                   # Script principal
├── requirements.txt
└── README.md
```


## Statistiques

Le script affiche automatiquement :
- Nombre total de tokens : 15976
- Moyenne de tokens par article :  533 tokens/article
- Min/Max tokens : Min: 189 / Max: 2430
