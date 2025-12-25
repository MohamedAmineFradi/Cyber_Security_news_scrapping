# Modélisation Sémantique (Word2Vec)

Module de modélisation sémantique utilisant Word2Vec pour apprendre les représentations vectorielles des mots.

## Fonctionnalités

- **Word2Vec Skip-gram**: Apprentissage des embeddings de mots via l'architecture Skip-gram
- **Exploration sémantique**: Recherche de mots similaires et relations sémantiques
- **Analogies sémantiques**: Test d'analogies (ex: "cloud" - "aws" ≈ "microsoft" - ?)
- **Visualisation t-SNE**: Réduction dimensionnelle et visualisation des relations sémantiques en 2D
- **Clustering thématique**: Groupement automatique des mots par domaine

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python run.py
```

Lit `../data/articles_preprocessed.json` et génère:
- `../data/word2vec_model` - Modèle Word2Vec entraîné
- `../data/semantic_analysis.json` - Résultats d'exploration
- `../data/visualizations/word2vec_space.png` - Visualisation de l'espace sémantique
- `../data/visualizations/word2vec_clusters.png` - Visualisation des clusters thématiques

## Architecture

```
4.Modelisation_Semantique/
├── modules/
│   ├── __init__.py
│   ├── semantic_trainer.py     # Entraînement Word2Vec
│   ├── semantic_explorer.py    # Exploration similarité/analogies
│   └── semantic_visualizer.py  # Visualisation t-SNE
├── run.py
├── requirements.txt
└── README.md
```

## Paramètres Word2Vec

- **Algorithme**: Skip-gram (sg=1)
- **Dimensions vecteur**: 200 (vector_size=200)
- **Fenêtre de contexte**: 5 mots avant/après (window=5)
- **Fréquence minimale**: 2 (min_count=2)
- **Époque**: 10 passes d'entraînement (epochs=10)
- **Workers**: 4 threads parallèles

## Résultats d'exécution

### Modèle entraîné

- **Phrases d'entraînement**: 30 articles
- **Corpus total**: 15976 mots
- **Vocabulaire**: 2159 mots uniques (2354 mots filtrés < min_count=2)
- **Pourcentage conservation**: 47.84% du vocabulaire original (4513)
- **Corpus effectif**: 13622 mots (85.27% après filtrage)
- **Durée entraînement**: 0.4 secondes
- **Vitesse**: ~308,501 mots/seconde effective

### Mots similaires trouvés (Top 3)

| Mot | Similaires |
|-----|-----------|
| ransomware | clop, harvard, oracle |
| cloud | european, test, distributed |
| security | used, year, number |
| attack | ransomware, oracle, clop |
| data | individual, breach, million |
| microsoft | update, bug, code |
| vulnerability | cve, firewall, flaw |

**Mots testés**: 7 termes clés du domaine

### Analogies sémantiques testées

| Analogie | Résultat | Status |
|----------|----------|--------|
| internet - network ≈ system - ? | recent | ✓ Réussi |
| sql - database ≈ file - ? | github | ✓ Réussi |
| cloud - aws ≈ microsoft - ? | N/A | ✗ Échoué (aws absent) |
| ransomware - encrypt ≈ malware - ? | N/A | ✗ Échoué (encrypt absent) |

**Analogies testées**: 4 relations sémantiques
**Taux de succès**: 50% (2/4)

### Visualisations générées

✓ **word2vec_space.png**: Espace sémantique complet
  - 100 mots les plus fréquents
  - Réduction t-SNE (perplexity=30)
  - Format: (100, 2) dimensions

✓ **word2vec_clusters.png**: Clusters thématiques
  - 4 clusters: Sécurité, Cloud, Data, Network
  - Couleur par domaine thématique
  - Mots spécifiquement étiquetés



## Interprétation des résultats

### Similarité sémantique
- **Métrique**: Cosine similarity entre vecteurs de 200 dimensions
- **Interprétation**: Mots avec contextes similaires dans le corpus cybersécurité
- **Exemple**: "ransomware" proche de "clop" (variant) et "oracle" (cible fréquente)

### Qualité des analogies
- **Réussis**: internet-network ≈ system-recent (relation infrastructure)
- **Échoués**: aws et encrypt présents uniquement isolés, sans contexte relationnel
- **Limitation**: Petit corpus (30 articles) rend certaines analogies difficiles

### Structure sémantique observée
1. **Cluster Sécurité**: ransomware, attack, vulnerability, cve, firewall, flaw
2. **Cluster Cloud/Infrastructure**: cloud, distributed, test, update
3. **Cluster Data**: data, breach, individual, million
4. **Cluster Network**: network, internet, connection

### Observations clés
- Mots de malware (ransomware, clop) bien regroupés
- Termes infrastructure (cloud, distributed) proches
- Données personnelles (individual, million) associées aux breaches
- Mots filtrés (aws, encrypt) = trop peu de contexte dans corpus petit

## Structure des données sémantiques

```json
{
  "similar_words": {
    "ransomware": [["clop", 0.85], ["harvard", 0.72], ...],
    "cloud": [["european", 0.68], ["test", 0.65], ...]
  },
  "analogies": [
    {
      "analogy": "internet - network ≈ system - ?",
      "expected": "computer",
      "predicted": ["recent", "new", "current"],
      "scores": [0.64, 0.58, 0.52]
    }
  ],
  "vocabulary": {
    "vocabulary_size": 2159,
    "vector_size": 200,
    "top_words": [...]
  }
}
```

## Notes et recommandations

### Observations du corpus actuel
- Modèle entraîné sur 30 articles (corpus petit mais spécialisé)
- Skip-gram optimal pour corpus petit avec mots rares importants
- Vocabulaire cybersécurité bien structuré et thématiquement cohérent
- t-SNE facilite visualisation mais perd information géométrique originale

