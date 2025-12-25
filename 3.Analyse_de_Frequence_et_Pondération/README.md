# Analyse de Fréquence et Pondération (TF-IDF)

Module d'analyse TF-IDF pour extraction de mots-clés et clustering thématique.

## Fonctionnalités

- **TF-IDF**: Calcul Term Frequency-Inverse Document Frequency pour pondération des termes
- **Extraction de mots-clés**: Identification des termes les plus discriminants par document et pour le corpus
- **Analyse thématique**: Clustering K-means pour regroupement automatique des documents
- **Termes discriminants**: Identification des mots-clés caractérisant chaque document

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python run.py
```

Lit `../data/articles_preprocessed.json` et génère `../data/tfidf_analysis.json`.

## Structure des résultats

```json
{
  "metadata": {
    "nb_documents": 30,
    "nb_features": 1000,
    "matrix_density": 18.4
  },
  "keywords": {
    "corpus_keywords": [["term", score], ...],
    "documents": [
      {
        "doc_index": 0,
        "titre": "...",
        "keywords": [["term", score], ...],
        "discriminant_terms": [["term", score], ...]
      }
    ]
  },
  "clustering": {
    "n_clusters": 5,
    "distribution": {"0": 4, "1": 8, ...},
    "clusters": [
      {
        "cluster_id": 0,
        "nb_documents": 4,
        "top_terms": [["term", score], ...],
        "documents": [...]
      }
    ]
  }
}
```

## Architecture

```
3.Analyse_de_Frequence_et_Pondération/
├── modules/
│   ├── __init__.py
│   ├── tfidf_analyzer.py      # Calcul TF-IDF avec scikit-learn
│   ├── keyword_extractor.py   # Extraction mots-clés discriminants
│   └── thematic_analyzer.py   # Clustering K-means thématique
├── run.py
├── requirements.txt
└── README.md
```

## Paramètres TF-IDF

- **max_features**: 1000 termes maximum
- **min_df**: Terme doit apparaître dans au moins 2 documents
- **max_df**: Terme ne doit pas apparaître dans plus de 80% des documents

## Clustering

- **Algorithme**: K-means
- **Nombre de clusters**: 5 (configurable)
- **Base**: Matrice TF-IDF des documents


## Résultats 

- **Documents analysés**: 30 articles
- **Termes uniques**: 1000 après filtrage
- **Densité matrice**: 18.40% (termes présents par document)
- **Clusters**: 5 groupes thématiques automatiques

### Distribution des clusters

```
Cluster 0: 4 documents
Cluster 1: 8 documents
Cluster 2: 4 documents
Cluster 3: 7 documents
Cluster 4: 7 documents
```

### Top 10 mots-clés du corpus

1. data: 0.0662
2. iam: 0.0624
3. window: 0.0556
4. said: 0.0528
5. university: 0.0522
6. domain: 0.0473
7. microsoft: 0.0463
8. ransomware: 0.0448
9. service: 0.0427
10. cve: 0.0425

### Exemple de résultat détaillé

```json
{
  "metadata": {
    "nb_documents": 30,
    "nb_features": 1000,
    "matrix_density": 18.4
  },
  "clustering": {
    "n_clusters": 5,
    "distribution": {
      "0": 4,
      "1": 8,
      "2": 4,
      "3": 7,
      "4": 7
    }
  }
}
```

## Interprétation

- **Mots-clés corpus**: Termes globalement importants dans tous les articles
- **Mots-clés document**: Termes les plus importants pour un article spécifique
- **Termes discriminants**: Termes qui distinguent un article des autres (score TF-IDF - moyenne corpus)
- **Clusters**: Regroupements thématiques basés sur similarité TF-IDF
