from typing import List, Dict, Tuple
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter


class ThematicAnalyzer:
    def __init__(self, n_clusters: int = 5, random_state: int = 42):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        self.labels = None
        self.cluster_centers = None
    
    def fit(self, tfidf_matrix: np.ndarray) -> np.ndarray:
        self.labels = self.kmeans.fit_predict(tfidf_matrix)
        self.cluster_centers = self.kmeans.cluster_centers_
        return self.labels
    
    def get_cluster_distribution(self) -> Dict[int, int]:
        if self.labels is None:
            raise ValueError("Must call fit first")
        return {int(k): int(v) for k, v in Counter(self.labels).items()}
    
    def get_top_terms_per_cluster(self, feature_names: List[str], top_n: int = 10) -> Dict[int, List[Tuple[str, float]]]:
        if self.cluster_centers is None:
            raise ValueError("Must call fit first")
        
        cluster_terms = {}
        for cluster_id in range(self.n_clusters):
            center = self.cluster_centers[cluster_id]
            top_indices = center.argsort()[-top_n:][::-1]
            cluster_terms[cluster_id] = [(feature_names[i], float(center[i])) for i in top_indices]
        
        return cluster_terms
    
    def assign_documents_to_clusters(self, articles: List[Dict]) -> Dict[int, List[Dict]]:
        if self.labels is None:
            raise ValueError("Must call fit first")
        
        clusters = {i: [] for i in range(self.n_clusters)}
        for i, (article, label) in enumerate(zip(articles, self.labels)):
            clusters[int(label)].append({
                'doc_index': i,
                'titre': article.get('titre', 'Sans titre'),
                'source': article.get('source', 'Unknown'),
                'nb_tokens': article.get('nb_tokens', 0)
            })
        
        return clusters
    
    def get_cluster_summary(self, articles: List[Dict], feature_names: List[str], top_terms: int = 10) -> List[Dict]:
        distribution = self.get_cluster_distribution()
        cluster_terms = self.get_top_terms_per_cluster(feature_names, top_terms)
        document_clusters = self.assign_documents_to_clusters(articles)
        
        summary = []
        for cluster_id in range(self.n_clusters):
            summary.append({
                'cluster_id': cluster_id,
                'nb_documents': distribution[cluster_id],
                'top_terms': cluster_terms[cluster_id],
                'documents': document_clusters[cluster_id]
            })
        
        return summary
