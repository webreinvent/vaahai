"""
VaahAI Base Agent Classes

This module provides abstract base classes that implement the core interfaces
defined in the interfaces module. These base classes provide common functionality
that can be reused across different agent implementations, promoting code reuse
and consistent behavior.
"""

import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional, Set

from .interfaces import IAgent, IMessageProcessor, ITool, IGroupChat
from .exceptions import AgentInitializationError, AgentConfigurationError

logger = logging.getLogger(__name__)

class BaseAgent(IAgent, ABC):
    """
    Abstract base class for all agents in the VaahAI system.
    
    This class provides common functionality for all agents, such as
    initialization, configuration validation, and capability management.
    """
    
    def __init__(self, agent_id: Optional[str] = None, name: Optional[str] = None):
        """
        Initialize a new agent.
        
        Args:
            agent_id: Unique identifier for this agent. If not provided, a UUID will be generated.
            name: Display name for this agent. If not provided, the class name will be used.
        """
        self._id = agent_id or str(uuid.uuid4())
        self._name = name or self.__class__.__name__
        self._config: Dict[str, Any] = {}
        self._capabilities: Set[str] = set()
        self._initialized = False
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the agent with configuration.
        
        Args:
            config: Dictionary containing agent configuration parameters
            
        Raises:
            AgentInitializationError: If the configuration is invalid
        """
        self._config = config.copy()
        
        if not self._validate_config():
            raise AgentInitializationError(self._name, f"Invalid configuration for agent {self._name}")
        
        self._initialize_capabilities()
        self._initialized = True
    
    def get_id(self) -> str:
        """
        Get the unique identifier for this agent.
        
        Returns:
            Agent identifier string
        """
        return self._id
    
    def get_name(self) -> str:
        """
        Get the display name of this agent.
        
        Returns:
            Agent name string
        """
        return self._name
    
    def get_capabilities(self) -> List[str]:
        """
        Return a list of capabilities this agent supports.
        
        Returns:
            List of capability identifiers
        """
        return list(self._capabilities)
    
    def add_capability(self, capability: str) -> None:
        """
        Add a capability to this agent.
        
        Args:
            capability: Capability identifier
        """
        self._capabilities.add(capability)
    
    def remove_capability(self, capability: str) -> None:
        """
        Remove a capability from this agent.
        
        Args:
            capability: Capability identifier
        """
        self._capabilities.discard(capability)
    
    def has_capability(self, capability: str) -> bool:
        """
        Check if this agent has a specific capability.
        
        Args:
            capability: Capability identifier
            
        Returns:
            True if the agent has the capability, False otherwise
        """
        return capability in self._capabilities
    
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
    def _validate_config(self) -> bool:
        """
        Validate the agent configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def _initialize_capabilities(self) -> None:
        """Initialize the agent's capabilities."""
        pass


class AgentDecorator(IAgent):
    """
    Base decorator for agents.
    
    This class implements the decorator pattern, allowing functionality
    to be added to agents dynamically without modifying their code.
    """
    
    def __init__(self, agent: IAgent):
        """
        Initialize a new agent decorator.
        
        Args:
            agent: The agent to decorate
        """
        self._agent = agent
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the decorated agent with configuration.
        
        Args:
            config: Dictionary containing agent configuration parameters
        """
        self._agent.initialize(config)
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming message using the decorated agent.
        
        Args:
            message: The message to process
            
        Returns:
            The agent's response message
        """
        return await self._agent.process_message(message)
    
    def get_capabilities(self) -> List[str]:
        """
        Return a list of capabilities the decorated agent supports.
        
        Returns:
            List of capability identifiers
        """
        return self._agent.get_capabilities()
    
    def get_id(self) -> str:
        """
        Get the unique identifier for the decorated agent.
        
        Returns:
            Agent identifier string
        """
        return self._agent.get_id()
    
    def get_name(self) -> str:
        """
        Get the display name of the decorated agent.
        
        Returns:
            Agent name string
        """
        return self._agent.get_name()


class BaseMessageProcessor(IMessageProcessor):
    """
    Base class for message processors.
    
    Message processors handle the transformation and processing of
    messages before they are sent to or after they are received from agents.
    """
    
    def __init__(self, name: Optional[str] = None):
        """
        Initialize a new message processor.
        
        Args:
            name: Name of this processor. If not provided, the class name will be used.
        """
        self._name = name or self.__class__.__name__
    
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
    
    def get_name(self) -> str:
        """
        Get the name of this processor.
        
        Returns:
            Processor name string
        """
        return self._name


class ChainedMessageProcessor(BaseMessageProcessor):
    """
    A message processor that chains multiple processors together.
    
    This processor applies a sequence of processors to a message in order.
    """
    
    def __init__(self, processors: Optional[List[IMessageProcessor]] = None, name: Optional[str] = None):
        """
        Initialize a new chained message processor.
        
        Args:
            processors: List of processors to chain. If not provided, an empty list will be used.
            name: Name of this processor. If not provided, the class name will be used.
        """
        super().__init__(name)
        self._processors = processors or []
    
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a message by applying each processor in the chain.
        
        Args:
            message: The message to process
            
        Returns:
            The processed message
        """
        result = message
        for processor in self._processors:
            result = await processor.process(result)
        return result
    
    def add_processor(self, processor: IMessageProcessor) -> None:
        """
        Add a processor to the chain.
        
        Args:
            processor: The processor to add
        """
        self._processors.append(processor)
    
    def remove_processor(self, processor: IMessageProcessor) -> None:
        """
        Remove a processor from the chain.
        
        Args:
            processor: The processor to remove
        """
        if processor in self._processors:
            self._processors.remove(processor)
    
    def get_processors(self) -> List[IMessageProcessor]:
        """
        Get all processors in the chain.
        
        Returns:
            List of processors
        """
        return self._processors.copy()


class BaseTool(ITool):
    """
    Base class for agent tools.
    
    Tools provide specific capabilities to agents, such as web search,
    code execution, or data retrieval.
    """
    
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a new tool.
        
        Args:
            name: Name of this tool. If not provided, the class name will be used.
            description: Description of what this tool does.
        """
        self._name = name or self.__class__.__name__
        self._description = description or f"{self._name} tool"
        self._parameters: Dict[str, Dict[str, Any]] = {}
    
    def get_name(self) -> str:
        """
        Get the name of this tool.
        
        Returns:
            Tool name string
        """
        return self._name
    
    def get_description(self) -> str:
        """
        Get a description of what this tool does.
        
        Returns:
            Tool description string
        """
        return self._description
    
    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the parameters this tool accepts.
        
        Returns:
            Dictionary mapping parameter names to their specifications
        """
        return self._parameters.copy()
    
    def add_parameter(self, name: str, spec: Dict[str, Any]) -> None:
        """
        Add a parameter to this tool.
        
        Args:
            name: Parameter name
            spec: Parameter specification
        """
        self._parameters[name] = spec.copy()
    
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


class BaseGroupChat(IGroupChat):
    """
    Base class for group chat implementations.
    
    Group chats manage conversations between multiple agents,
    handling message routing and conversation flow.
    """
    
    def __init__(self, name: Optional[str] = None):
        """
        Initialize a new group chat.
        
        Args:
            name: Name of this group chat. If not provided, the class name will be used.
        """
        self._name = name or self.__class__.__name__
        self._agents: Dict[str, IAgent] = {}
        self._history: List[Dict[str, Any]] = []
    
    def add_agent(self, agent: IAgent) -> None:
        """
        Add an agent to the group chat.
        
        Args:
            agent: The agent to add
        """
        self._agents[agent.get_id()] = agent
    
    def remove_agent(self, agent_id: str) -> None:
        """
        Remove an agent from the group chat.
        
        Args:
            agent_id: ID of the agent to remove
        """
        if agent_id in self._agents:
            del self._agents[agent_id]
    
    def get_agents(self) -> List[IAgent]:
        """
        Get all agents in this group chat.
        
        Returns:
            List of agents
        """
        return list(self._agents.values())
    
    def get_agent(self, agent_id: str) -> Optional[IAgent]:
        """
        Get an agent by ID.
        
        Args:
            agent_id: ID of the agent to get
            
        Returns:
            The agent, or None if not found
        """
        return self._agents.get(agent_id)
    
    def get_chat_history(self) -> List[Dict[str, Any]]:
        """
        Get the chat history.
        
        Returns:
            List of messages in the chat
        """
        return self._history.copy()
    
    def add_to_history(self, message: Dict[str, Any]) -> None:
        """
        Add a message to the chat history.
        
        Args:
            message: The message to add
        """
        self._history.append(message.copy())
    
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
