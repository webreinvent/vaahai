"""
VaahAI Agent Interfaces

This module defines the core interfaces for the VaahAI agent architecture.
These interfaces establish the contracts that all agent implementations must follow,
ensuring consistency, reusability, and extensibility throughout the system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Callable, TypeVar, Generic

T = TypeVar('T')


class IAgent(ABC):
    """
    Base interface for all agents in the VaahAI system.
    
    All agent implementations must implement this interface to ensure
    consistent behavior and interoperability within the system.
    """
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the agent with configuration.
        
        Args:
            config: Dictionary containing agent configuration parameters
        """
        pass
        
    @abstractmethod
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming message and return a response.
        
        Args:
            message: The message to process
            
        Returns:
            The agent's response message
        """
        pass
        
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Return a list of capabilities this agent supports.
        
        Returns:
            List of capability identifiers
        """
        pass
    
    @abstractmethod
    def get_id(self) -> str:
        """
        Get the unique identifier for this agent.
        
        Returns:
            Agent identifier string
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the display name of this agent.
        
        Returns:
            Agent name string
        """
        pass


class IMessageProcessor(ABC):
    """
    Interface for message processing components.
    
    Message processors handle the transformation and processing of
    messages before they are sent to or after they are received from agents.
    """
    
    @abstractmethod
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a message according to the processor's strategy.
        
        Args:
            message: The message to process
            
        Returns:
            The processed message
        """
        pass


class ITool(ABC):
    """
    Interface for agent tools.
    
    Tools provide specific capabilities to agents, such as web search,
    code execution, or data retrieval.
    """
    
    @abstractmethod
    async def execute(self, parameters: Dict[str, Any]) -> Any:
        """
        Execute the tool with the given parameters.
        
        Args:
            parameters: Tool execution parameters
            
        Returns:
            Tool execution result
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get a description of what this tool does.
        
        Returns:
            Tool description string
        """
        pass
    
    @abstractmethod
    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the parameters this tool accepts.
        
        Returns:
            Dictionary mapping parameter names to their specifications
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of this tool.
        
        Returns:
            Tool name string
        """
        pass


class IGroupChat(ABC):
    """
    Interface for group chat implementations.
    
    Group chats manage conversations between multiple agents,
    handling message routing and conversation flow.
    """
    
    @abstractmethod
    def add_agent(self, agent: IAgent) -> None:
        """
        Add an agent to the group chat.
        
        Args:
            agent: The agent to add
        """
        pass
    
    @abstractmethod
    def remove_agent(self, agent_id: str) -> None:
        """
        Remove an agent from the group chat.
        
        Args:
            agent_id: ID of the agent to remove
        """
        pass
    
    @abstractmethod
    async def start_chat(self, initial_message: Dict[str, Any]) -> None:
        """
        Start a group chat with an initial message.
        
        Args:
            initial_message: The message to start the chat with
        """
        pass
    
    @abstractmethod
    async def end_chat(self) -> Dict[str, Any]:
        """
        End the current group chat.
        
        Returns:
            Summary of the chat
        """
        pass
    
    @abstractmethod
    def get_agents(self) -> List[IAgent]:
        """
        Get all agents in this group chat.
        
        Returns:
            List of agents
        """
        pass
    
    @abstractmethod
    def get_chat_history(self) -> List[Dict[str, Any]]:
        """
        Get the chat history.
        
        Returns:
            List of messages in the chat
        """
        pass


class IAgentAdapter(ABC):
    """
    Interface for agent adapters.
    
    Agent adapters translate between VaahAI's agent interface and
    external agent frameworks like Autogen.
    """
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the adapter with configuration.
        
        Args:
            config: Dictionary containing adapter configuration
        """
        pass
    
    @abstractmethod
    def adapt_agent(self, agent: IAgent) -> Any:
        """
        Adapt a VaahAI agent to the external framework's agent type.
        
        Args:
            agent: The VaahAI agent to adapt
            
        Returns:
            External framework agent instance
        """
        pass
    
    @abstractmethod
    def adapt_message_to_external(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a VaahAI message to the external framework's format.
        
        Args:
            message: VaahAI message
            
        Returns:
            External framework message
        """
        pass
    
    @abstractmethod
    def adapt_message_from_external(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert an external framework message to VaahAI format.
        
        Args:
            message: External framework message
            
        Returns:
            VaahAI message
        """
        pass


class IGroupChatAdapter(ABC):
    """
    Interface for group chat adapters.
    
    Group chat adapters translate between VaahAI's group chat interface
    and external frameworks' group chat implementations.
    """
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the adapter with configuration.
        
        Args:
            config: Dictionary containing adapter configuration
        """
        pass
    
    @abstractmethod
    def adapt_group_chat(self, group_chat: IGroupChat) -> Any:
        """
        Adapt a VaahAI group chat to the external framework's group chat type.
        
        Args:
            group_chat: The VaahAI group chat to adapt
            
        Returns:
            External framework group chat instance
        """
        pass


class IPlugin(ABC):
    """
    Interface for plugins.
    
    Plugins provide a way to extend the system with new functionality
    without modifying existing code.
    """
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin."""
        pass
    
    @abstractmethod
    def get_hooks(self) -> Dict[str, Callable]:
        """
        Get the hooks this plugin provides.
        
        Returns:
            Dictionary mapping hook names to handler functions
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of this plugin.
        
        Returns:
            Plugin name string
        """
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """
        Get the version of this plugin.
        
        Returns:
            Plugin version string
        """
        pass


class IConfig(ABC):
    """
    Interface for configuration objects.
    
    Configuration objects provide a structured way to configure
    components in the system.
    """
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of the configuration
        """
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """
        Validate the configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        pass


class IEventHandler(Generic[T], ABC):
    """
    Interface for event handlers.
    
    Event handlers respond to events in the system, allowing
    for loose coupling between components.
    """
    
    @abstractmethod
    async def handle_event(self, event_data: T) -> None:
        """
        Handle an event.
        
        Args:
            event_data: Data associated with the event
        """
        pass


class IRegistry(Generic[T], ABC):
    """
    Interface for component registries.
    
    Registries provide a way to register and discover components
    dynamically, enhancing extensibility.
    """
    
    @abstractmethod
    def register(self, name: str, component: T) -> None:
        """
        Register a component.
        
        Args:
            name: Name to register the component under
            component: The component to register
        """
        pass
    
    @abstractmethod
    def get(self, name: str) -> Optional[T]:
        """
        Get a registered component by name.
        
        Args:
            name: Name of the component to get
            
        Returns:
            The registered component, or None if not found
        """
        pass
    
    @abstractmethod
    def list_all(self) -> List[str]:
        """
        List all registered component names.
        
        Returns:
            List of registered component names
        """
        pass
