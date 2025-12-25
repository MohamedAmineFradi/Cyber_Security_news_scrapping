from typing import List, Dict, Tuple, Optional
from gensim.models import Word2Vec
import logging

logger = logging.getLogger(__name__)


class SemanticExplorer:
    def __init__(self, model: Word2Vec):
        self.model = model
        self.wv = model.wv
    
    def get_similar_words(self, word: str, top_n: int = 10) -> List[Tuple[str, float]]:
        try:
            similarities = self.wv.most_similar(word, topn=top_n)
            return [(w, float(sim)) for w, sim in similarities]
        except KeyError:
            logger.warning(f"Mot '{word}' non trouvé dans le vocabulaire")
            return []
    
    def get_word_vector(self, word: str) -> Optional[List[float]]:
        try:
            vector = self.wv[word]
            return vector.tolist()
        except KeyError:
            logger.warning(f"Mot '{word}' non trouvé dans le vocabulaire")
            return None
    
    def word_similarity(self, word1: str, word2: str) -> Optional[float]:
        try:
            sim = self.wv.similarity(word1, word2)
            return float(sim)
        except KeyError:
            logger.warning(f"L'un des mots '{word1}' ou '{word2}' non trouvé")
            return None
    
    def get_analogy(self, word1: str, word2: str, word3: str, top_n: int = 5) -> List[Tuple[str, float]]:
        try:
            results = self.wv.most_similar(positive=[word2, word3], negative=[word1], topn=top_n)
            return [(w, float(sim)) for w, sim in results]
        except KeyError as e:
            logger.warning(f"Analogie échouée: {e}")
            return []
    
    def explore_related_words(self, word: str, top_n: int = 15) -> Dict:
        return {
            'word': word,
            'similar_words': self.get_similar_words(word, top_n),
            'vocabulary_size': len(self.wv)
        }
    
    def test_analogies(self) -> List[Dict]:
        test_analogies = [
            ('cloud', 'aws', 'microsoft', 'azure'),
            ('ransomware', 'encrypt', 'malware', 'virus'),
            ('network', 'internet', 'system', 'computer'),
            ('database', 'sql', 'file', 'storage'),
        ]
        
        results = []
        for word1, word2, word3, expected in test_analogies:
            analogy_results = self.get_analogy(word1, word2, word3, top_n=3)
            results.append({
                'analogy': f"{word2} - {word1} ≈ {word3} - ?",
                'expected': expected,
                'predicted': [w for w, _ in analogy_results],
                'scores': [float(s) for _, s in analogy_results]
            })
        
        return results
    
    def analyze_vocabulary(self, top_n: int = 30) -> Dict:
        all_words = list(self.wv.index_to_key[:top_n])
        
        word_info = []
        for word in all_words:
            word_info.append({
                'word': word,
                'frequency_rank': self.wv.get_index(word)
            })
        
        return {
            'vocabulary_size': len(self.wv),
            'vector_size': self.model.vector_size,
            'top_words': word_info
        }
