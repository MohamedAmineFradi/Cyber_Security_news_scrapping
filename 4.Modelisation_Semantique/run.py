import json
import logging
from pathlib import Path
from typing import List, Dict
from modules.semantic_trainer import SemanticModelTrainer
from modules.semantic_explorer import SemanticExplorer
from modules.semantic_visualizer import SemanticVisualizer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_preprocessed_articles(file_path: Path) -> List[Dict]:
    logger.info(f"Chargement depuis {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    logger.info(f"Articles chargés: {len(articles)}")
    return articles


def extract_sentences(articles: List[Dict]) -> List[List[str]]:
    sentences = []
    for article in articles:
        tokens = article.get('contenu_tokens', [])
        if tokens and len(tokens) > 0:
            sentences.append(tokens)
    
    logger.info(f"Phrases extraites: {len(sentences)}")
    return sentences


def train_semantic_model(sentences: List[List[str]]) -> SemanticModelTrainer:
    trainer = SemanticModelTrainer(
        vector_size=200,
        window=5,
        min_count=2,
        sg=1,
        epochs=10,
        workers=4
    )
    
    trainer.train(sentences)
    return trainer


def explore_semantics(trainer: SemanticModelTrainer) -> Dict:
    logger.info("Exploration sémantique...")
    explorer = SemanticExplorer(trainer.get_model())
    
    test_words = ['ransomware', 'cloud', 'security', 'attack', 'data', 'microsoft', 'vulnerability']
    similar_words_results = {}
    
    for word in test_words:
        similar = explorer.get_similar_words(word, top_n=8)
        if similar:
            similar_words_results[word] = similar
            logger.info(f"  {word}: {[w for w, _ in similar[:3]]}")
    
    logger.info("Test d'analogies sémantiques...")
    analogies = explorer.test_analogies()
    for analogy in analogies:
        predicted = analogy['predicted'][0] if analogy['predicted'] else "N/A"
        logger.info(f"  {analogy['analogy']} → {predicted}")
    
    vocab_info = explorer.analyze_vocabulary(top_n=30)
    
    return {
        'similar_words': similar_words_results,
        'analogies': analogies,
        'vocabulary': vocab_info
    }


def visualize_semantics(trainer: SemanticModelTrainer, output_dir: Path):
    logger.info("Visualisation du space sémantique...")
    
    visualizer = SemanticVisualizer(trainer.get_model(), perplexity=30)
    visualizer.prepare_visualization(n_words=100)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    visualizer.plot_embedding(str(output_dir / "word2vec_space.png"))
    
    word_groups = {
        'Security': ['ransomware', 'malware', 'attack', 'vulnerability', 'threat', 'exploit', 'virus', 'virus'],
        'Cloud': ['cloud', 'aws', 'azure', 'microsoft', 'server', 'infrastructure'],
        'Data': ['data', 'database', 'storage', 'backup', 'encrypt'],
        'Network': ['network', 'internet', 'connection', 'bandwidth', 'protocol']
    }
    
    visualizer.plot_word_clusters(word_groups, str(output_dir / "word2vec_clusters.png"))
    
    logger.info("Visualisations sauvegardées")


def save_model_and_results(trainer: SemanticModelTrainer, results: Dict, 
                          model_path: Path, results_path: Path):
    logger.info("Sauvegarde du modèle et résultats...")
    
    trainer.save(str(model_path))
    
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Résultats sauvegardés: {results_path}")


def main():
    input_file = Path("../data/articles_preprocessed.json")
    model_path = Path("../data/word2vec_model")
    results_path = Path("../data/semantic_analysis.json")
    output_dir = Path("../data/visualizations")
    
    if not input_file.exists():
        logger.error(f"Fichier introuvable: {input_file}")
        return
    
    articles = load_preprocessed_articles(input_file)
    sentences = extract_sentences(articles)
    
    if not sentences:
        logger.error("Aucune phrase extraite")
        return
    
    trainer = train_semantic_model(sentences)
    
    exploration_results = explore_semantics(trainer)
    
    visualize_semantics(trainer, output_dir)
    
    save_model_and_results(trainer, exploration_results, model_path, results_path)
    
    logger.info("\n=== RÉSUMÉ ===")
    logger.info(f"Phrases d'entraînement: {len(sentences)}")
    logger.info(f"Vocabulaire: {len(trainer.get_model().wv)} mots")
    logger.info(f"Dimensions vecteur: {trainer.get_model().vector_size}")
    logger.info(f"Mots similaires testés: {len(exploration_results['similar_words'])}")
    logger.info(f"Analogies testées: {len(exploration_results['analogies'])}")
    logger.info("Modélisation sémantique terminée")


if __name__ == "__main__":
    main()
