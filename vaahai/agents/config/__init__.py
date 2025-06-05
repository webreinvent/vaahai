"""
VaahAI Agent Configuration Package

This package provides configuration classes for agents, group chats, tools, adapters, and LLMs.
These classes implement the IConfig interface and provide structured configuration
with validation, enhancing reusability and extensibility by separating configuration
from implementation.
"""

from .base import BaseConfig, IConfig
from .agent import AgentConfig, AutogenAgentConfig
from .group_chat import GroupChatConfig, AutogenGroupChatConfig
from .tool import ToolConfig, AutogenToolConfig
from .adapter import AdapterConfig
from .llm import LLMConfig
from .factory import ConfigFactory

__all__ = [
    'IConfig',
    'BaseConfig',
    'AgentConfig',
    'GroupChatConfig',
    'ToolConfig',
    'AdapterConfig',
    'AutogenAgentConfig',
    'AutogenGroupChatConfig',
    'AutogenToolConfig',
    'LLMConfig',
    'ConfigFactory'
]
