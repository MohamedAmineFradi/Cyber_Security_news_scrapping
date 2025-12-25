from typing import List
import logging

logger = logging.getLogger(__name__)


class Lemmatizer:
    def __init__(self):
        try:
            import nltk
            from nltk.stem import WordNetLemmatizer
            try:
                self.lemmatizer = WordNetLemmatizer()
                self.lemmatizer.lemmatize('test')
            except LookupError:
                logger.warning("NLTK wordnet non disponible, téléchargement...")
                nltk.download('wordnet', quiet=True)
                nltk.download('omw-1.4', quiet=True)
                self.lemmatizer = WordNetLemmatizer()
        except Exception as e:
            logger.error(f"Erreur initialisation lemmatizer: {e}")
            self.lemmatizer = None
    
    def lemmatize(self, tokens: List[str]) -> List[str]:
        if not self.lemmatizer:
            return tokens
        return [self.lemmatizer.lemmatize(token) for token in tokens]


class Stemmer:
    def __init__(self):
        try:
            from nltk.stem import PorterStemmer
            self.stemmer = PorterStemmer()
        except Exception as e:
            logger.error(f"Erreur initialisation stemmer: {e}")
            self.stemmer = None
    
    def stem(self, tokens: List[str]) -> List[str]:
        if not self.stemmer:
            return tokens
        return [self.stemmer.stem(token) for token in tokens]
