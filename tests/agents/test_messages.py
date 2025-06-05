"""
Tests for the message handling functionality in VaahAI.

This module contains tests for the Message class, MessageProcessor,
and MessageBus classes, as well as their integration with agents.
"""

import pytest
import uuid
from datetime import datetime
import asyncio
from typing import Dict, Any

from vaahai.agents.messages import Message, MessageProcessor, MessageBus
from vaahai.agents.exceptions import MessageValidationError


class TestMessage:
    """Tests for the Message class."""
    
    def test_create_message(self):
        """Test creating a message."""
        sender_id = "agent1"
        receiver_id = "agent2"
        content = {"text": "Hello, world!", "format": "plain"}
        message_type = "text"
        
        message = Message.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            message_type=message_type
        )
        
        assert message.get_sender_id() == sender_id
        assert message.get_receiver_id() == receiver_id
        assert message.get_content() == content
        assert message.get_message_type() == message_type
        assert message.get_id() is not None
        assert message.get_timestamp() is not None
        assert message.get_conversation_id() is not None
    
    def test_create_text_message(self):
        """Test creating a text message."""
        sender_id = "agent1"
        receiver_id = "agent2"
        text = "Hello, world!"
        format = "markdown"
        
        message = Message.create_text_message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            text=text,
            format=format
        )
        
        assert message.get_sender_id() == sender_id
        assert message.get_receiver_id() == receiver_id
        assert message.get_message_type() == "text"
        assert message.get_content()["text"] == text
        assert message.get_content()["format"] == format
        assert message.is_text_message() is True
    
    def test_create_function_call(self):
        """Test creating a function call message."""
        sender_id = "agent1"
        receiver_id = "agent2"
        function_name = "test_function"
        arguments = {"arg1": "value1", "arg2": 42}
        description = "Test function call"
        
        message = Message.create_function_call(
            sender_id=sender_id,
            receiver_id=receiver_id,
            function_name=function_name,
            arguments=arguments,
            description=description
        )
        
        assert message.get_sender_id() == sender_id
        assert message.get_receiver_id() == receiver_id
        assert message.get_message_type() == "function_call"
        assert message.get_content()["name"] == function_name
        assert message.get_content()["arguments"] == arguments
        assert message.get_content()["description"] == description
        assert message.is_function_call() is True
    
    def test_create_function_result(self):
        """Test creating a function result message."""
        sender_id = "agent1"
        receiver_id = "agent2"
        function_name = "test_function"
        result = {"status": "success", "data": {"key": "value"}}
        
        message = Message.create_function_result(
            sender_id=sender_id,
            receiver_id=receiver_id,
            function_name=function_name,
            result=result
        )
        
        assert message.get_sender_id() == sender_id
        assert message.get_receiver_id() == receiver_id
        assert message.get_message_type() == "function_result"
        assert message.get_content()["name"] == function_name
        assert message.get_content()["result"] == result
        assert message.is_function_result() is True
    
    def test_create_error_message(self):
        """Test creating an error message."""
        sender_id = "agent1"
        receiver_id = "agent2"
        error_type = "validation_error"
        error_message = "Invalid input"
        traceback = "Traceback (most recent call last):\n  ..."
        
        message = Message.create_error_message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            error_type=error_type,
            error_message=error_message,
            traceback=traceback
        )
        
        assert message.get_sender_id() == sender_id
        assert message.get_receiver_id() == receiver_id
        assert message.get_message_type() == "error"
        assert message.get_content()["error_type"] == error_type
        assert message.get_content()["error_message"] == error_message
        assert message.get_content()["traceback"] == traceback
        assert message.is_error_message() is True
    
    def test_create_system_message(self):
        """Test creating a system message."""
        sender_id = "agent1"
        receiver_id = "agent2"
        system_message_type = "info"
        system_message = "System is starting up"
        
        message = Message.create_system_message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            system_message_type=system_message_type,
            system_message=system_message
        )
        
        assert message.get_sender_id() == sender_id
        assert message.get_receiver_id() == receiver_id
        assert message.get_message_type() == "system"
        assert message.get_content()["system_message_type"] == system_message_type
        assert message.get_content()["system_message"] == system_message
        assert message.is_system_message() is True
    
    def test_message_validation(self):
        """Test message validation."""
        # Valid message
        valid_message_data = {
            "message_id": str(uuid.uuid4()),
            "sender_id": "agent1",
            "receiver_id": "agent2",
            "content": {"text": "Hello, world!", "format": "plain"},
            "timestamp": datetime.utcnow().isoformat(),
            "message_type": "text",
            "conversation_id": str(uuid.uuid4())
        }
        
        message = Message(valid_message_data)
        assert message.get_id() == valid_message_data["message_id"]
        
        # Invalid message (missing required field)
        invalid_message_data = {
            "sender_id": "agent1",
            "content": {"text": "Hello, world!", "format": "plain"},
            "timestamp": datetime.utcnow().isoformat(),
            "message_type": "text"
        }
        
        with pytest.raises(MessageValidationError):
            Message(invalid_message_data)
        
        # Invalid message (invalid content for message type)
        invalid_content_data = {
            "message_id": str(uuid.uuid4()),
            "sender_id": "agent1",
            "receiver_id": "agent2",
            "content": {"invalid_field": "value"},
            "timestamp": datetime.utcnow().isoformat(),
            "message_type": "text",
            "conversation_id": str(uuid.uuid4())
        }
        
        with pytest.raises(MessageValidationError):
            Message(invalid_content_data)


class TestMessageProcessor:
    """Tests for the MessageProcessor class."""
    
    class TestProcessor(MessageProcessor):
        """Test message processor that adds a field to the message content."""
        
        async def _process_message(self, message: Message) -> Message:
            content = message.get_content()
            if message.is_text_message():
                content["processed"] = True
                return Message.create(
                    sender_id=message.get_sender_id(),
                    receiver_id=message.get_receiver_id(),
                    content=content,
                    message_type=message.get_message_type(),
                    message_id=message.get_id(),
                    in_reply_to=message.get_in_reply_to(),
                    conversation_id=message.get_conversation_id()
                )
            return message
    
    @pytest.mark.asyncio
    async def test_process_message(self):
        """Test processing a message."""
        processor = self.TestProcessor()
        
        # Create a text message
        message = Message.create_text_message(
            sender_id="agent1",
            receiver_id="agent2",
            text="Hello, world!"
        )
        
        # Process the message
        processed_message = await processor.process(message)
        
        # Check that the message was processed
        assert processed_message.get_content()["processed"] is True
        assert processed_message.get_content()["text"] == "Hello, world!"
    
    @pytest.mark.asyncio
    async def test_process_dict_message(self):
        """Test processing a message passed as a dictionary."""
        processor = self.TestProcessor()
        
        # Create a message dictionary
        message_dict = {
            "message_id": str(uuid.uuid4()),
            "sender_id": "agent1",
            "receiver_id": "agent2",
            "content": {"text": "Hello, world!", "format": "plain"},
            "timestamp": datetime.utcnow().isoformat(),
            "message_type": "text",
            "conversation_id": str(uuid.uuid4())
        }
        
        # Process the message
        processed_message = await processor.process(message_dict)
        
        # Check that the message was processed
        assert processed_message.get_content()["processed"] is True
        assert processed_message.get_content()["text"] == "Hello, world!"


class TestMessageBus:
    """Tests for the MessageBus class."""
    
    @pytest.mark.asyncio
    async def test_publish_and_subscribe(self):
        """Test publishing and subscribing to messages."""
        bus = MessageBus()
        
        # Create a message
        message = Message.create_text_message(
            sender_id="agent1",
            receiver_id="agent2",
            text="Hello, agent2!"
        )
        
        # Set up a subscriber
        received_messages = []
        
        async def message_handler(msg):
            received_messages.append(msg)
        
        # Subscribe to messages
        bus.subscribe("agent2", message_handler)
        
        # Publish the message
        await bus.publish(message)
        
        # Check that the message was received
        assert len(received_messages) == 1
        assert received_messages[0].get_sender_id() == "agent1"
        assert received_messages[0].get_receiver_id() == "agent2"
        assert received_messages[0].get_content()["text"] == "Hello, agent2!"
    
    @pytest.mark.asyncio
    async def test_broadcast_message(self):
        """Test broadcasting a message to all subscribers."""
        bus = MessageBus()
        
        # Create a broadcast message
        message = Message.create_text_message(
            sender_id="agent1",
            receiver_id=None,  # Broadcast
            text="Hello, everyone!"
        )
        
        # Set up subscribers
        agent2_messages = []
        agent3_messages = []
        
        async def agent2_handler(msg):
            agent2_messages.append(msg)
        
        async def agent3_handler(msg):
            agent3_messages.append(msg)
        
        # Subscribe to messages
        bus.subscribe("agent2", agent2_handler)
        bus.subscribe("agent3", agent3_handler)
        
        # Publish the message
        await bus.publish(message)
        
        # Check that both subscribers received the message
        assert len(agent2_messages) == 1
        assert len(agent3_messages) == 1
        assert agent2_messages[0].get_content()["text"] == "Hello, everyone!"
        assert agent3_messages[0].get_content()["text"] == "Hello, everyone!"
    
    @pytest.mark.asyncio
    async def test_message_processors(self):
        """Test adding message processors to the bus."""
        bus = MessageBus()
        
        # Create a test processor
        class TestProcessor(MessageProcessor):
            async def _process_message(self, message: Message) -> Message:
                if message.is_text_message():
                    content = message.get_content()
                    content["processed"] = True
                    return Message.create(
                        sender_id=message.get_sender_id(),
                        receiver_id=message.get_receiver_id(),
                        content=content,
                        message_type=message.get_message_type(),
                        message_id=message.get_id(),
                        in_reply_to=message.get_in_reply_to(),
                        conversation_id=message.get_conversation_id()
                    )
                return message
        
        processor = TestProcessor()
        bus.add_processor(processor)
        
        # Create a message
        message = Message.create_text_message(
            sender_id="agent1",
            receiver_id="agent2",
            text="Hello, agent2!"
        )
        
        # Set up a subscriber
        received_messages = []
        
        async def message_handler(msg):
            received_messages.append(msg)
        
        # Subscribe to messages
        bus.subscribe("agent2", message_handler)
        
        # Publish the message
        await bus.publish(message)
        
        # Check that the message was processed
        assert len(received_messages) == 1
        assert received_messages[0].get_content()["processed"] is True
    
    @pytest.mark.asyncio
    async def test_message_history(self):
        """Test message history in the bus."""
        bus = MessageBus()
        
        # Create and publish some messages
        message1 = Message.create_text_message(
            sender_id="agent1",
            receiver_id="agent2",
            text="Message 1"
        )
        
        message2 = Message.create_text_message(
            sender_id="agent2",
            receiver_id="agent1",
            text="Message 2"
        )
        
        await bus.publish(message1)
        await bus.publish(message2)
        
        # Check the history
        history = bus.get_history()
        assert len(history) == 2
        assert history[0].get_content()["text"] == "Message 1"
        assert history[1].get_content()["text"] == "Message 2"
        
        # Clear the history
        bus.clear_history()
        assert len(bus.get_history()) == 0
    
    @pytest.mark.asyncio
    async def test_unsubscribe(self):
        """Test unsubscribing from the bus."""
        bus = MessageBus()
        
        # Create a message
        message = Message.create_text_message(
            sender_id="agent1",
            receiver_id="agent2",
            text="Hello, agent2!"
        )
        
        # Set up a subscriber
        received_messages = []
        
        async def message_handler(msg):
            received_messages.append(msg)
        
        # Subscribe to messages
        bus.subscribe("agent2", message_handler)
        
        # Publish a message
        await bus.publish(message)
        assert len(received_messages) == 1
        
        # Unsubscribe
        bus.unsubscribe("agent2")
        
        # Publish another message
        await bus.publish(message)
        
        # Check that no new message was received
        assert len(received_messages) == 1
