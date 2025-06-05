"""
VaahAI Agent Architecture

This module provides the core agent architecture for VaahAI, focusing on
reusability and extensibility through well-defined interfaces and design patterns.

The architecture follows an MVP approach, exposing only the essential components
needed for the initial implementation while maintaining the foundation for future extensions.
"""

# Core interfaces
from .interfaces import (
    IAgent,
    IMessageProcessor,
    ITool,
    IGroupChat,
    IAgentAdapter,
    IGroupChatAdapter,
    IConfig
)

# Base implementations
from .base import (
    BaseAgent,
    AgentDecorator,
    BaseMessageProcessor,
    ChainedMessageProcessor,
    BaseTool,
    BaseGroupChat
)

# Adapter layer for Autogen integration
from .adapters import (
    AutogenAgentAdapter,
    AutogenGroupChatAdapter,
    AutogenToolAdapter,
    AdapterFactory
)

# Factory pattern for object creation
from .factory import (
    AgentFactory,
    GroupChatFactory,
    ToolFactory,
    FactoryProvider
)

# Configuration system
from .config import (
    AgentConfig,
    GroupChatConfig,
    ToolConfig,
    AdapterConfig,
    ConfigFactory
)

# Version information
__version__ = "0.1.0"
