# Collecte de Données - Web Scraping Cybersécurité

Système automatisé de collecte d'articles sur la cybersécurité depuis plusieurs sources en ligne.

## Sources

- **BleepingComputer** - Actualités et vulnérabilités
- **Krebs on Security** - Analyses d'expert

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### Collecte automatique

```bash
python main.py
```

Les articles sont sauvegardés dans `../data/articles_cybersecurity.json`.

## Structure des données

```json
{
  "source": "BleepingComputer",
  "url": "https://...",
  "titre": "Titre de l'article",
  "date": "2025-12-25",
  "auteur": "Nom auteur",
  "contenu": "Texte complet...",
  "date_extraction": "2025-12-25T10:30:00"
}
```

## Architecture

```
1.Collecte_de_Donnees/
├── scrapers/
│   ├── __init__.py
│   ├── base.py              # Classe de base
│   ├── bleepingcomputer.py  # Scraper BleepingComputer
│   └── krebs.py             # Scraper Krebs
├── main.py                  # Point d'entrée
├── requirements.txt
└── README.md
```

## Tests

```bash
python test_scraper.py
```

## Bonnes pratiques

- Délai de 1s entre requêtes
- User-Agent configuré
- Gestion d'erreurs robuste
- Logs détaillés

## Dépannage

**Aucun article collecté** : Vérifier connexion Internet et logs

**Erreur 403** : Site bloque l'accès, utiliser une autre source

**Contenu vide** : Structure HTML du site a changé
