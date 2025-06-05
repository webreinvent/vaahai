"""
VaahAI Agent Plugin System

This module provides the plugin system for VaahAI agents, enabling extensibility
through dynamic loading and registration of plugins. Plugins can extend agent
functionality without modifying core code, supporting the open-closed principle.
"""

import importlib
import os
import sys
from abc import abstractmethod
from typing import Dict, Any, List, Optional, Callable, Set, Type

from .interfaces import IPlugin, IAgent, IRegistry


class BasePlugin(IPlugin):
    """
    Base class for all plugins.
    
    This class provides common functionality for plugins, such as
    initialization, hook registration, and metadata.
    """
    
    def __init__(self, name: Optional[str] = None, version: str = "0.1.0"):
        """
        Initialize a new plugin.
        
        Args:
            name: Name of this plugin. If not provided, the class name will be used.
            version: Version of this plugin.
        """
        self._name = name or self.__class__.__name__
        self._version = version
        self._hooks: Dict[str, Callable] = {}
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the plugin."""
        self._register_hooks()
        self._initialized = True
    
    def get_name(self) -> str:
        """
        Get the name of this plugin.
        
        Returns:
            Plugin name string
        """
        return self._name
    
    def get_version(self) -> str:
        """
        Get the version of this plugin.
        
        Returns:
            Plugin version string
        """
        return self._version
    
    def get_hooks(self) -> Dict[str, Callable]:
        """
        Get the hooks this plugin provides.
        
        Returns:
            Dictionary mapping hook names to handler functions
        """
        return self._hooks.copy()
    
    def register_hook(self, name: str, handler: Callable) -> None:
        """
        Register a hook handler.
        
        Args:
            name: Hook name
            handler: Hook handler function
        """
        self._hooks[name] = handler
    
    @abstractmethod
    def _register_hooks(self) -> None:
        """Register hooks provided by this plugin."""
        pass


class PluginManager:
    """
    Manager for plugin discovery, loading, and registration.
    
    This class provides methods for discovering, loading, and registering plugins,
    as well as invoking plugin hooks.
    """
    
    def __init__(self):
        """Initialize a new plugin manager."""
        self._plugins: Dict[str, IPlugin] = {}
        self._hooks: Dict[str, List[Callable]] = {}
        self._plugin_paths: List[str] = []
    
    def register_plugin(self, plugin: IPlugin) -> None:
        """
        Register a plugin.
        
        Args:
            plugin: The plugin to register
            
        Raises:
            ValueError: If a plugin with the same name is already registered
        """
        name = plugin.get_name()
        if name in self._plugins:
            raise ValueError(f"Plugin already registered: {name}")
        
        self._plugins[name] = plugin
        
        # Register plugin hooks
        for hook_name, handler in plugin.get_hooks().items():
            if hook_name not in self._hooks:
                self._hooks[hook_name] = []
            
            self._hooks[hook_name].append(handler)
    
    def unregister_plugin(self, plugin_name: str) -> None:
        """
        Unregister a plugin.
        
        Args:
            plugin_name: Name of the plugin to unregister
        """
        if plugin_name not in self._plugins:
            return
        
        plugin = self._plugins[plugin_name]
        del self._plugins[plugin_name]
        
        # Unregister plugin hooks
        for hook_name, handlers in list(self._hooks.items()):
            new_handlers = []
            for handler in handlers:
                if handler not in plugin.get_hooks().values():
                    new_handlers.append(handler)
            
            if new_handlers:
                self._hooks[hook_name] = new_handlers
            else:
                del self._hooks[hook_name]
    
    def get_plugin(self, plugin_name: str) -> Optional[IPlugin]:
        """
        Get a registered plugin by name.
        
        Args:
            plugin_name: Name of the plugin to get
            
        Returns:
            The plugin, or None if not found
        """
        return self._plugins.get(plugin_name)
    
    def get_plugins(self) -> List[IPlugin]:
        """
        Get all registered plugins.
        
        Returns:
            List of registered plugins
        """
        return list(self._plugins.values())
    
    def add_plugin_path(self, path: str) -> None:
        """
        Add a path to search for plugins.
        
        Args:
            path: Path to search for plugins
        """
        if path not in self._plugin_paths:
            self._plugin_paths.append(path)
    
    def discover_plugins(self) -> List[str]:
        """
        Discover plugins in registered paths.
        
        Returns:
            List of discovered plugin module paths
        """
        plugin_modules = []
        
        for path in self._plugin_paths:
            if not os.path.exists(path):
                continue
            
            # Add path to Python path if not already there
            if path not in sys.path:
                sys.path.append(path)
            
            # Look for Python files in the path
            for file in os.listdir(path):
                if file.endswith(".py") and not file.startswith("__"):
                    module_name = file[:-3]  # Remove .py extension
                    plugin_modules.append(module_name)
        
        return plugin_modules
    
    def load_plugin(self, module_path: str) -> Optional[IPlugin]:
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
                if isinstance(attr, type) and issubclass(attr, IPlugin) and attr != IPlugin and attr != BasePlugin:
                    plugin = attr()
                    plugin.initialize()
                    self.register_plugin(plugin)
                    return plugin
            
            return None
        except ImportError as e:
            raise ImportError(f"Failed to import plugin module: {module_path}") from e
    
    def load_plugins(self) -> List[IPlugin]:
        """
        Discover and load all plugins in registered paths.
        
        Returns:
            List of loaded plugins
        """
        loaded_plugins = []
        
        for module_path in self.discover_plugins():
            plugin = self.load_plugin(module_path)
            if plugin:
                loaded_plugins.append(plugin)
        
        return loaded_plugins
    
    async def invoke_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """
        Invoke all handlers for a hook.
        
        Args:
            hook_name: Name of the hook to invoke
            *args: Positional arguments to pass to hook handlers
            **kwargs: Keyword arguments to pass to hook handlers
            
        Returns:
            List of results from hook handlers
        """
        results = []
        
        if hook_name not in self._hooks:
            return results
        
        for handler in self._hooks[hook_name]:
            try:
                result = handler(*args, **kwargs)
                
                # Handle async handlers
                if hasattr(result, "__await__"):
                    result = await result
                
                results.append(result)
            except Exception as e:
                # Log the error but continue with other handlers
                print(f"Error invoking hook {hook_name}: {e}")
        
        return results
    
    def has_hook(self, hook_name: str) -> bool:
        """
        Check if a hook has any handlers.
        
        Args:
            hook_name: Name of the hook to check
            
        Returns:
            True if the hook has handlers, False otherwise
        """
        return hook_name in self._hooks and len(self._hooks[hook_name]) > 0


class AgentPlugin(BasePlugin):
    """
    Base class for agent plugins.
    
    Agent plugins extend agent functionality by providing hooks that
    are called at specific points in the agent lifecycle.
    """
    
    def __init__(self, name: Optional[str] = None, version: str = "0.1.0"):
        """
        Initialize a new agent plugin.
        
        Args:
            name: Name of this plugin. If not provided, the class name will be used.
            version: Version of this plugin.
        """
        super().__init__(name, version)
        self._supported_agent_types: Set[str] = set()
    
    def supports_agent_type(self, agent_type: str) -> bool:
        """
        Check if this plugin supports a specific agent type.
        
        Args:
            agent_type: Agent type to check
            
        Returns:
            True if the plugin supports the agent type, False otherwise
        """
        # If no agent types are specified, the plugin supports all agent types
        if not self._supported_agent_types:
            return True
        
        return agent_type in self._supported_agent_types
    
    def add_supported_agent_type(self, agent_type: str) -> None:
        """
        Add a supported agent type.
        
        Args:
            agent_type: Agent type to add
        """
        self._supported_agent_types.add(agent_type)
    
    def get_supported_agent_types(self) -> List[str]:
        """
        Get all supported agent types.
        
        Returns:
            List of supported agent types
        """
        return list(self._supported_agent_types)


class MessageProcessorPlugin(BasePlugin):
    """
    Base class for message processor plugins.
    
    Message processor plugins extend message processing functionality by
    providing hooks that are called during message processing.
    """
    
    def __init__(self, name: Optional[str] = None, version: str = "0.1.0"):
        """
        Initialize a new message processor plugin.
        
        Args:
            name: Name of this plugin. If not provided, the class name will be used.
            version: Version of this plugin.
        """
        super().__init__(name, version)
        self._message_types: Set[str] = set()
    
    def supports_message_type(self, message_type: str) -> bool:
        """
        Check if this plugin supports a specific message type.
        
        Args:
            message_type: Message type to check
            
        Returns:
            True if the plugin supports the message type, False otherwise
        """
        # If no message types are specified, the plugin supports all message types
        if not self._message_types:
            return True
        
        return message_type in self._message_types
    
    def add_supported_message_type(self, message_type: str) -> None:
        """
        Add a supported message type.
        
        Args:
            message_type: Message type to add
        """
        self._message_types.add(message_type)
    
    def get_supported_message_types(self) -> List[str]:
        """
        Get all supported message types.
        
        Returns:
            List of supported message types
        """
        return list(self._message_types)


class PluginRegistry(IRegistry):
    """
    Registry for plugin classes.
    
    This registry provides a way to register and discover plugin classes,
    enhancing extensibility by allowing plugins to be added dynamically.
    """
    
    def __init__(self):
        """Initialize a new plugin registry."""
        self._plugins: Dict[str, Type[IPlugin]] = {}
    
    def register(self, name: str, plugin_class: Type[IPlugin]) -> None:
        """
        Register a plugin class.
        
        Args:
            name: Name to register the plugin class under
            plugin_class: The plugin class to register
        """
        self._plugins[name] = plugin_class
    
    def get(self, name: str) -> Optional[Type[IPlugin]]:
        """
        Get a registered plugin class by name.
        
        Args:
            name: Name of the plugin class to get
            
        Returns:
            The registered plugin class, or None if not found
        """
        return self._plugins.get(name)
    
    def list_all(self) -> List[str]:
        """
        List all registered plugin class names.
        
        Returns:
            List of registered plugin class names
        """
        return list(self._plugins.keys())
    
    def create_instance(self, name: str, **kwargs) -> Optional[IPlugin]:
        """
        Create an instance of a registered plugin class.
        
        Args:
            name: Name of the plugin class to instantiate
            **kwargs: Arguments to pass to the plugin constructor
            
        Returns:
            Plugin instance, or None if the plugin class is not found
        """
        plugin_class = self.get(name)
        if not plugin_class:
            return None
        
        plugin = plugin_class(**kwargs)
        plugin.initialize()
        
        return plugin
