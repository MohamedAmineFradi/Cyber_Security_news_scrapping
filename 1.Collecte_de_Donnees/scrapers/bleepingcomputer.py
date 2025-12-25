from .base import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urljoin
import logging
import time

logger = logging.getLogger(__name__)


class BleepingComputerScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.bleepingcomputer.com"
        self.source_name = "BleepingComputer"
    
    def scrape(self, max_articles: int = 50) -> List[Dict]:
        logger.info(f"Scraping {self.source_name}...")
        articles = []
        
        category_url = f"{self.base_url}/news/security/"
        soup = self.get_page(category_url)
        
        if not soup:
            return articles
        
        article_items = soup.find_all('h4')
        if not article_items:
            article_section = soup.find('div', id='bc_latest_news')
            if article_section:
                article_items = article_section.find_all('a', href=True)
        
        count = 0
        for item in article_items:
            if count >= max_articles:
                break
            
            try:
                if item.name == 'a':
                    link = item
                else:
                    link = item.find('a')
                
                if not link:
                    continue
                
                article_url = link.get('href')
                if not article_url or 'javascript' in article_url:
                    continue
                
                if not article_url.startswith('http'):
                    article_url = urljoin(self.base_url, article_url)
                
                if '/news/' not in article_url:
                    continue
                
                logger.info(f"Extraction de: {article_url}")
                article_soup = self.get_page(article_url)
                
                if article_soup:
                    article = self.extract_article(article_soup, article_url)
                    if article and article.get('contenu'):
                        articles.append(article)
                        count += 1
                
                time.sleep(1)
            
            except Exception as e:
                logger.error(f"Erreur lors de l'extraction: {e}")
                continue
        
        return articles
    
    def extract_article(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        try:
            title_elem = soup.find('h1', class_='article_title')
            title = title_elem.get_text(strip=True) if title_elem else "Titre non trouvé"
            
            date_elem = soup.find('time')
            date = date_elem.get('datetime', '') if date_elem else ""
            
            author_elem = soup.find('a', rel='author')
            author = author_elem.get_text(strip=True) if author_elem else "Auteur inconnu"
            
            content_elem = soup.find('div', class_='articleBody')
            if content_elem:
                for script in content_elem(['script', 'style', 'aside']):
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
