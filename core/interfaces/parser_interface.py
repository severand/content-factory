"""Основной интерфейс для всех парсеров
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
import uuid

class ParserType(str, Enum):
    """Типы парсеров"""
    RSS = "rss"
    WEB = "web"
    API = "api"
    SELENIUM = "selenium"
    CUSTOM = "custom"

class ParsedItem(dict):
    """Единица спарсённых данных"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['id'] = str(uuid.uuid4())
        self['parsed_at'] = datetime.now().isoformat()
        self['source'] = None
        self['type'] = 'item'

class ParserConfig(dict):
    """Конфиг парсера"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setdefault('enabled', True)
        self.setdefault('timeout', 10)
        self.setdefault('retry_count', 3)
        self.setdefault('cache_duration', 3600)

class ParserInterface(ABC):
    """Базовый интерфейс для всех парсеров"""
    
    @property
    @abstractmethod
    def parser_type(self) -> ParserType:
        """Тип парсера"""
        pass
    
    @property
    @abstractmethod
    def parser_name(self) -> str:
        """Уникальное имя парсера"""
        pass
    
    @property
    @abstractmethod
    def parser_version(self) -> str:
        """Версия парсера"""
        pass
    
    @property
    @abstractmethod
    def parser_description(self) -> str:
        """Описание парсера"""
        pass
    
    @abstractmethod
    async def initialize(self, config: ParserConfig) -> None:
        """Инициализация парсера"""
        pass
    
    @abstractmethod
    async def parse(self, source: str) -> List[ParsedItem]:
        """
        Спарсить источник
        
        Args:
            source: URL или путь до источника
        
        Returns:
            Нсписок спарсённых элементов
        """
        pass
    
    @abstractmethod
    async def validate_source(self, source: str) -> bool:
        """Валидировать источник"""
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Проверить соединение"""
        pass
    
    async def cleanup(self) -> None:
        """Очистка ресурсов"""
        pass
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Вернуть JSON schema конфига парсера"""
        return {}

class ParserMetadata:
    """Метаданные парсера"""
    
    def __init__(self, parser: ParserInterface):
        self.name = parser.parser_name
        self.type = parser.parser_type
        self.version = parser.parser_version
        self.description = parser.parser_description
        self.config_schema = parser.get_config_schema()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'type': self.type.value,
            'version': self.version,
            'description': self.description,
            'config_schema': self.config_schema
        }
