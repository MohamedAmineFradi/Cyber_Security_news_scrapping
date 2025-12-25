import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la récupération de {url}: {e}")
            return None
    
    def scrape(self, max_articles: int = 50) -> List[Dict]:
        raise NotImplementedError("Méthode à implémenter par les sous-classes")
    
    def extract_article(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        raise NotImplementedError("Méthode à implémenter par les sous-classes")
