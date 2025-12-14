"""Интерфейсы для всех компонентов системы"""

from core.interfaces.parser_interface import ParserInterface, ParserType, ParsedItem, ParserConfig
from core.interfaces.llm_interface import LLMInterface, LLMConfig, Message
from core.interfaces.social_interface import SocialNetworkInterface, PostType
from core.interfaces.agent_interface import AgentInterface, AgentRole

__all__ = [
    "ParserInterface",
    "ParserType", 
    "ParsedItem",
    "ParserConfig",
    "LLMInterface",
    "LLMConfig",
    "Message",
    "SocialNetworkInterface",
    "PostType",
    "AgentInterface",
    "AgentRole",
]
