import json
import logging
from typing import List, Dict
from pathlib import Path
from modules.preprocessor import TextPreprocessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def process_articles(articles: List[Dict], preprocessor: TextPreprocessor) -> List[Dict]:
    processed = []
    
    for i, article in enumerate(articles):
        try:
            logger.info(f"Traitement {i+1}/{len(articles)}: {article.get('titre', '')[:50]}...")
            processed_article = preprocessor.preprocess_article(article)
            processed.append(processed_article)
        except Exception as e:
            logger.error(f"Erreur article {i+1}: {e}")
            continue
    
    return processed


def main():
    input_file = Path("../data/articles_cybersecurity.json")
    output_file = Path("../data/articles_preprocessed.json")
    
    if not input_file.exists():
        logger.error(f"Fichier {input_file} non trouvé")
        return
    
    logger.info(f"Chargement depuis {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    logger.info(f"Articles: {len(articles)}")
    
    preprocessor = TextPreprocessor(use_lemmatization=True)
    processed_articles = process_articles(articles, preprocessor)
    
    logger.info(f"Sauvegarde dans {output_file}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_articles, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Terminé: {len(processed_articles)} articles")
    
    if processed_articles:
        total_tokens = sum(art['nb_tokens'] for art in processed_articles)
        avg_tokens = total_tokens / len(processed_articles)
        logger.info(f"Total tokens: {total_tokens}")
        logger.info(f"Moyenne: {avg_tokens:.0f} tokens/article")
        logger.info(f"Min: {min(art['nb_tokens'] for art in processed_articles)}")
        logger.info(f"Max: {max(art['nb_tokens'] for art in processed_articles)}")


if __name__ == "__main__":
    main()
