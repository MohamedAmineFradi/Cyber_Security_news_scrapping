import re
import string


class TextNormalizer:
    def __init__(self):
        self.punctuation = string.punctuation
    
    def normalize(self, text: str) -> str:
        return text.lower()
    
    def remove_urls(self, text: str) -> str:
        return re.sub(r'http\S+|www\.\S+', '', text)
    
    def remove_emails(self, text: str) -> str:
        return re.sub(r'\S+@\S+', '', text)
    
    def remove_numbers(self, text: str) -> str:
        return re.sub(r'\d+', '', text)
    
    def remove_punctuation(self, text: str) -> str:
        return text.translate(str.maketrans('', '', self.punctuation))
    
    def remove_extra_spaces(self, text: str) -> str:
        return ' '.join(text.split())
    
    def process(self, text: str) -> str:
        text = self.normalize(text)
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        text = self.remove_numbers(text)
        text = self.remove_punctuation(text)
        text = self.remove_extra_spaces(text)
        return text
