"""Регистры модулей"""

from core.registry.parser_registry import ParserRegistry
from core.registry.llm_registry import LLMRegistry  
from core.registry.agent_registry import AgentRegistry
from core.registry.social_registry import SocialNetworkRegistry

__all__ = [
    "ParserRegistry",
    "LLMRegistry",
    "AgentRegistry",
    "SocialNetworkRegistry"
]
