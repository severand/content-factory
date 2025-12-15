"""
Web Parser - Парсер веб-страниц с BeautifulSoup
"""

import logging
import aiohttp
from bs4 import BeautifulSoup
from typing import List
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from core.interfaces.parser_interface import (
    ParserInterface,
    ParserType,
    ParsedItem,
    ParserConfig
)

logger = logging.getLogger(__name__)

class WebParser(ParserInterface):
    """Парсер HTML страниц"""
    
    @property
    def parser_type(self) -> ParserType:
        return ParserType.WEB
    
    @property
    def parser_name(self) -> str:
        return "web_parser"
    
    @property
    def parser_version(self) -> str:
        return "1.0.0"
    
    @property
    def parser_description(self) -> str:
        return "🖤️ HTML web page parser using BeautifulSoup"
    
    async def initialize(self, config: ParserConfig) -> None:
        """Оинициализация"""
        self.config = config
        self.css_selectors = config.get('css_selectors', {})
        logger.info(f"✅ {self.parser_name} initialized")
    
    async def parse(self, source: str) -> List[ParsedItem]:
        """Парсить HTML страницу"""
        items = []
        
        try:
            logger.info(f"🖤️ Parsing web page from {source}")
            
            # Загружаем HTML
            html = await self._fetch_url(source)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Парсим элементы
            article_selector = self.css_selectors.get('articles', 'article')
            article_elements = soup.select(article_selector)[:10]
            
            for article in article_elements:
                try:
                    item = ParsedItem()
                    
                    # Основные ноля
                    title_selector = self.css_selectors.get('title', 'h1, h2, .title')
                    title_elem = article.select_one(title_selector)
                    item['title'] = title_elem.get_text(strip=True) if title_elem else 'No title'
                    
                    content_selector = self.css_selectors.get('content', 'p, .content, .description')
                    content_elem = article.select_one(content_selector)
                    item['content'] = content_elem.get_text(strip=True) if content_elem else 'No content'
                    
                    link_elem = article.find('a', href=True)
                    item['url'] = link_elem['href'] if link_elem else ''
                    
                    item['source'] = source
                    item['type'] = 'web_item'
                    
                    items.append(item)
                
                except Exception as e:
                    logger.warning(f"⚠️ Error parsing article: {e}")
                    continue
            
            logger.info(f"✅ Parsed {len(items)} items from web page")
        
        except Exception as e:
            logger.error(f"❌ Error parsing web page: {e}")
            raise
        
        return items
    
    async def validate_source(self, source: str) -> bool:
        """Проверить URL"""
        return source.startswith('http')
    
    async def test_connection(self) -> bool:
        """Проверить соединение"""
        return True
    
    async def _fetch_url(self, url: str) -> str:
        """Загрузить HTML"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=15),
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                ) as resp:
                    if resp.status == 200:
                        return await resp.text()
                    else:
                        raise Exception(f"HTTP {resp.status}")
        except Exception as e:
            logger.error(f"❌ Failed to fetch {url}: {e}")
            raise
    
    def get_config_schema(self):
        """Конфиг схема"""
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL веб-страницы"
                },
                "css_selectors": {
                    "type": "object",
                    "description": "CSS селекторы",
                    "properties": {
                        "articles": {"type": "string"},
                        "title": {"type": "string"},
                        "content": {"type": "string"}
                    }
                }
            },
            "required": ["url"]
        }
