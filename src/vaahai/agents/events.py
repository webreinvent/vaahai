"""
VaahAI Agent Event System

This module provides an event system for VaahAI agents, enabling loose coupling
between components through event-based communication. Components can publish events
and subscribe to events, enhancing extensibility by allowing new components to
integrate without modifying existing code.
"""

import asyncio
from abc import abstractmethod
from typing import Dict, Any, List, Optional, Callable, TypeVar, Generic, Set, Union

from .interfaces import IEventHandler

T = TypeVar('T')


class Event(Generic[T]):
    """
    Base class for all events.
    
    Events encapsulate data related to something that has happened in the system,
    allowing components to react to changes without direct coupling.
    """
    
    def __init__(self, event_type: str, data: T):
        """
        Initialize a new event.
        
        Args:
            event_type: Type of the event
            data: Data associated with the event
        """
        self._type = event_type
        self._data = data
        self._timestamp = asyncio.get_event_loop().time()
    
    @property
    def type(self) -> str:
        """
        Get the type of this event.
        
        Returns:
            Event type string
        """
        return self._type
    
    @property
    def data(self) -> T:
        """
        Get the data associated with this event.
        
        Returns:
            Event data
        """
        return self._data
    
    @property
    def timestamp(self) -> float:
        """
        Get the timestamp of this event.
        
        Returns:
            Event timestamp
        """
        return self._timestamp


class EventBus:
    """
    Central event bus for publishing and subscribing to events.
    
    The event bus decouples event publishers from event subscribers,
    enhancing extensibility by allowing components to communicate
    without direct dependencies.
    """
    
    def __init__(self):
        """Initialize a new event bus."""
        self._subscribers: Dict[str, List[IEventHandler]] = {}
        self._wildcard_subscribers: List[IEventHandler] = []
    
    def subscribe(self, event_type: str, handler: IEventHandler) -> None:
        """
        Subscribe to events of a specific type.
        
        Args:
            event_type: Type of events to subscribe to
            handler: Event handler to call when events of this type are published
        """
        if event_type == "*":
            self._wildcard_subscribers.append(handler)
        else:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            
            self._subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: IEventHandler) -> None:
        """
        Unsubscribe from events of a specific type.
        
        Args:
            event_type: Type of events to unsubscribe from
            handler: Event handler to remove
        """
        if event_type == "*":
            if handler in self._wildcard_subscribers:
                self._wildcard_subscribers.remove(handler)
        else:
            if event_type in self._subscribers and handler in self._subscribers[event_type]:
                self._subscribers[event_type].remove(handler)
                
                if not self._subscribers[event_type]:
                    del self._subscribers[event_type]
    
    async def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event: The event to publish
        """
        # Notify specific subscribers
        if event.type in self._subscribers:
            for handler in self._subscribers[event.type]:
                try:
                    await handler.handle_event(event.data)
                except Exception as e:
                    # Log the error but continue with other handlers
                    print(f"Error handling event {event.type}: {e}")
        
        # Notify wildcard subscribers
        for handler in self._wildcard_subscribers:
            try:
                await handler.handle_event(event.data)
            except Exception as e:
                # Log the error but continue with other handlers
                print(f"Error handling event {event.type}: {e}")
    
    def get_subscribers(self, event_type: Optional[str] = None) -> List[IEventHandler]:
        """
        Get all subscribers for a specific event type.
        
        Args:
            event_type: Type of events to get subscribers for. If None, returns all subscribers.
            
        Returns:
            List of event handlers
        """
        if event_type is None:
            # Return all subscribers
            all_subscribers = set(self._wildcard_subscribers)
            for handlers in self._subscribers.values():
                all_subscribers.update(handlers)
            return list(all_subscribers)
        elif event_type == "*":
            return self._wildcard_subscribers.copy()
        else:
            return self._subscribers.get(event_type, []).copy()


class BaseEventHandler(IEventHandler[T]):
    """
    Base class for event handlers.
    
    Event handlers respond to events in the system, allowing
    for loose coupling between components.
    """
    
    def __init__(self, name: Optional[str] = None):
        """
        Initialize a new event handler.
        
        Args:
            name: Name of this handler. If not provided, the class name will be used.
        """
        self._name = name or self.__class__.__name__
    
    @abstractmethod
    async def handle_event(self, event_data: T) -> None:
        """
        Handle an event.
        
        Args:
            event_data: Data associated with the event
        """
        pass
    
    def get_name(self) -> str:
        """
        Get the name of this handler.
        
        Returns:
            Handler name string
        """
        return self._name


class EventHandlerRegistry:
    """
    Registry for event handlers.
    
    This registry provides a way to register and discover event handlers,
    enhancing extensibility by allowing handlers to be added dynamically.
    """
    
    def __init__(self):
        """Initialize a new event handler registry."""
        self._handlers: Dict[str, IEventHandler] = {}
    
    def register(self, name: str, handler: IEventHandler) -> None:
        """
        Register an event handler.
        
        Args:
            name: Name to register the handler under
            handler: The handler to register
        """
        self._handlers[name] = handler
    
    def unregister(self, name: str) -> None:
        """
        Unregister an event handler.
        
        Args:
            name: Name of the handler to unregister
        """
        if name in self._handlers:
            del self._handlers[name]
    
    def get(self, name: str) -> Optional[IEventHandler]:
        """
        Get a registered handler by name.
        
        Args:
            name: Name of the handler to get
            
        Returns:
            The registered handler, or None if not found
        """
        return self._handlers.get(name)
    
    def list_all(self) -> List[str]:
        """
        List all registered handler names.
        
        Returns:
            List of registered handler names
        """
        return list(self._handlers.keys())


class EventManager:
    """
    Manager for the event system.
    
    This class provides a centralized way to access the event bus and event handler registry,
    implementing the singleton pattern to ensure only one instance exists.
    """
    
    _instance: Optional['EventManager'] = None
    
    def __new__(cls):
        """
        Create a new event manager instance, or return the existing one.
        
        Returns:
            Event manager instance
        """
        if cls._instance is None:
            cls._instance = super(EventManager, cls).__new__(cls)
            cls._instance._initialized = False
        
        return cls._instance
    
    def __init__(self):
        """Initialize the event manager."""
        if not self._initialized:
            self._event_bus = EventBus()
            self._handler_registry = EventHandlerRegistry()
            self._initialized = True
    
    @property
    def event_bus(self) -> EventBus:
        """
        Get the event bus.
        
        Returns:
            Event bus instance
        """
        return self._event_bus
    
    @property
    def handler_registry(self) -> EventHandlerRegistry:
        """
        Get the event handler registry.
        
        Returns:
            Event handler registry instance
        """
        return self._handler_registry
    
    async def publish_event(self, event_type: str, data: Any) -> None:
        """
        Publish an event.
        
        Args:
            event_type: Type of the event
            data: Data associated with the event
        """
        event = Event(event_type, data)
        await self._event_bus.publish(event)
    
    def subscribe(self, event_type: str, handler: IEventHandler) -> None:
        """
        Subscribe to events of a specific type.
        
        Args:
            event_type: Type of events to subscribe to
            handler: Event handler to call when events of this type are published
        """
        self._event_bus.subscribe(event_type, handler)
    
    def unsubscribe(self, event_type: str, handler: IEventHandler) -> None:
        """
        Unsubscribe from events of a specific type.
        
        Args:
            event_type: Type of events to unsubscribe from
            handler: Event handler to remove
        """
        self._event_bus.unsubscribe(event_type, handler)
    
    def register_handler(self, name: str, handler: IEventHandler) -> None:
        """
        Register an event handler.
        
        Args:
            name: Name to register the handler under
            handler: The handler to register
        """
        self._handler_registry.register(name, handler)
    
    def unregister_handler(self, name: str) -> None:
        """
        Unregister an event handler.
        
        Args:
            name: Name of the handler to unregister
        """
        self._handler_registry.unregister(name)
    
    def get_handler(self, name: str) -> Optional[IEventHandler]:
        """
        Get a registered handler by name.
        
        Args:
            name: Name of the handler to get
            
        Returns:
            The registered handler, or None if not found
        """
        return self._handler_registry.get(name)


# Common event types
class EventTypes:
    """Constants for common event types."""
    
    # Agent events
    AGENT_CREATED = "agent.created"
    AGENT_INITIALIZED = "agent.initialized"
    AGENT_MESSAGE_RECEIVED = "agent.message.received"
    AGENT_MESSAGE_SENT = "agent.message.sent"
    AGENT_ERROR = "agent.error"
    
    # Group chat events
    GROUP_CHAT_CREATED = "group_chat.created"
    GROUP_CHAT_STARTED = "group_chat.started"
    GROUP_CHAT_ENDED = "group_chat.ended"
    GROUP_CHAT_MESSAGE = "group_chat.message"
    GROUP_CHAT_ERROR = "group_chat.error"
    
    # Tool events
    TOOL_EXECUTED = "tool.executed"
    TOOL_ERROR = "tool.error"
    
    # Plugin events
    PLUGIN_LOADED = "plugin.loaded"
    PLUGIN_UNLOADED = "plugin.unloaded"
    PLUGIN_ERROR = "plugin.error"
