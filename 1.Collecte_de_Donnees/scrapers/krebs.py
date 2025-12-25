from .base import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urljoin
import logging
import time

logger = logging.getLogger(__name__)


class KrebsScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://krebsonsecurity.com"
        self.source_name = "Krebs on Security"
    
    def scrape(self, max_articles: int = 50) -> List[Dict]:
        logger.info(f"Scraping {self.source_name}...")
        articles = []
        
        soup = self.get_page(self.base_url)
        if not soup:
            logger.warning(f"Impossible d'accéder à {self.source_name}")
            return articles
        
        article_links = soup.find_all('h2', class_='entry-title')[:max_articles]
        
        for h2 in article_links:
            try:
                link = h2.find('a')
                if not link:
                    continue
                
                article_url = link.get('href')
                if not article_url.startswith('http'):
                    article_url = urljoin(self.base_url, article_url)
                
                logger.info(f"Extraction de: {article_url}")
                article_soup = self.get_page(article_url)
                
                if article_soup:
                    article = self.extract_article(article_soup, article_url)
                    if article and article.get('contenu'):
                        articles.append(article)
                
                time.sleep(1)
            
            except Exception as e:
                logger.error(f"Erreur lors de l'extraction: {e}")
                continue
        
        return articles
    
    def extract_article(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        try:
            title_elem = soup.find('h1', class_='entry-title')
            if not title_elem:
                title_elem = soup.find('h1')
            title = title_elem.get_text(strip=True) if title_elem else "Titre non trouvé"
            
            date_elem = soup.find('time', class_='entry-date')
            date = date_elem.get('datetime', '') if date_elem else ""
            
            author_elem = soup.find('span', class_='author')
            if not author_elem:
                author_elem = soup.find('a', rel='author')
            author = author_elem.get_text(strip=True) if author_elem else "Brian Krebs"
            
            content_elem = soup.find('div', class_='entry-content')
            if not content_elem:
                content_elem = soup.find('article')
            
            if content_elem:
                for script in content_elem(['script', 'style', 'aside', 'nav', 'iframe']):
                    script.decompose()
                content = content_elem.get_text(separator='\n', strip=True)
            else:
                content = ""
            
            return {
                'source': self.source_name,
                'url': url,
                'titre': title,
                'date': date,
                'auteur': author,
                'contenu': content,
                'date_extraction': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Erreur extraction données: {e}")
            return None
