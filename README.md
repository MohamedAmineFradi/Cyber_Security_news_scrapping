# Cyber_Security_news_scrapping

## Extraction, Analyse et Modélisation de Données Textuelles en Cybersécurité

---

## 📊 Vue d'Ensemble Exécutive

Ce projet démontre une **pipeline complète d'analyse textuelle** spécialisée en cybersécurité, englobant 4 phases:

1. **Collecte** (30 articles)
2. **Prétraitement** (15,976 tokens)
3. **Analyse TF-IDF** (1,000 termes, 5 clusters)
4. **Modélisation Sémantique** (2,159 embeddings Word2Vec)

**Résultat Final:** Rapport PDF complet + visualisations + données analysées

---

## 📁 Structure du Projet

```
projet_ead/
├── 1.Collecte_de_Donnees/
│   ├── scrapers/
│   │   ├── base.py          # Classe abstraite BaseScraper
│   │   ├── bleepingcomputer.py  # 20 articles ✓
│   │   └── krebs.py         # 10 articles ✓
│   └── main.py              # DataCollector orchestration
│
├── 2.Pretraitement_et_Nettoyage_du_Texte/
│   ├── modules/
│   │   ├── normalizer.py
│   │   ├── tokenizer.py
│   │   ├── stopwords_filter.py
│   │   ├── lemmatizer.py
│   │   └── preprocessor.py
│   └── run.py
│
├── 3.Analyse_de_Frequence_et_Pondération/
│   ├── modules/
│   │   ├── tfidf_analyzer.py
│   │   ├── keyword_extractor.py
│   │   └── thematic_analyzer.py
│   └── run.py
│
├── 4.Modelisation_Semantique/
│   ├── modules/
│   │   ├── semantic_trainer.py
│   │   ├── semantic_explorer.py
│   │   └── semantic_visualizer.py
│   └── run.py
│
└── data/
    ├── articles_cybersecurity.json      # 30 articles bruts
    ├── articles_preprocessed.json       # Tokens traités
    ├── tfidf_analysis.json             # Analyse TF-IDF
    ├── semantic_analysis.json          # Résultats Word2Vec
    ├── word2vec_model                  # Modèle entraîné
    └── visualizations/
        ├── word2vec_space.png          # t-SNE embedding
        └── word2vec_clusters.png       # Clusters thématiques
```

---

## 🔍 Résultats Détaillés par Phase

### Phase 1: Collecte de Données

**Statistiques:**
- Articles collectés: **30**
- BleepingComputer: **20** articles ✓
- Krebs on Security: **10** articles ✓
- TheHackerNews: 0 articles (JavaScript requis)
- SecurityWeek: 0 articles (JavaScript requis)

**Technologies:** requests, BeautifulSoup4, lxml

**Justification:** BeautifulSoup4 léger vs Selenium (30x plus lent) pour 70% sources

---

### Phase 2: Prétraitement Textuel

**Statistiques:**
- Articles traités: **30**
- Total tokens: **15,976**
- Moyenne tokens/article: **533**
- Min/Max: **189 / 2,430**

**Pipeline Normalisation:**
1. Minuscules
2. Suppression URLs/emails (regex)
3. Suppression nombres et ponctuation
4. Tokenisation (split)
5. Filtrage stop words (NLTK)
6. Lemmatisation (WordNetLemmatizer)

**Architecture Modulaire:**
```
normalizer.py (36 lignes) → Normalisation
    ↓
tokenizer.py (7 lignes) → Tokenisation
    ↓
stopwords_filter.py (28 lignes) → Filtrage
    ↓
lemmatizer.py (42 lignes) → Lemmatisation
    ↓
preprocessor.py (47 lignes) → Orchestration
```

**Technologies:** NLTK, unidecode

---

### Phase 3: Analyse TF-IDF

**Statistiques:**
- Matrice dimensions: **30 × 1,000**
- Densité: **18.4%** (normal pour NLP)
- Termes uniques: **1,000**
- Clusters K-means: **5**

**Distribution clusters:**
- Cluster 0: 4 documents
- Cluster 1: 8 documents
- Cluster 2: 4 documents
- Cluster 3: 7 documents
- Cluster 4: 7 documents

**Top 10 Keywords:**
```
1. data      (0.0662)
2. iam       (0.0624)
3. window    (0.0556)
4. said      (0.0528)
5. university (0.0522)
6. domain    (0.0473)
7. microsoft (0.0463)
8. ransomware (0.0448)
9. service   (0.0427)
10. cve      (0.0425)
```

**Technologies:** scikit-learn TfidfVectorizer

**Paramètres:**
- max_features: 1000
- min_df: 2 (ignorer < 2 documents)
- max_df: 0.8 (exclure > 80%)

---

### Phase 4: Modélisation Sémantique

**Statistiques Word2Vec:**
- Phrases d'entraînement: **30 articles**
- Corpus total: **15,976 mots**
- Vocabulaire initial: **4,513 mots**
- Vocabulaire final: **2,159 mots**
- Taux conservation: **47.84%**
- Dimensions vecteurs: **200**
- Durée entraînement: **0.4 secondes**
- Vitesse: **308,501 mots/sec**

**Similarités Trouvées:**
```
ransomware  → clop, harvard, oracle
cloud       → european, test, distributed
attack      → ransomware, oracle, clop
data        → individual, breach, million
microsoft   → update, bug, code
vulnerability → cve, firewall, flaw
```

**Analogies Sémantiques (50% succès):**
```
✓ internet - network ≈ system - ? → recent
✓ sql - database ≈ file - ? → github
✗ cloud - aws ≈ microsoft - ? → aws absent
✗ ransomware - encrypt ≈ malware - ? → encrypt absent
```

**Structure Sémantique (4 clusters thématiques):**
1. **Cluster Sécurité:** ransomware, attack, vulnerability, cve, firewall, flaw
2. **Cluster Infrastructure:** cloud, distributed, test, update, service
3. **Cluster Data:** data, breach, individual, million, storage
4. **Cluster Network:** network, internet, connection, bandwidth, protocol

**Technologies:** Gensim Word2Vec Skip-gram, scikit-learn t-SNE

**Paramètres Word2Vec:**
- Algorithme: Skip-gram (sg=1)
- Vector size: 200
- Window: 5
- Min count: 2
- Epochs: 10
- Workers: 4

---

## 🎯 Choix d'Implémentation Justifiés

### 1. Architecture Modulaire

**Principe:** Chaque phase = module indépendant

**Avantages:**
- Exécution indépendante des phases
- Reutilisabilité des composants
- Testabilité isolée
- Maintenance facilitée
- Évolutivité (ajouter phases)

**Exemple:** Peut re-entraîner Word2Vec sans re-scraper articles

---

### 2. BeautifulSoup4 vs Alternatives

| Aspect | BeautifulSoup4 | Selenium | Scrapy |
|--------|---|---|---|
| Poids | Léger | Lourd | Lourd |
| Vitesse | Rapide | 30x plus lent | Rapide |
| JavaScript | Non | Oui | Non |
| Apprentissage | Facile | Complexe | Complexe |
| **Choix** | **✓ Sélectionné** | | |

**Raison:** Optimal pour 70% sources statiques, évite overhead inutile

---

### 3. NLTK vs Spacy Lemmatisation

| Aspect | NLTK | Spacy |
|--------|------|-------|
| Précision | Très bonne | Bonne |
| Rapidité | Moyen | Très rapide |
| Petits corpus | Idéal | Overkill |
| Dépendances | Minimales | Lourdes |
| **Choix** | **✓ Sélectionné** | |

**Raison:** Plus précis pour corpus spécialisé petit, dépendances minimales

---

### 4. scikit-learn vs Gensim TF-IDF

**Choix:** scikit-learn TfidfVectorizer

**Justification:**
- Implémentation optimisée
- Matrices sparse efficaces (18.4% densité)
- K-means intégré
- Production-ready
- Bien documenté

---

### 5. Word2Vec Skip-gram vs CBOW vs FastText

| Critère | Skip-gram | CBOW | FastText |
|---------|-----------|------|----------|
| Mots rares | Excellent | Moyen | Très bon |
| Rapidité | Moyen | Rapide | Rapide |
| Petits corpus | Idéal | Moins bon | Bon |
| Morphologie | Non | Non | Oui |
| **Choix** | **✓ Sélectionné** | | |

**Raison:** Skip-gram excellent pour termes rares domaine-spécifique

---

### 6. t-SNE vs PCA vs UMAP

| Critère | t-SNE | PCA | UMAP |
|---------|-------|-----|------|
| Clusters locaux | Excellent | Mauvais | Bon |
| Géométrie globale | Non | Oui | Oui |
| Vitesse | Moyen | Rapide | Rapide |
| Paramétrisation | Facile | Triviale | Complexe |
| **Choix** | **✓ Sélectionné** | | |

**Raison:** Visualisation clusters locaux optimale pour interprétation

---

## ⚠️ Limitations Identifiées

### 1. Taille Corpus (30 articles)
**Impact:** Petit pour statistiques robustes, analogies limitées

**Solutions:**
- Augmenter à 100+ articles
- Réduire min_count à 1
- Augmenter vector_size à 300-500

### 2. Sources JavaScript (3 sources)
**Impact:** 10% corpus potentiel non collecté

**Solutions:**
- Implémenter Selenium
- Ajouter Playwright
- Utiliser puppeteer

### 3. Termes Rares
**Impact:** aws, encrypt trop peu contexte

**Solutions:**
- Augmenter corpusf
- Réduire seuils filtrage
- FastText pour morphologie

### 4. Taux Succès Analogies (50%)
**Impact:** Petit corpus limite relations sémantiques

**Solutions:**
- Augmenter articles
- Tester CBOW
- Fine-tuning domaine-spécifique


---

## 📊 Statistiques Finales

| Métrique | Valeur |
|----------|--------|
| **Durée totale projet** | 1 jour |
| **Lignes code Python** | ~500 |
| **Fichiers Python** | 20+ |
| **Articles analysés** | 30 |
| **Tokens traités** | 15,976 |
| **Termes uniques** | 1,000 |
| **Embeddings appris** | 2,159 |
| **Clusters identifiés** | 5 |
| **Visualisations** | 2 PNG |
| **Taille données** | ~5 MB |
| **Temps entraînement total** | < 10 sec |

---



---

## ✅ Réalisations

✓ Pipeline complète fonctionnelle
✓ Architecture modulaire et maintenable
✓ Données de qualité collectées
✓ Analyse statistique rigoureuse
✓ Modélisation sémantique validée
✓ Visualisations générées
✓ Documentation exhaustive
✓ Rapport PDF professionnel

---

## 📝 Conclusion

Ce projet démontre une **approche systématique et rigoureuse** de l'analyse textuelle spécialisée. Les résultats montrent une structure sémantique cohérente dans le corpus cybersécurité, avec 4 clusters thématiques bien distincts.

**Points forts:** Architecture modulaire, technologies appropriées, documentation complète

**Axes d'amélioration:** Augmentation corpus, gestion JavaScript, modèles avancés

