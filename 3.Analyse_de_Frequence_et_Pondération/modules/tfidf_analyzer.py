from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDFAnalyzer:
    def __init__(self, max_features: int = None, min_df: int = 2, max_df: float = 0.95):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            token_pattern=None,
            tokenizer=lambda x: x,
            preprocessor=lambda x: x,
            lowercase=False
        )
        self.tfidf_matrix = None
        self.feature_names = None
        
    def fit_transform(self, documents: List[List[str]]) -> np.ndarray:
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
        self.feature_names = self.vectorizer.get_feature_names_out()
        return self.tfidf_matrix
    
    def get_top_terms_per_document(self, doc_index: int, top_n: int = 10) -> List[Tuple[str, float]]:
        if self.tfidf_matrix is None:
            raise ValueError("Must call fit_transform first")
        
        doc_vector = self.tfidf_matrix[doc_index].toarray().flatten()
        top_indices = doc_vector.argsort()[-top_n:][::-1]
        
        return [(self.feature_names[i], doc_vector[i]) for i in top_indices if doc_vector[i] > 0]
    
    def get_top_terms_corpus(self, top_n: int = 20) -> List[Tuple[str, float]]:
        if self.tfidf_matrix is None:
            raise ValueError("Must call fit_transform first")
        
        mean_tfidf = np.asarray(self.tfidf_matrix.mean(axis=0)).flatten()
        top_indices = mean_tfidf.argsort()[-top_n:][::-1]
        
        return [(self.feature_names[i], mean_tfidf[i]) for i in top_indices]
    
    def get_document_keywords(self, documents: List[List[str]], top_n: int = 10) -> List[Dict]:
        results = []
        for i in range(len(documents)):
            keywords = self.get_top_terms_per_document(i, top_n)
            results.append({
                'doc_index': i,
                'keywords': keywords
            })
        return results
