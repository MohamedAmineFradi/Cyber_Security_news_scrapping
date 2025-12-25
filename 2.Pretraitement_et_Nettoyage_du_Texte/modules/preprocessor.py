from typing import List, Dict
from .normalizer import TextNormalizer
from .tokenizer import Tokenizer
from .stopwords_filter import StopWordsFilter
from .lemmatizer import Lemmatizer, Stemmer


class TextPreprocessor:
    def __init__(self, use_lemmatization: bool = True, use_stemming: bool = False):
        self.normalizer = TextNormalizer()
        self.tokenizer = Tokenizer()
        self.stop_words_filter = StopWordsFilter(language='english')
        self.lemmatizer = Lemmatizer() if use_lemmatization else None
        self.stemmer = Stemmer() if use_stemming else None
    
    def preprocess_text(self, text: str) -> List[str]:
        text = self.normalizer.process(text)
        tokens = self.tokenizer.tokenize(text)
        tokens = self.stop_words_filter.filter(tokens)
        
        if self.lemmatizer:
            tokens = self.lemmatizer.lemmatize(tokens)
        elif self.stemmer:
            tokens = self.stemmer.stem(tokens)
        
        return tokens
    
    def preprocess_article(self, article: Dict) -> Dict:
        titre_tokens = self.preprocess_text(article.get('titre', ''))
        contenu_tokens = self.preprocess_text(article.get('contenu', ''))
        
        return {
            'source': article.get('source', ''),
            'url': article.get('url', ''),
            'titre': article.get('titre', ''),
            'titre_tokens': titre_tokens,
            'date': article.get('date', ''),
            'auteur': article.get('auteur', ''),
            'contenu_original': article.get('contenu', ''),
            'contenu_tokens': contenu_tokens,
            'nb_tokens': len(contenu_tokens),
            'date_extraction': article.get('date_extraction', '')
        }
