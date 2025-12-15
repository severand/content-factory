"""
RSS Parser - Полностью работающий парсер RSS
"""

import logging
import feedparser
import aiohttp
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

class RSSParser(ParserInterface):
    """Парсер RSS лент"""
    
    @property
    def parser_type(self) -> ParserType:
        return ParserType.RSS
    
    @property
    def parser_name(self) -> str:
        return "rss_parser"
    
    @property
    def parser_version(self) -> str:
        return "1.0.0"
    
    @property
    def parser_description(self) -> str:
        return "📂 Universal RSS parser for news feeds"
    
    async def initialize(self, config: ParserConfig) -> None:
        """Оинициализация"""
        self.config = config
        logger.info(f"✅ {self.parser_name} initialized")
    
    async def parse(self, source: str) -> List[ParsedItem]:
        """Парсить RSS ленту"""
        items = []
        
        try:
            logger.info(f"🔍 Parsing RSS from {source}")
            
            # Загружаем RSS
            feed_content = await self._fetch_url(source)
            feed = feedparser.parse(feed_content)
            
            if feed.bozo:
                logger.warning(f"⚠️ RSS has parsing issues")
            
            # Парсим энтри
            for entry in feed.entries[:20]:
                item = ParsedItem()
                
                item['title'] = entry.get('title', 'No title')
                item['content'] = entry.get('summary', entry.get('description', 'No content'))
                item['url'] = entry.get('link', '')
                item['author'] = entry.get('author', 'Unknown')
                item['source'] = source
                item['source_name'] = feed.feed.get('title', 'Unknown Feed')
                item['type'] = 'rss_item'
                
                # Published date
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    from datetime import datetime
                    item['published_at'] = datetime(*entry.published_parsed[:6]).isoformat()
                
                items.append(item)
            
            logger.info(f"✅ Parsed {len(items)} items from RSS")
        
        except Exception as e:
            logger.error(f"❌ Error parsing RSS: {e}")
            raise
        
        return items
    
    async def validate_source(self, source: str) -> bool:
        """Проверить адрес RSS"""
        return source.startswith('http://') or source.startswith('https://')
    
    async def test_connection(self) -> bool:
        """Проверить соединение (всегда труе, т.k. RSS протокол)"""
        return True
    
    async def _fetch_url(self, url: str) -> str:
        """Загрузить содержимое URL"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=10),
                    headers={'User-Agent': 'Mozilla/5.0 (Content Factory RSS Parser)'}
                ) as resp:
                    if resp.status == 200:
                        return await resp.text()
                    else:
                        raise Exception(f"HTTP {resp.status}")
        except Exception as e:
            logger.error(f"❌ Failed to fetch URL {url}: {e}")
            raise
    
    def get_config_schema(self):
        """Конфиг схема"""
        return {
            "type": "object",
            "properties": {
                "rss_url": {
                    "type": "string",
                    "description": "URL к RSS ленте"
                }
            },
            "required": ["rss_url"]
        }
