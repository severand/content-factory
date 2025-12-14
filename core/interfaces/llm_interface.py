"""Основной интерфейс для LLM провайдеров
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator

class Message:
    """Сообщение для LLM"""
    def __init__(self, role: str, content: str):
        self.role = role  # "user", "assistant", "system"
        self.content = content

class LLMConfig(dict):
    """Конфиг LLM"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setdefault('model', None)
        self.setdefault('temperature', 0.7)
        self.setdefault('max_tokens', 2048)
        self.setdefault('top_p', 1.0)

class LLMInterface(ABC):
    """Основной интерфейс для LLM провайдеров"""
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Имя провайдера"""
        pass
    
    @abstractmethod
    async def initialize(self, config: LLMConfig) -> None:
        """Инициализация"""
        pass
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Генерировать текст"""
        pass
    
    @abstractmethod
    async def generate_streaming(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Генерировать текст с потоком"""
        pass
    
    @abstractmethod
    async def chat(
        self,
        messages: List[Message],
        **kwargs
    ) -> str:
        """Chat mode"""
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Проверить соединение"""
        pass
    
    def get_available_models(self) -> List[str]:
        """Список доступных моделей"""
        return []
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Вернуть JSON schema конфига"""
        return {}
