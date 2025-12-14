"""Основной интерфейс для агентов
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum

class AgentRole(str, Enum):
    """Роли агентов"""
    CONTENT_GENERATOR = "content_generator"
    NEWS_PROCESSOR = "news_processor"
    EDITOR = "editor"
    PUBLISHER = "publisher"
    ANALYST = "analyst"
    SCHEDULER = "scheduler"
    VALIDATOR = "validator"

class AgentStatus(str, Enum):
    """Статусы агентов"""
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    PAUSED = "paused"

class AgentInterface(ABC):
    """Основной интерфейс для агентов"""
    
    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Название агента"""
        pass
    
    @property
    @abstractmethod
    def agent_role(self) -> AgentRole:
        """Роль агента"""
        pass
    
    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Инициализация"""
        pass
    
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнить задачу"""
        pass
    
    @abstractmethod
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Валидировать входные данные"""
        pass
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Вернуть JSON schema конфига"""
        return {}
