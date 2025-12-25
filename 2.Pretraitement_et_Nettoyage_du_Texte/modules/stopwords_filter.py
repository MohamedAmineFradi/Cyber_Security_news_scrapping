from typing import List
import logging

logger = logging.getLogger(__name__)


class StopWordsFilter:
    def __init__(self, language: str = 'english'):
        self.language = language
        self.stop_words = self._load_stop_words()
    
    def _load_stop_words(self) -> set:
        try:
            import nltk
            try:
                from nltk.corpus import stopwords
                return set(stopwords.words(self.language))
            except LookupError:
                logger.warning("NLTK stopwords non disponibles, téléchargement...")
                nltk.download('stopwords', quiet=True)
                from nltk.corpus import stopwords
                return set(stopwords.words(self.language))
        except Exception as e:
            logger.error(f"Erreur chargement stopwords: {e}")
            return set()
    
    def filter(self, tokens: List[str]) -> List[str]:
        return [token for token in tokens if token not in self.stop_words and len(token) > 2]
