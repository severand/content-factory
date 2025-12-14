"""Реестр парсеров
"""

from typing import Dict, Type, Optional, List
from core.interfaces.parser_interface import ParserInterface, ParserMetadata
import importlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ParserRegistry:
    """Нреестр парсеров"""
    
    def __init__(self):
        self._parsers: Dict[str, Type[ParserInterface]] = {}
        self._metadata: Dict[str, ParserMetadata] = {}
        self._instances: Dict[str, ParserInterface] = {}
    
    def register(self, parser_class: Type[ParserInterface]) -> None:
        """Регистрировать парсер"""
        try:
            instance = parser_class()
            name = instance.parser_name
            
            self._parsers[name] = parser_class
            self._metadata[name] = ParserMetadata(instance)
            
            logger.info(f"✅ Парсер {name} регистрирован")
        except Exception as e:
            logger.error(f"❌ Ошибка регистрации: {e}")
    
    def get_parser(self, name: str) -> Optional[ParserInterface]:
        """Получить парсер"""
        if name not in self._instances:
            parser_class = self._parsers.get(name)
            if not parser_class:
                return None
            self._instances[name] = parser_class()
        return self._instances[name]
    
    def list_parsers(self) -> List[Dict]:
        """Нсписок всех парсеров"""
        return [self._metadata[name].to_dict() for name in self._parsers.keys()]
    
    def auto_discover_parsers(self, modules_path: str) -> None:
        """Автоматически обнаружить парсеры"""
        parsers_dir = Path(modules_path) / "parsers"
        
        if not parsers_dir.exists():
            logger.warning(f"❌ Папка {parsers_dir} не найдена")
            return
        
        for parser_dir in parsers_dir.iterdir():
            if not parser_dir.is_dir() or parser_dir.name.startswith('_'):
                continue
            
            try:
                module = importlib.import_module(
                    f"modules.parsers.{parser_dir.name}.parser"
                )
                
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, ParserInterface) and 
                        attr != ParserInterface):
                        self.register(attr)
            
            except Exception as e:
                logger.error(f"❌ Ошибка нагрузки {parser_dir.name}: {e}")
