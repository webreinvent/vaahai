"""
VaahAI Agent Factory

This module provides factory classes for creating agents, group chats, and related components.
The factory pattern centralizes object creation logic, enhancing reusability and extensibility
by decoupling client code from specific implementation details.
"""

import importlib
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Type, Union, Callable

from .interfaces import IAgent, IGroupChat, ITool, IPlugin, IRegistry
from .base import BaseAgent, BaseGroupChat, BaseTool
from .exceptions import AgentTypeNotFoundError, AgentInitializationError
from .impl import (
    ConversationalAgent,
    AssistantAgent,
    UserProxyAgent,
    SpecializedAgent,
    CodeReviewAgent,
    SecurityAuditAgent,
    LanguageDetectionAgent,
    ReportGenerationAgent
)


class Registry(IRegistry):
    """
    Generic registry for component registration and discovery.
    
    This class provides a way to register and discover components dynamically,
    enhancing extensibility by allowing components to be added at runtime.
    """
    
    def __init__(self):
        """Initialize a new registry."""
        self._components: Dict[str, Any] = {}
    
    def register(self, name: str, component: Any) -> None:
        """
        Register a component.
        
        Args:
            name: Name to register the component under
            component: The component to register
        """
        self._components[name] = component
    
    def get(self, name: str) -> Optional[Any]:
        """
        Get a registered component by name.
        
        Args:
            name: Name of the component to get
            
        Returns:
            The registered component, or None if not found
        """
        return self._components.get(name)
    
    def list_all(self) -> List[str]:
        """
        List all registered component names.
        
        Returns:
            List of registered component names
        """
        return list(self._components.keys())
    
    def unregister(self, name: str) -> None:
        """
        Unregister a component.
        
        Args:
            name: Name of the component to unregister
        """
        if name in self._components:
            del self._components[name]


class AgentRegistry(Registry):
    """Registry specifically for agent classes."""
    pass


class GroupChatRegistry(Registry):
    """Registry specifically for group chat classes."""
    pass


class ToolRegistry(Registry):
    """Registry specifically for tool classes."""
    pass


class PluginRegistry(Registry):
    """Registry specifically for plugin classes."""
    pass


class BaseFactory(ABC):
    """
    Abstract base class for all factories.
    
    This class provides common functionality for factories, such as
    component registration and discovery.
    """
    
    def __init__(self):
        """Initialize a new factory."""
        self._registry = self._create_registry()
    
    @abstractmethod
    def _create_registry(self) -> Registry:
        """
        Create a registry for this factory.
        
        Returns:
            A registry instance
        """
        pass
    
    def register_component(self, name: str, component: Any) -> None:
        """
        Register a component.
        
        Args:
            name: Name to register the component under
            component: The component to register
        """
        self._registry.register(name, component)
    
    def get_component(self, name: str) -> Optional[Any]:
        """
        Get a registered component by name.
        
        Args:
            name: Name of the component to get
            
        Returns:
            The registered component, or None if not found
        """
        return self._registry.get(name)
    
    def list_components(self) -> List[str]:
        """
        List all registered component names.
        
        Returns:
            List of registered component names
        """
        return self._registry.list_all()


class AgentFactory(BaseFactory):
    """
    Factory for creating agent instances.
    
    This factory provides methods for creating different types of agents,
    centralizing agent creation logic and enhancing extensibility.
    """
    
    def __init__(self):
        """Initialize a new agent factory."""
        super().__init__()
        self._decorators: Dict[str, Type] = {}
        
        # Register default agent implementations
        self._register_default_agents()
    
    def _create_registry(self) -> Registry:
        """
        Create a registry for this factory.
        
        Returns:
            An agent registry instance
        """
        return AgentRegistry()
    
    def _register_default_agents(self) -> None:
        """
        Register the default agent implementations.
        """
        self.register_agent_class("conversational", ConversationalAgent)
        self.register_agent_class("assistant", AssistantAgent)
        self.register_agent_class("user_proxy", UserProxyAgent)
        self.register_agent_class("specialized", SpecializedAgent)
        self.register_agent_class("code_review", CodeReviewAgent)
        self.register_agent_class("security_audit", SecurityAuditAgent)
        self.register_agent_class("language_detection", LanguageDetectionAgent)
        self.register_agent_class("report_generation", ReportGenerationAgent)
    
    def create_agent(self, agent_type: str, config: Dict[str, Any]) -> IAgent:
        """
        Create an agent of the specified type.
        
        Args:
            agent_type: Type of agent to create
            config: Agent configuration
            
        Returns:
            Agent instance
            
        Raises:
            AgentTypeNotFoundError: If the agent type is not registered
            AgentInitializationError: If there's an error initializing the agent
        """
        agent_class = self.get_component(agent_type)
        if agent_class is None:
            raise AgentTypeNotFoundError(agent_type)
        
        try:
            # Create the agent instance
            agent = agent_class()
            
            # Initialize the agent with the configuration
            agent.initialize(config)
            
            # Apply decorators if specified in the configuration
            if 'decorators' in config and isinstance(config['decorators'], list):
                for decorator_name in config['decorators']:
                    decorator_class = self.get_decorator(decorator_name)
                    if decorator_class is not None:
                        agent = decorator_class(agent)
            
            return agent
        except Exception as e:
            # Wrap any initialization errors in our custom exception
            # Use the agent name from the configuration if available
            agent_name = config.get('name', agent_type)
            # Include both agent type and name in the error message
            error_message = f"Failed to initialize {agent_type} agent '{agent_name}': {str(e)}"
            raise AgentInitializationError(agent_name, error_message)
    
    def register_agent_class(self, name: str, agent_class: Type[IAgent]) -> None:
        """
        Register an agent class.
        
        Args:
            name: Name to register the agent class under
            agent_class: The agent class to register
        """
        self.register_component(name, agent_class)
    
    def register_decorator(self, name: str, decorator_class: Type) -> None:
        """
        Register an agent decorator class.
        
        Args:
            name: Name to register the decorator class under
            decorator_class: The decorator class to register
        """
        self._decorators[name] = decorator_class
    
    def get_decorator(self, name: str) -> Optional[Type]:
        """
        Get a registered decorator class by name.
        
        Args:
            name: Name of the decorator class to get
            
        Returns:
            The registered decorator class, or None if not found
        """
        return self._decorators.get(name)
    
    def list_decorators(self) -> List[str]:
        """
        List all registered decorator names.
        
        Returns:
            List of decorator names
        """
        return list(self._decorators.keys())
    
    @classmethod
    def create_conversational_agent(cls, config: Dict[str, Any]) -> ConversationalAgent:
        """
        Create a conversational agent.
        
        Args:
            config: Agent configuration
            
        Returns:
            Conversational agent instance
        """
        factory = cls()
        return factory.create_agent("conversational", config)
    
    @classmethod
    def create_assistant_agent(cls, config: Dict[str, Any]) -> AssistantAgent:
        """
        Create an assistant agent.
        
        Args:
            config: Agent configuration
            
        Returns:
            Assistant agent instance
        """
        factory = cls()
        return factory.create_agent("assistant", config)
    
    @classmethod
    def create_user_proxy_agent(cls, config: Dict[str, Any]) -> UserProxyAgent:
        """
        Create a user proxy agent.
        
        Args:
            config: Agent configuration
            
        Returns:
            User proxy agent instance
        """
        factory = cls()
        return factory.create_agent("user_proxy", config)
    
    @classmethod
    def create_code_review_agent(cls, config: Dict[str, Any]) -> CodeReviewAgent:
        """
        Create a code review agent.
        
        Args:
            config: Agent configuration
            
        Returns:
            Code review agent instance
        """
        factory = cls()
        return factory.create_agent("code_review", config)
    
    @classmethod
    def create_security_audit_agent(cls, config: Dict[str, Any]) -> SecurityAuditAgent:
        """
        Create a security audit agent.
        
        Args:
            config: Agent configuration
            
        Returns:
            Security audit agent instance
        """
        factory = cls()
        return factory.create_agent("security_audit", config)
    
    @classmethod
    def create_language_detection_agent(cls, config: Dict[str, Any]) -> LanguageDetectionAgent:
        """
        Create a language detection agent.
        
        Args:
            config: Agent configuration
            
        Returns:
            Language detection agent instance
        """
        factory = cls()
        return factory.create_agent("language_detection", config)
    
    @classmethod
    def create_report_generation_agent(cls, config: Dict[str, Any]) -> ReportGenerationAgent:
        """
        Create a report generation agent.
        
        Args:
            config: Agent configuration
            
        Returns:
            Report generation agent instance
        """
        factory = cls()
        return factory.create_agent("report_generation", config)


class GroupChatFactory(BaseFactory):
    """
    Factory for creating group chat instances.
    
    This factory provides methods for creating different types of group chats,
    centralizing group chat creation logic and enhancing extensibility.
    """
    
    def _create_registry(self) -> Registry:
        """
        Create a registry for this factory.
        
        Returns:
            A group chat registry instance
        """
        return GroupChatRegistry()
    
    def create_group_chat(self, chat_type: str, config: Dict[str, Any]) -> IGroupChat:
        """
        Create a group chat of the specified type.
        
        Args:
            chat_type: Type of group chat to create
            config: Group chat configuration
            
        Returns:
            Group chat instance
            
        Raises:
            ValueError: If the group chat type is not registered
        """
        chat_class = self.get_component(chat_type)
        if not chat_class:
            raise ValueError(f"Group chat type not registered: {chat_type}")
        
        chat = chat_class()
        
        # Add agents if specified in config
        agents = config.get("agents", [])
        for agent in agents:
            chat.add_agent(agent)
        
        return chat
    
    def register_group_chat_class(self, name: str, chat_class: Type[IGroupChat]) -> None:
        """
        Register a group chat class.
        
        Args:
            name: Name to register the group chat class under
            chat_class: The group chat class to register
        """
        self.register_component(name, chat_class)


class ToolFactory(BaseFactory):
    """
    Factory for creating tool instances.
    
    This factory provides methods for creating different types of tools,
    centralizing tool creation logic and enhancing extensibility.
    """
    
    def _create_registry(self) -> Registry:
        """
        Create a registry for this factory.
        
        Returns:
            A tool registry instance
        """
        return ToolRegistry()
    
    def create_tool(self, tool_type: str, config: Dict[str, Any]) -> ITool:
        """
        Create a tool of the specified type.
        
        Args:
            tool_type: Type of tool to create
            config: Tool configuration
            
        Returns:
            Tool instance
            
        Raises:
            ValueError: If the tool type is not registered
        """
        tool_class = self.get_component(tool_type)
        if not tool_class:
            raise ValueError(f"Tool type not registered: {tool_type}")
        
        tool = tool_class()
        
        # Configure tool if needed
        name = config.get("name")
        if name:
            tool._name = name
            
        description = config.get("description")
        if description:
            tool._description = description
            
        parameters = config.get("parameters", {})
        for param_name, param_spec in parameters.items():
            tool.add_parameter(param_name, param_spec)
        
        return tool
    
    def register_tool_class(self, name: str, tool_class: Type[ITool]) -> None:
        """
        Register a tool class.
        
        Args:
            name: Name to register the tool class under
            tool_class: The tool class to register
        """
        self.register_component(name, tool_class)


class PluginFactory(BaseFactory):
    """
    Factory for creating plugin instances.
    
    This factory provides methods for creating different types of plugins,
    centralizing plugin creation logic and enhancing extensibility.
    """
    
    def _create_registry(self) -> Registry:
        """
        Create a registry for this factory.
        
        Returns:
            A plugin registry instance
        """
        return PluginRegistry()
    
    def create_plugin(self, plugin_type: str) -> IPlugin:
        """
        Create a plugin of the specified type.
        
        Args:
            plugin_type: Type of plugin to create
            
        Returns:
            Plugin instance
            
        Raises:
            ValueError: If the plugin type is not registered
        """
        plugin_class = self.get_component(plugin_type)
        if not plugin_class:
            raise ValueError(f"Plugin type not registered: {plugin_type}")
        
        plugin = plugin_class()
        plugin.initialize()
        
        return plugin
    
    def register_plugin_class(self, name: str, plugin_class: Type[IPlugin]) -> None:
        """
        Register a plugin class.
        
        Args:
            name: Name to register the plugin class under
            plugin_class: The plugin class to register
        """
        self.register_component(name, plugin_class)
    
    def load_plugin_from_module(self, module_path: str) -> Optional[IPlugin]:
        """
        Load a plugin from a module.
        
        Args:
            module_path: Path to the module containing the plugin
            
        Returns:
            Plugin instance, or None if the module does not contain a plugin
            
        Raises:
            ImportError: If the module cannot be imported
        """
        try:
            module = importlib.import_module(module_path)
            
            # Look for a class that implements IPlugin
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, IPlugin) and attr != IPlugin:
                    plugin = attr()
                    plugin.initialize()
                    return plugin
            
            return None
        except ImportError as e:
            raise ImportError(f"Failed to import plugin module: {module_path}") from e


class FactoryProvider:
    """
    Provider for factory instances.
    
    This class provides a centralized way to access factory instances,
    implementing the singleton pattern to ensure only one instance of
    each factory exists.
    """
    
    _agent_factory: Optional[AgentFactory] = None
    _group_chat_factory: Optional[GroupChatFactory] = None
    _tool_factory: Optional[ToolFactory] = None
    _plugin_factory: Optional[PluginFactory] = None
    
    @classmethod
    def get_agent_factory(cls) -> AgentFactory:
        """
        Get the agent factory instance.
        
        Returns:
            Agent factory instance
        """
        if cls._agent_factory is None:
            cls._agent_factory = AgentFactory()
        
        return cls._agent_factory
    
    @classmethod
    def get_group_chat_factory(cls) -> GroupChatFactory:
        """
        Get the group chat factory instance.
        
        Returns:
            Group chat factory instance
        """
        if cls._group_chat_factory is None:
            cls._group_chat_factory = GroupChatFactory()
        
        return cls._group_chat_factory
    
    @classmethod
    def get_tool_factory(cls) -> ToolFactory:
        """
        Get the tool factory instance.
        
        Returns:
            Tool factory instance
        """
        if cls._tool_factory is None:
            cls._tool_factory = ToolFactory()
        
        return cls._tool_factory
    
    @classmethod
    def get_plugin_factory(cls) -> PluginFactory:
        """
        Get the plugin factory instance.
        
        Returns:
            Plugin factory instance
        """
        if cls._plugin_factory is None:
            cls._plugin_factory = PluginFactory()
        
        return cls._plugin_factory
