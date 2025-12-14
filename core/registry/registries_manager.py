"""Менеджер всех реестров
"""

import logging
from core.registry.parser_registry import ParserRegistry
from core.registry.llm_registry import LLMRegistry
from core.registry.agent_registry import AgentRegistry
from core.registry.social_registry import SocialNetworkRegistry

logger = logging.getLogger(__name__)

class RegistriesManager:
    """Объединяет все реестры"""
    
    def __init__(self):
        self.parser_registry = ParserRegistry()
        self.llm_registry = LLMRegistry()
        self.agent_registry = AgentRegistry()
        self.social_registry = SocialNetworkRegistry()
        
        logger.info("🏗️ Менеджер регистров инициализирован")
    
    def auto_discover_all(self, modules_path: str = "modules") -> None:
        """Автообнаружение всех модулей"""
        logger.info("🔍 Начинаю поиск модулей...")
        
        self.parser_registry.auto_discover_parsers(modules_path)
        # Остальные реестры аналогично
        
        logger.info("✅ Поиск модулей завершён")
    
    def get_stats(self) -> dict:
        """Получить статистику"""
        return {
            "parsers": len(self.parser_registry._parsers),
            "llm_providers": len(self.llm_registry._providers),
            "agents": len(self.agent_registry._agents),
            "social_networks": len(self.social_registry._networks)
        }
