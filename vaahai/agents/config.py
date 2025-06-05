"""
VaahAI Agent Configuration

This module provides configuration classes for agents, group chats, and related components.
These classes implement the IConfig interface and provide structured configuration
with validation, enhancing reusability and extensibility by separating configuration
from implementation.

This file re-exports all configuration classes from the config package for backward compatibility.
"""

# Re-export all configuration classes from the config package
from .config.base import BaseConfig
from .config.agent import AgentConfig, AutogenAgentConfig
from .config.group_chat import GroupChatConfig, AutogenGroupChatConfig
from .config.tool import ToolConfig, AutogenToolConfig
from .config.adapter import AdapterConfig
from .config.llm import LLMConfig
from .config.factory import ConfigFactory

# Re-export IConfig from interfaces for backward compatibility
from .interfaces import IConfig

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
