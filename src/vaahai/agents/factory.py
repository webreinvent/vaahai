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
        Register a component with this factory.
        
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
            List of component names
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
    
    def _create_registry(self) -> Registry:
        """
        Create a registry for this factory.
        
        Returns:
            An agent registry instance
        """
        return AgentRegistry()
    
    def create_agent(self, agent_type: str, config: Dict[str, Any]) -> IAgent:
        """
        Create an agent of the specified type.
        
        Args:
            agent_type: Type of agent to create
            config: Agent configuration
            
        Returns:
            Agent instance
            
        Raises:
            ValueError: If the agent type is not registered
        """
        agent_class = self.get_component(agent_type)
        if not agent_class:
            raise ValueError(f"Agent type not registered: {agent_type}")
        
        agent = agent_class()
        agent.initialize(config)
        
        # Apply decorators if specified in config
        decorators = config.get("decorators", [])
        for decorator_name in decorators:
            decorator_class = self._decorators.get(decorator_name)
            if decorator_class:
                agent = decorator_class(agent)
        
        return agent
    
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
    async def create_language_detector_agent(cls, llm_client: Any) -> IAgent:
        """
        Create a language detector agent.
        
        Args:
            llm_client: LLM client to use for language detection
            
        Returns:
            Language detector agent instance
        """
        # This is a placeholder - actual implementation would create a language detector agent
        # For now, we'll just return a dictionary representing the agent
        return {
            "type": "language_detector",
            "name": "LanguageDetector",
            "id": "language_detector_1",
            "capabilities": ["language_detection"],
            "llm_client": llm_client
        }


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
