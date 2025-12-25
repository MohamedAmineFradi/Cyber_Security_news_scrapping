import json
import os
from typing import List, Dict
import logging
from scrapers import BleepingComputerScraper, KrebsScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataCollector:
    def __init__(self, output_dir: str = "../data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.articles = []
        self.scrapers = [
            BleepingComputerScraper(),
            KrebsScraper()
        ]
    
    def collect_all(self, max_articles_per_source: int = 50) -> None:
        logger.info("Début de la collecte...")
        
        for scraper in self.scrapers:
            try:
                articles = scraper.scrape(max_articles_per_source)
                self.articles.extend(articles)
                logger.info(f"{scraper.source_name}: {len(articles)} articles collectés")
            except Exception as e:
                logger.error(f"Erreur avec {scraper.source_name}: {e}")
        
        logger.info(f"Collecte terminée. Total: {len(self.articles)} articles")
        
        if len(self.articles) == 0:
            logger.warning("ATTENTION: Aucun article collecté")
    
    def save_to_json(self, filename: str = "articles_cybersecurity.json") -> None:
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.articles, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Données sauvegardées: {output_path}")
            logger.info(f"Nombre total d'articles: {len(self.articles)}")
            
            sources = {}
            for article in self.articles:
                source = article.get('source', 'Unknown')
                sources[source] = sources.get(source, 0) + 1
            
            logger.info("Statistiques par source:")
            for source, count in sources.items():
                logger.info(f"  - {source}: {count} articles")
        
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")


def main():
    collector = DataCollector(output_dir="../data")
    collector.collect_all(max_articles_per_source=150)
    collector.save_to_json("articles_cybersecurity.json")


if __name__ == "__main__":
    main()
