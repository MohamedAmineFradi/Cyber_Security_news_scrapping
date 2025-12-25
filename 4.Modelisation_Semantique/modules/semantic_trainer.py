from typing import List, Optional, Tuple
from gensim.models import Word2Vec
import logging

logger = logging.getLogger(__name__)


class SemanticModelTrainer:
    def __init__(self, vector_size: int = 200, window: int = 5, min_count: int = 2, 
                 sg: int = 1, epochs: int = 10, workers: int = 4):
        self.vector_size = vector_size
        self.window = window
        self.min_count = min_count
        self.sg = sg
        self.epochs = epochs
        self.workers = workers
        self.model = None
    
    def train(self, sentences: List[List[str]]) -> Word2Vec:
        logger.info(f"Entraînement Word2Vec (sg={self.sg}, vector_size={self.vector_size})")
        logger.info(f"  - Fenêtre: {self.window}, Min count: {self.min_count}")
        logger.info(f"  - Époque: {self.epochs}, Workers: {self.workers}")
        
        self.model = Word2Vec(
            sentences=sentences,
            vector_size=self.vector_size,
            window=self.window,
            min_count=self.min_count,
            sg=self.sg,
            epochs=self.epochs,
            workers=self.workers,
            seed=42
        )
        
        logger.info(f"Vocabulaire: {len(self.model.wv)} mots")
        return self.model
    
    def save(self, filepath: str):
        if self.model is None:
            raise ValueError("Model not trained yet")
        self.model.save(filepath)
        logger.info(f"Modèle sauvegardé: {filepath}")
    
    def load(self, filepath: str):
        self.model = Word2Vec.load(filepath)
        logger.info(f"Modèle chargé: {filepath}")
        return self.model
    
    def get_model(self) -> Word2Vec:
        if self.model is None:
            raise ValueError("Model not trained yet")
        return self.model
