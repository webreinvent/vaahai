"""
VaahAI Agent Adapters

This module provides adapter implementations that bridge between VaahAI's agent interfaces
and external frameworks like Autogen. These adapters follow the adapter pattern to provide
a clean separation between VaahAI components and external dependencies, enhancing reusability
and extensibility.
"""

from abc import abstractmethod
from typing import Dict, Any, List, Optional, Type, Callable, Union, Tuple

from .interfaces import IAgent, IGroupChat, IAgentAdapter, IGroupChatAdapter, ITool


class BaseAdapter:
    """
    Base class for all adapters.
    
    Provides common functionality for adapter initialization and configuration.
    """
    
    def __init__(self):
        """Initialize a new adapter."""
        self._config: Dict[str, Any] = {}
        self._initialized = False
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the adapter with configuration.
        
        Args:
            config: Dictionary containing adapter configuration
        
        Raises:
            ValueError: If the configuration is invalid
        """
        self._config = config.copy()
        
        if not self._validate_config():
            raise ValueError("Invalid adapter configuration")
        
        self._initialized = True
    
    def _validate_config(self) -> bool:
        """
        Validate the adapter configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        return True  # Base implementation assumes any config is valid
    
    def _ensure_initialized(self) -> None:
        """
        Ensure the adapter is initialized.
        
        Raises:
            RuntimeError: If the adapter is not initialized
        """
        if not self._initialized:
            raise RuntimeError("Adapter not initialized")


class AutogenAgentAdapter(BaseAdapter, IAgentAdapter):
    """
    Adapter for Autogen agents.
    
    This adapter translates between VaahAI's agent interface and Autogen's agent interface.
    """
    
    def __init__(self):
        """Initialize a new Autogen agent adapter."""
        super().__init__()
        self._autogen_agent = None
        self._vaah_agent: Optional[IAgent] = None
        self._message_converters: Dict[str, Callable] = {}
    
    def adapt_agent(self, agent: IAgent) -> Any:
        """
        Adapt a VaahAI agent to an Autogen agent.
        
        Args:
            agent: The VaahAI agent to adapt
            
        Returns:
            Autogen agent instance
        
        Raises:
            RuntimeError: If the adapter is not initialized
        """
        self._ensure_initialized()
        self._vaah_agent = agent
        
        # Create Autogen agent based on configuration
        # This is a placeholder - actual implementation would import and use Autogen
        self._autogen_agent = self._create_autogen_agent()
        
        return self._autogen_agent
    
    def adapt_message_to_external(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a VaahAI message to Autogen format.
        
        Args:
            message: VaahAI message
            
        Returns:
            Autogen message
        
        Raises:
            RuntimeError: If the adapter is not initialized
        """
        self._ensure_initialized()
        
        # Apply registered converters for the message type
        message_type = message.get("type", "default")
        converter = self._message_converters.get(message_type)
        
        if converter:
            return converter(message, "to_external")
        
        # Default conversion logic
        return self._default_message_conversion(message, "to_external")
    
    def adapt_message_from_external(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert an Autogen message to VaahAI format.
        
        Args:
            message: Autogen message
            
        Returns:
            VaahAI message
        
        Raises:
            RuntimeError: If the adapter is not initialized
        """
        self._ensure_initialized()
        
        # Apply registered converters for the message type
        message_type = self._get_external_message_type(message)
        converter = self._message_converters.get(message_type)
        
        if converter:
            return converter(message, "from_external")
        
        # Default conversion logic
        return self._default_message_conversion(message, "from_external")
    
    def register_message_converter(self, message_type: str, converter: Callable) -> None:
        """
        Register a custom message converter for a specific message type.
        
        Args:
            message_type: Type of message to convert
            converter: Function that converts messages
        """
        self._message_converters[message_type] = converter
    
    def _create_autogen_agent(self) -> Any:
        """
        Create an Autogen agent based on configuration.
        
        Returns:
            Autogen agent instance
        """
        # This is a placeholder - actual implementation would create an Autogen agent
        # based on the adapter configuration and the VaahAI agent's capabilities
        agent_type = self._config.get("agent_type", "assistant")
        
        # In a real implementation, we would import Autogen and create the appropriate agent
        # For now, we'll just return a dictionary representing the agent
        return {
            "type": agent_type,
            "name": self._vaah_agent.get_name(),
            "id": self._vaah_agent.get_id(),
            "capabilities": self._vaah_agent.get_capabilities(),
            "config": self._config.get("agent_config", {})
        }
    
    def _default_message_conversion(self, message: Dict[str, Any], direction: str) -> Dict[str, Any]:
        """
        Default message conversion logic.
        
        Args:
            message: Message to convert
            direction: Direction of conversion ('to_external' or 'from_external')
            
        Returns:
            Converted message
        """
        if direction == "to_external":
            # Convert VaahAI message to Autogen format
            return {
                "role": message.get("sender_role", "user"),
                "content": message.get("content", ""),
                "sender": message.get("sender_id", ""),
                "recipient": message.get("recipient_id", ""),
                "metadata": message.get("metadata", {})
            }
        else:
            # Convert Autogen message to VaahAI format
            return {
                "type": "message",
                "content": message.get("content", ""),
                "sender_id": message.get("sender", ""),
                "sender_role": message.get("role", "assistant"),
                "recipient_id": message.get("recipient", ""),
                "metadata": message.get("metadata", {})
            }
    
    def _get_external_message_type(self, message: Dict[str, Any]) -> str:
        """
        Determine the type of an external message.
        
        Args:
            message: External message
            
        Returns:
            Message type string
        """
        # This is a placeholder - actual implementation would determine the message type
        # based on the structure of the Autogen message
        if "function_call" in message:
            return "function_call"
        elif "tool_calls" in message:
            return "tool_calls"
        elif "error" in message:
            return "error"
        else:
            return "default"
    
    def _validate_config(self) -> bool:
        """
        Validate the adapter configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        # Check for required configuration
        required_keys = ["agent_type"]
        return all(key in self._config for key in required_keys)


class AutogenGroupChatAdapter(BaseAdapter, IGroupChatAdapter):
    """
    Adapter for Autogen group chats.
    
    This adapter translates between VaahAI's group chat interface and Autogen's group chat interface.
    """
    
    def __init__(self):
        """Initialize a new Autogen group chat adapter."""
        super().__init__()
        self._autogen_group_chat = None
        self._vaah_group_chat: Optional[IGroupChat] = None
        self._agent_adapters: Dict[str, IAgentAdapter] = {}
    
    def adapt_group_chat(self, group_chat: IGroupChat) -> Any:
        """
        Adapt a VaahAI group chat to an Autogen group chat.
        
        Args:
            group_chat: The VaahAI group chat to adapt
            
        Returns:
            Autogen group chat instance
        
        Raises:
            RuntimeError: If the adapter is not initialized
        """
        self._ensure_initialized()
        self._vaah_group_chat = group_chat
        
        # Create Autogen group chat based on configuration
        # This is a placeholder - actual implementation would import and use Autogen
        self._autogen_group_chat = self._create_autogen_group_chat()
        
        return self._autogen_group_chat
    
    def register_agent_adapter(self, agent_id: str, adapter: IAgentAdapter) -> None:
        """
        Register an agent adapter for a specific agent.
        
        Args:
            agent_id: ID of the agent
            adapter: Adapter for the agent
        """
        self._agent_adapters[agent_id] = adapter
    
    def get_agent_adapter(self, agent_id: str) -> Optional[IAgentAdapter]:
        """
        Get the adapter for a specific agent.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            Agent adapter, or None if not found
        """
        return self._agent_adapters.get(agent_id)
    
    def _create_autogen_group_chat(self) -> Any:
        """
        Create an Autogen group chat based on configuration.
        
        Returns:
            Autogen group chat instance
        """
        # This is a placeholder - actual implementation would create an Autogen group chat
        # based on the adapter configuration and the VaahAI group chat's agents
        chat_type = self._config.get("chat_type", "round_robin")
        
        # Adapt all agents in the group chat
        autogen_agents = []
        for agent in self._vaah_group_chat.get_agents():
            agent_id = agent.get_id()
            adapter = self.get_agent_adapter(agent_id)
            
            if adapter:
                autogen_agent = adapter.adapt_agent(agent)
                autogen_agents.append(autogen_agent)
        
        # In a real implementation, we would import Autogen and create the appropriate group chat
        # For now, we'll just return a dictionary representing the group chat
        return {
            "type": chat_type,
            "agents": autogen_agents,
            "config": self._config.get("chat_config", {})
        }
    
    def _validate_config(self) -> bool:
        """
        Validate the adapter configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        # Check for required configuration
        required_keys = ["chat_type"]
        return all(key in self._config for key in required_keys)


class AutogenToolAdapter(BaseAdapter):
    """
    Adapter for Autogen tools.
    
    This adapter translates between VaahAI's tool interface and Autogen's tool interface.
    """
    
    def __init__(self):
        """Initialize a new Autogen tool adapter."""
        super().__init__()
        self._tools: Dict[str, ITool] = {}
    
    def register_tool(self, tool: ITool) -> None:
        """
        Register a tool with the adapter.
        
        Args:
            tool: The tool to register
        """
        self._tools[tool.get_name()] = tool
    
    def unregister_tool(self, tool_name: str) -> None:
        """
        Unregister a tool from the adapter.
        
        Args:
            tool_name: Name of the tool to unregister
        """
        if tool_name in self._tools:
            del self._tools[tool_name]
    
    def get_tool(self, tool_name: str) -> Optional[ITool]:
        """
        Get a registered tool by name.
        
        Args:
            tool_name: Name of the tool to get
            
        Returns:
            The tool, or None if not found
        """
        return self._tools.get(tool_name)
    
    def get_tools(self) -> List[ITool]:
        """
        Get all registered tools.
        
        Returns:
            List of registered tools
        """
        return list(self._tools.values())
    
    def get_tool_specs(self) -> List[Dict[str, Any]]:
        """
        Get specifications for all registered tools in Autogen format.
        
        Returns:
            List of tool specifications
        """
        self._ensure_initialized()
        
        specs = []
        for tool in self._tools.values():
            specs.append({
                "name": tool.get_name(),
                "description": tool.get_description(),
                "parameters": {
                    "type": "object",
                    "properties": tool.get_parameters(),
                    "required": self._get_required_parameters(tool)
                }
            })
        
        return specs
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """
        Execute a tool with the given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Tool execution parameters
            
        Returns:
            Tool execution result
            
        Raises:
            ValueError: If the tool is not found
        """
        self._ensure_initialized()
        
        tool = self.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")
        
        return await tool.execute(parameters)
    
    def _get_required_parameters(self, tool: ITool) -> List[str]:
        """
        Get the required parameters for a tool.
        
        Args:
            tool: The tool to get required parameters for
            
        Returns:
            List of required parameter names
        """
        required = []
        for name, spec in tool.get_parameters().items():
            if spec.get("required", False):
                required.append(name)
        
        return required


class AdapterFactory:
    """
    Factory for creating adapters.
    
    This factory provides a centralized way to create adapters for different
    external frameworks, enhancing extensibility.
    """
    
    _adapter_classes: Dict[str, Dict[str, Type]] = {
        "autogen": {
            "agent": AutogenAgentAdapter,
            "group_chat": AutogenGroupChatAdapter,
            "tool": AutogenToolAdapter
        }
    }
    
    @classmethod
    def create_agent_adapter(cls, framework: str, config: Dict[str, Any]) -> IAgentAdapter:
        """
        Create an agent adapter for the specified framework.
        
        Args:
            framework: Name of the external framework
            config: Adapter configuration
            
        Returns:
            Agent adapter instance
            
        Raises:
            ValueError: If the framework or adapter type is not supported
        """
        if framework not in cls._adapter_classes:
            raise ValueError(f"Unsupported framework: {framework}")
        
        if "agent" not in cls._adapter_classes[framework]:
            raise ValueError(f"Agent adapter not available for framework: {framework}")
        
        adapter_class = cls._adapter_classes[framework]["agent"]
        adapter = adapter_class()
        adapter.initialize(config)
        
        return adapter
    
    @classmethod
    def create_group_chat_adapter(cls, framework: str, config: Dict[str, Any]) -> IGroupChatAdapter:
        """
        Create a group chat adapter for the specified framework.
        
        Args:
            framework: Name of the external framework
            config: Adapter configuration
            
        Returns:
            Group chat adapter instance
            
        Raises:
            ValueError: If the framework or adapter type is not supported
        """
        if framework not in cls._adapter_classes:
            raise ValueError(f"Unsupported framework: {framework}")
        
        if "group_chat" not in cls._adapter_classes[framework]:
            raise ValueError(f"Group chat adapter not available for framework: {framework}")
        
        adapter_class = cls._adapter_classes[framework]["group_chat"]
        adapter = adapter_class()
        adapter.initialize(config)
        
        return adapter
    
    @classmethod
    def create_tool_adapter(cls, framework: str, config: Dict[str, Any]) -> Any:
        """
        Create a tool adapter for the specified framework.
        
        Args:
            framework: Name of the external framework
            config: Adapter configuration
            
        Returns:
            Tool adapter instance
            
        Raises:
            ValueError: If the framework or adapter type is not supported
        """
        if framework not in cls._adapter_classes:
            raise ValueError(f"Unsupported framework: {framework}")
        
        if "tool" not in cls._adapter_classes[framework]:
            raise ValueError(f"Tool adapter not available for framework: {framework}")
        
        adapter_class = cls._adapter_classes[framework]["tool"]
        adapter = adapter_class()
        adapter.initialize(config)
        
        return adapter
    
    @classmethod
    def register_adapter_class(cls, framework: str, adapter_type: str, adapter_class: Type) -> None:
        """
        Register an adapter class for a framework and adapter type.
        
        Args:
            framework: Name of the external framework
            adapter_type: Type of adapter ('agent', 'group_chat', or 'tool')
            adapter_class: Adapter class to register
        """
        if framework not in cls._adapter_classes:
            cls._adapter_classes[framework] = {}
        
        cls._adapter_classes[framework][adapter_type] = adapter_class
    
    @classmethod
    def get_supported_frameworks(cls) -> List[str]:
        """
        Get a list of supported frameworks.
        
        Returns:
            List of framework names
        """
        return list(cls._adapter_classes.keys())
    
    @classmethod
    def get_supported_adapter_types(cls, framework: str) -> List[str]:
        """
        Get a list of supported adapter types for a framework.
        
        Args:
            framework: Name of the external framework
            
        Returns:
            List of adapter type names
            
        Raises:
            ValueError: If the framework is not supported
        """
        if framework not in cls._adapter_classes:
            raise ValueError(f"Unsupported framework: {framework}")
        
        return list(cls._adapter_classes[framework].keys())
