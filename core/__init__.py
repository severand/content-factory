"""
Content Factory Core Module
Основной модуль с интерфейсами и системой регистрации
"""

__version__ = "1.0.0"
__author__ = "severand"

from core.registry.registries_manager import RegistriesManager

# Глобальный менеджер реестров
registries_manager = RegistriesManager()

__all__ = ["registries_manager"]
