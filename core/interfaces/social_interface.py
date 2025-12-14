"""Основной интерфейс для соц сетей
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from enum import Enum

class PostType(str, Enum):
    """Types of posts"""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    STORY = "story"

class SocialNetworkInterface(ABC):
    """Основной интерфейс для соц сетей"""
    
    @property
    @abstractmethod
    def network_name(self) -> str:
        """Название соц сети"""
        pass
    
    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Инициализация"""
        pass
    
    @abstractmethod
    async def publish(
        self,
        content: str,
        post_type: PostType = PostType.TEXT,
        attachments: Optional[List[str]] = None,
        schedule_time: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Опубликовать пост
        """
        pass
    
    @abstractmethod
    async def get_analytics(
        self,
        post_id: str
    ) -> Dict[str, Any]:
        """Получить аналитику поста"""
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Проверить соединение"""
        pass
    
    def get_supported_types(self) -> List[PostType]:
        """Поддерживаемые типы постов"""
        return [PostType.TEXT]
    
    def get_max_content_length(self) -> int:
        """Макс длина контента"""
        return 280
