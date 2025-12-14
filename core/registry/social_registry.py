"""Реестр соц сетей
"""

from typing import Dict, Type, Optional, List
from core.interfaces.social_interface import SocialNetworkInterface
import logging

logger = logging.getLogger(__name__)

class SocialNetworkRegistry:
    """Регистр соц сетей"""
    
    def __init__(self):
        self._networks: Dict[str, Type[SocialNetworkInterface]] = {}
        self._instances: Dict[str, SocialNetworkInterface] = {}
    
    def register(self, network_class: Type[SocialNetworkInterface]) -> None:
        """Регистрировать соц сеть"""
        try:
            instance = network_class()
            name = instance.network_name
            
            self._networks[name] = network_class
            logger.info(f"✅ Соц сеть {name} регистрирована")
        except Exception as e:
            logger.error(f"❌ Ошибка регистрации: {e}")
    
    def get_network(self, name: str) -> Optional[SocialNetworkInterface]:
        """Получить соц сеть"""
        if name not in self._instances:
            network_class = self._networks.get(name)
            if not network_class:
                return None
            self._instances[name] = network_class()
        return self._instances[name]
    
    def list_networks(self) -> List[str]:
        """Нсписок всех соц сетей"""
        return list(self._networks.keys())
