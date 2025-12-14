"""Реестр агентов
"""

from typing import Dict, Type, Optional, List
from core.interfaces.agent_interface import AgentInterface
import logging

logger = logging.getLogger(__name__)

class AgentRegistry:
    """Регистр агентов"""
    
    def __init__(self):
        self._agents: Dict[str, Type[AgentInterface]] = {}
        self._instances: Dict[str, AgentInterface] = {}
    
    def register(self, agent_class: Type[AgentInterface]) -> None:
        """Регистрировать агент"""
        try:
            instance = agent_class()
            name = instance.agent_name
            
            self._agents[name] = agent_class
            logger.info(f"✅ Агент {name} регистрирован")
        except Exception as e:
            logger.error(f"❌ Ошибка регистрации: {e}")
    
    def get_agent(self, name: str) -> Optional[AgentInterface]:
        """Получить агент"""
        if name not in self._instances:
            agent_class = self._agents.get(name)
            if not agent_class:
                return None
            self._instances[name] = agent_class()
        return self._instances[name]
    
    def list_agents(self) -> List[str]:
        """Нсписок всех агентов"""
        return list(self._agents.keys())
