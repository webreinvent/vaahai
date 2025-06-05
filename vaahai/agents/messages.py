"""
VaahAI Message Handling

This module provides functionality for creating, validating, and processing
messages exchanged between agents in the VaahAI system.
"""

import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Union

import jsonschema

from .message_schema import BASE_MESSAGE_SCHEMA, get_message_schema
from .exceptions import MessageValidationError

logger = logging.getLogger(__name__)


class Message:
    """
    Represents a message exchanged between agents in the VaahAI system.
    
    This class provides methods for creating, validating, and manipulating
    messages according to the VaahAI message schema.
    """
    
    def __init__(self, message_data: Dict[str, Any]):
        """
        Initialize a message from a dictionary.
        
        Args:
            message_data: Dictionary containing message data
            
        Raises:
            MessageValidationError: If the message data is invalid
        """
        self._data = message_data.copy()
        self._validate()
    
    @classmethod
    def create(cls, 
               sender_id: str,
               receiver_id: Optional[str],
               content: Dict[str, Any],
               message_type: str,
               sender_name: Optional[str] = None,
               message_id: Optional[str] = None,
               in_reply_to: Optional[str] = None,
               conversation_id: Optional[str] = None,
               metadata: Optional[Dict[str, Any]] = None) -> 'Message':
        """
        Create a new message.
        
        Args:
            sender_id: ID of the agent sending the message
            receiver_id: ID of the agent receiving the message, or None for broadcast
            content: Content of the message
            message_type: Type of message content
            sender_name: Name of the agent sending the message
            message_id: Unique identifier for the message (generated if not provided)
            in_reply_to: ID of the message this is a reply to, if applicable
            conversation_id: ID of the conversation this message belongs to
            metadata: Additional metadata for the message
            
        Returns:
            A new Message instance
            
        Raises:
            MessageValidationError: If the message data is invalid
        """
        message_data = {
            "message_id": message_id or str(uuid.uuid4()),
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "message_type": message_type,
        }
        
        if sender_name:
            message_data["sender_name"] = sender_name
        
        if in_reply_to:
            message_data["in_reply_to"] = in_reply_to
            
        if conversation_id:
            message_data["conversation_id"] = conversation_id
        else:
            message_data["conversation_id"] = str(uuid.uuid4())
            
        if metadata:
            message_data["metadata"] = metadata
            
        return cls(message_data)
    
    @classmethod
    def create_text_message(cls,
                           sender_id: str,
                           receiver_id: Optional[str],
                           text: str,
                           format: str = "plain",
                           **kwargs) -> 'Message':
        """
        Create a new text message.
        
        Args:
            sender_id: ID of the agent sending the message
            receiver_id: ID of the agent receiving the message, or None for broadcast
            text: Text content of the message
            format: Format of the text content (plain, markdown, html)
            **kwargs: Additional arguments to pass to Message.create
            
        Returns:
            A new Message instance with text content
        """
        content = {
            "text": text,
            "format": format
        }
        
        return cls.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            message_type="text",
            **kwargs
        )
    
    @classmethod
    def create_function_call(cls,
                            sender_id: str,
                            receiver_id: Optional[str],
                            function_name: str,
                            arguments: Dict[str, Any],
                            description: Optional[str] = None,
                            **kwargs) -> 'Message':
        """
        Create a new function call message.
        
        Args:
            sender_id: ID of the agent sending the message
            receiver_id: ID of the agent receiving the message, or None for broadcast
            function_name: Name of the function to call
            arguments: Arguments to pass to the function
            description: Description of what the function call does
            **kwargs: Additional arguments to pass to Message.create
            
        Returns:
            A new Message instance with function call content
        """
        content = {
            "name": function_name,
            "arguments": arguments
        }
        
        if description:
            content["description"] = description
            
        return cls.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            message_type="function_call",
            **kwargs
        )
    
    @classmethod
    def create_function_result(cls,
                              sender_id: str,
                              receiver_id: Optional[str],
                              function_name: str,
                              result: Any,
                              error: Optional[str] = None,
                              **kwargs) -> 'Message':
        """
        Create a new function result message.
        
        Args:
            sender_id: ID of the agent sending the message
            receiver_id: ID of the agent receiving the message, or None for broadcast
            function_name: Name of the function that was called
            result: Result of the function call
            error: Error message if the function call failed
            **kwargs: Additional arguments to pass to Message.create
            
        Returns:
            A new Message instance with function result content
        """
        content = {
            "name": function_name,
            "result": result
        }
        
        if error:
            content["error"] = error
            
        return cls.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            message_type="function_result",
            **kwargs
        )
    
    @classmethod
    def create_error_message(cls,
                            sender_id: str,
                            receiver_id: Optional[str],
                            error_type: str,
                            error_message: str,
                            traceback: Optional[str] = None,
                            **kwargs) -> 'Message':
        """
        Create a new error message.
        
        Args:
            sender_id: ID of the agent sending the message
            receiver_id: ID of the agent receiving the message, or None for broadcast
            error_type: Type of error
            error_message: Error message
            traceback: Error traceback
            **kwargs: Additional arguments to pass to Message.create
            
        Returns:
            A new Message instance with error content
        """
        content = {
            "error_type": error_type,
            "error_message": error_message
        }
        
        if traceback:
            content["traceback"] = traceback
            
        return cls.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            message_type="error",
            **kwargs
        )
    
    @classmethod
    def create_system_message(cls,
                             sender_id: str,
                             receiver_id: Optional[str],
                             system_message_type: str,
                             system_message: str,
                             **kwargs) -> 'Message':
        """
        Create a new system message.
        
        Args:
            sender_id: ID of the agent sending the message
            receiver_id: ID of the agent receiving the message, or None for broadcast
            system_message_type: Type of system message (info, warning, error, debug)
            system_message: System message content
            **kwargs: Additional arguments to pass to Message.create
            
        Returns:
            A new Message instance with system content
        """
        content = {
            "system_message_type": system_message_type,
            "system_message": system_message
        }
        
        return cls.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            message_type="system",
            **kwargs
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the message to a dictionary.
        
        Returns:
            Dictionary representation of the message
        """
        return self._data.copy()
    
    def get_id(self) -> str:
        """
        Get the message ID.
        
        Returns:
            Message ID
        """
        return self._data["message_id"]
    
    def get_sender_id(self) -> str:
        """
        Get the sender ID.
        
        Returns:
            Sender ID
        """
        return self._data["sender_id"]
    
    def set_sender_id(self, sender_id: str) -> None:
        """
        Set the sender ID.
        
        Args:
            sender_id: New sender ID
        """
        self._data["sender_id"] = sender_id
    
    def get_receiver_id(self) -> Optional[str]:
        """
        Get the receiver ID.
        
        Returns:
            Receiver ID, or None for broadcast
        """
        return self._data["receiver_id"]
    
    def get_content(self) -> Dict[str, Any]:
        """
        Get the message content.
        
        Returns:
            Message content
        """
        return self._data["content"].copy()
    
    def get_timestamp(self) -> str:
        """
        Get the message timestamp.
        
        Returns:
            ISO 8601 timestamp string
        """
        return self._data["timestamp"]
    
    def get_message_type(self) -> str:
        """
        Get the message type.
        
        Returns:
            Message type
        """
        return self._data["message_type"]
    
    def get_in_reply_to(self) -> Optional[str]:
        """
        Get the ID of the message this is a reply to.
        
        Returns:
            Message ID, or None if not a reply
        """
        return self._data.get("in_reply_to")
    
    def get_conversation_id(self) -> str:
        """
        Get the conversation ID.
        
        Returns:
            Conversation ID
        """
        return self._data["conversation_id"]
    
    def set_conversation_id(self, conversation_id: str) -> None:
        """
        Set the conversation ID.
        
        Args:
            conversation_id: New conversation ID
        """
        self._data["conversation_id"] = conversation_id
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get the message metadata.
        
        Returns:
            Message metadata, or empty dict if none
        """
        return self._data.get("metadata", {}).copy()
    
    def is_text_message(self) -> bool:
        """
        Check if this is a text message.
        
        Returns:
            True if this is a text message, False otherwise
        """
        return self._data["message_type"] == "text"
    
    def is_function_call(self) -> bool:
        """
        Check if this is a function call message.
        
        Returns:
            True if this is a function call message, False otherwise
        """
        return self._data["message_type"] == "function_call"
    
    def is_function_result(self) -> bool:
        """
        Check if this is a function result message.
        
        Returns:
            True if this is a function result message, False otherwise
        """
        return self._data["message_type"] == "function_result"
    
    def is_error_message(self) -> bool:
        """
        Check if this is an error message.
        
        Returns:
            True if this is an error message, False otherwise
        """
        return self._data["message_type"] == "error"
    
    def is_system_message(self) -> bool:
        """
        Check if this is a system message.
        
        Returns:
            True if this is a system message, False otherwise
        """
        return self._data["message_type"] == "system"
    
    def _validate(self) -> None:
        """
        Validate the message data against the schema.
        
        Raises:
            MessageValidationError: If the message data is invalid
        """
        try:
            # Validate against base message schema
            jsonschema.validate(self._data, BASE_MESSAGE_SCHEMA)
            
            # Validate content against specific schema for message type
            message_type = self._data["message_type"]
            content_schema = get_message_schema(message_type)
            jsonschema.validate(self._data["content"], content_schema)
        except jsonschema.exceptions.ValidationError as e:
            raise MessageValidationError(f"Invalid message: {e}")
        except ValueError as e:
            raise MessageValidationError(str(e))


class MessageProcessor:
    """
    Processes messages according to a defined strategy.
    
    This class provides a base implementation of the IMessageProcessor
    interface for processing messages.
    """
    
    async def process(self, message: Union[Message, Dict[str, Any]]) -> Message:
        """
        Process a message according to the processor's strategy.
        
        Args:
            message: The message to process, either as a Message object or a dict
            
        Returns:
            The processed message as a Message object
        """
        if isinstance(message, dict):
            message = Message(message)
            
        return await self._process_message(message)
    
    async def _process_message(self, message: Message) -> Message:
        """
        Process a message according to the processor's strategy.
        
        This method should be overridden by subclasses to implement
        specific processing strategies.
        
        Args:
            message: The message to process
            
        Returns:
            The processed message
        """
        return message


class MessageBus:
    """
    Routes messages between agents in the VaahAI system.
    
    The message bus is responsible for delivering messages to their
    intended recipients and maintaining a record of message history.
    """
    
    def __init__(self):
        """Initialize a new message bus."""
        self._subscribers = {}
        self._history = []
        self._processors = []
    
    async def publish(self, message: Union[Message, Dict[str, Any]]) -> Message:
        """
        Publish a message to the bus.
        
        Args:
            message: The message to publish, either as a Message object or a dict
            
        Returns:
            The published message as a Message object
        """
        if isinstance(message, dict):
            message = Message(message)
            
        # Process the message through all registered processors
        processed_message = message
        for processor in self._processors:
            processed_message = await processor.process(processed_message)
            
        # Add to history
        self._history.append(processed_message)
        
        # Deliver to subscribers
        await self._deliver(processed_message)
        
        return processed_message
    
    async def _deliver(self, message: Message) -> None:
        """
        Deliver a message to its intended recipients.
        
        Args:
            message: The message to deliver
        """
        receiver_id = message.get_receiver_id()
        
        if receiver_id is None:
            # Broadcast to all subscribers
            for callback in self._subscribers.values():
                await callback(message)
        elif receiver_id in self._subscribers:
            # Deliver to specific recipient
            await self._subscribers[receiver_id](message)
        else:
            logger.warning(f"No subscriber found for message to {receiver_id}")
    
    def subscribe(self, agent_id: str, callback: callable) -> None:
        """
        Subscribe to messages.
        
        Args:
            agent_id: ID of the agent subscribing
            callback: Function to call when a message is received
        """
        self._subscribers[agent_id] = callback
    
    def unsubscribe(self, agent_id: str) -> None:
        """
        Unsubscribe from messages.
        
        Args:
            agent_id: ID of the agent unsubscribing
        """
        if agent_id in self._subscribers:
            del self._subscribers[agent_id]
    
    def add_processor(self, processor: MessageProcessor) -> None:
        """
        Add a message processor to the bus.
        
        Args:
            processor: The processor to add
        """
        self._processors.append(processor)
    
    def remove_processor(self, processor: MessageProcessor) -> None:
        """
        Remove a message processor from the bus.
        
        Args:
            processor: The processor to remove
        """
        if processor in self._processors:
            self._processors.remove(processor)
    
    def get_history(self) -> List[Message]:
        """
        Get the message history.
        
        Returns:
            List of messages in the history
        """
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear the message history."""
        self._history = []
