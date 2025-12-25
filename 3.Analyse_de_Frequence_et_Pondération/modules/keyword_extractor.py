from typing import List, Dict, Tuple
import numpy as np


class KeywordExtractor:
    def __init__(self, tfidf_matrix: np.ndarray, feature_names: List[str]):
        self.tfidf_matrix = tfidf_matrix
        self.feature_names = feature_names
    
    def extract_document_keywords(self, doc_index: int, top_n: int = 15) -> List[Tuple[str, float]]:
        doc_vector = self.tfidf_matrix[doc_index].toarray().flatten()
        top_indices = doc_vector.argsort()[-top_n:][::-1]
        return [(self.feature_names[i], float(doc_vector[i])) for i in top_indices if doc_vector[i] > 0]
    
    def extract_corpus_keywords(self, top_n: int = 30) -> List[Tuple[str, float]]:
        mean_tfidf = np.asarray(self.tfidf_matrix.mean(axis=0)).flatten()
        top_indices = mean_tfidf.argsort()[-top_n:][::-1]
        return [(self.feature_names[i], float(mean_tfidf[i])) for i in top_indices]
    
    def get_discriminant_terms(self, doc_index: int, top_n: int = 10) -> List[Tuple[str, float]]:
        doc_vector = self.tfidf_matrix[doc_index].toarray().flatten()
        mean_vector = np.asarray(self.tfidf_matrix.mean(axis=0)).flatten()
        
        discrimination_score = doc_vector - mean_vector
        top_indices = discrimination_score.argsort()[-top_n:][::-1]
        
        return [(self.feature_names[i], float(discrimination_score[i])) 
                for i in top_indices if discrimination_score[i] > 0]
    
    def analyze_all_documents(self, articles: List[Dict], top_n: int = 15) -> List[Dict]:
        results = []
        for i, article in enumerate(articles):
            keywords = self.extract_document_keywords(i, top_n)
            discriminant = self.get_discriminant_terms(i, 10)
            
            results.append({
                'doc_index': i,
                'titre': article.get('titre', 'Sans titre'),
                'source': article.get('source', 'Unknown'),
                'keywords': keywords,
                'discriminant_terms': discriminant,
                'nb_tokens': article.get('nb_tokens', 0)
            })
        return results
