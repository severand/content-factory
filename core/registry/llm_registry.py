"""Реестр LLM провайдеров
"""

from typing import Dict, Type, Optional, List
from core.interfaces.llm_interface import LLMInterface
import logging

logger = logging.getLogger(__name__)

class LLMRegistry:
    """Регистр LLM провайдеров"""
    
    def __init__(self):
        self._providers: Dict[str, Type[LLMInterface]] = {}
        self._instances: Dict[str, LLMInterface] = {}
    
    def register(self, provider_class: Type[LLMInterface]) -> None:
        """Регистрировать провайдер"""
        try:
            instance = provider_class()
            name = instance.provider_name
            
            self._providers[name] = provider_class
            logger.info(f"✅ LLM провайдер {name} регистрирован")
        except Exception as e:
            logger.error(f"❌ Ошибка регистрации: {e}")
    
    def get_provider(self, name: str) -> Optional[LLMInterface]:
        """Получить провайдер"""
        if name not in self._instances:
            provider_class = self._providers.get(name)
            if not provider_class:
                return None
            self._instances[name] = provider_class()
        return self._instances[name]
    
    def list_providers(self) -> List[str]:
        """Нсписок всех провайдеров"""
        return list(self._providers.keys())
