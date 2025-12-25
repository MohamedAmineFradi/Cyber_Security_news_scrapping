import json
import logging
from pathlib import Path
from typing import List, Dict
from modules.tfidf_analyzer import TFIDFAnalyzer
from modules.keyword_extractor import KeywordExtractor
from modules.thematic_analyzer import ThematicAnalyzer

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


def extract_tokens(articles: List[Dict]) -> List[List[str]]:
    documents = []
    for article in articles:
        tokens = article.get('contenu_tokens', [])
        if not tokens:
            logger.warning(f"Article sans tokens: {article.get('titre', 'Sans titre')}")
            tokens = []
        documents.append(tokens)
    return documents


def analyze_tfidf(articles: List[Dict], documents: List[List[str]]) -> tuple:
    logger.info("Calcul TF-IDF...")
    analyzer = TFIDFAnalyzer(max_features=1000, min_df=2, max_df=0.8)
    tfidf_matrix = analyzer.fit_transform(documents)
    
    logger.info(f"Matrice TF-IDF: {tfidf_matrix.shape[0]} documents × {tfidf_matrix.shape[1]} termes")
    logger.info(f"Densité: {(tfidf_matrix.nnz / (tfidf_matrix.shape[0] * tfidf_matrix.shape[1])) * 100:.2f}%")
    
    return analyzer, tfidf_matrix


def extract_keywords(analyzer: TFIDFAnalyzer, tfidf_matrix, articles: List[Dict]) -> Dict:
    logger.info("Extraction des mots-clés...")
    extractor = KeywordExtractor(tfidf_matrix, analyzer.feature_names)
    
    corpus_keywords = extractor.extract_corpus_keywords(top_n=30)
    logger.info(f"Top 10 mots-clés corpus:")
    for term, score in corpus_keywords[:10]:
        logger.info(f"  {term}: {score:.4f}")
    
    document_analysis = extractor.analyze_all_documents(articles, top_n=15)
    
    return {
        'corpus_keywords': corpus_keywords,
        'documents': document_analysis
    }


def perform_clustering(tfidf_matrix, articles: List[Dict], feature_names, n_clusters: int = 5) -> Dict:
    logger.info(f"Clustering K-means (k={n_clusters})...")
    thematic = ThematicAnalyzer(n_clusters=n_clusters)
    thematic.fit(tfidf_matrix)
    
    distribution = thematic.get_cluster_distribution()
    logger.info("Distribution des clusters:")
    for cluster_id, count in sorted(distribution.items()):
        logger.info(f"  Cluster {cluster_id}: {count} documents")
    
    cluster_summary = thematic.get_cluster_summary(articles, feature_names, top_terms=10)
    
    return {
        'n_clusters': n_clusters,
        'distribution': distribution,
        'clusters': cluster_summary
    }


def save_results(results: Dict, output_path: Path):
    logger.info(f"Sauvegarde résultats: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def main():
    input_file = Path("../data/articles_preprocessed.json")
    output_file = Path("../data/tfidf_analysis.json")
    
    if not input_file.exists():
        logger.error(f"Fichier introuvable: {input_file}")
        return
    
    articles = load_preprocessed_articles(input_file)
    documents = extract_tokens(articles)
    
    analyzer, tfidf_matrix = analyze_tfidf(articles, documents)
    
    keywords_results = extract_keywords(analyzer, tfidf_matrix, articles)
    
    clustering_results = perform_clustering(
        tfidf_matrix, 
        articles, 
        analyzer.feature_names,
        n_clusters=5
    )
    
    results = {
        'metadata': {
            'nb_documents': len(articles),
            'nb_features': tfidf_matrix.shape[1],
            'matrix_density': float((tfidf_matrix.nnz / (tfidf_matrix.shape[0] * tfidf_matrix.shape[1])) * 100)
        },
        'keywords': keywords_results,
        'clustering': clustering_results
    }
    
    save_results(results, output_file)
    logger.info("Analyse terminée")
    
    logger.info("\n=== RÉSUMÉ ===")
    logger.info(f"Documents analysés: {len(articles)}")
    logger.info(f"Termes uniques: {tfidf_matrix.shape[1]}")
    logger.info(f"Clusters identifiés: {clustering_results['n_clusters']}")


if __name__ == "__main__":
    main()
