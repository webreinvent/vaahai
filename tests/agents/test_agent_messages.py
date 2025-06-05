"""
Tests for agent message handling functionality in VaahAI.

This module contains tests for the integration of the Message class
with agents, focusing on message processing and response generation.
"""

import pytest
import uuid
from datetime import datetime
import asyncio
from typing import Dict, Any, Union

from vaahai.agents.base import BaseAgent
from vaahai.agents.messages import Message, MessageProcessor
from vaahai.agents.exceptions import MessageValidationError


class TestAgent(BaseAgent):
    """Test agent implementation for testing message handling."""
    
    def __init__(self, agent_id=None, name=None):
        super().__init__(agent_id, name)
        self.received_messages = []
    
    async def _generate_response(self, message: Message) -> Message:
        """Generate a response to a message."""
        self.received_messages.append(message)
        
        if message.is_text_message():
            content = message.get_content()
            text = content.get("text", "")
            
            # Echo the message back with a prefix
            return Message.create_text_message(
                sender_id=self.get_id(),
                receiver_id=message.get_sender_id(),
                text=f"Echo: {text}",
                format=content.get("format", "plain"),
                in_reply_to=message.get_id(),
                conversation_id=message.get_conversation_id()
            )
        elif message.is_function_call():
            # Respond to function calls with a result
            content = message.get_content()
            function_name = content.get("name", "")
            
            return Message.create_function_result(
                sender_id=self.get_id(),
                receiver_id=message.get_sender_id(),
                function_name=function_name,
                result={"status": "success", "message": "Function executed"},
                in_reply_to=message.get_id(),
                conversation_id=message.get_conversation_id()
            )
        else:
            # Default response for other message types
            return Message.create_text_message(
                sender_id=self.get_id(),
                receiver_id=message.get_sender_id(),
                text="Received your message",
                in_reply_to=message.get_id(),
                conversation_id=message.get_conversation_id()
            )
    
    def _initialize_capabilities(self):
        """Initialize agent capabilities."""
        self.add_capability("text_processing")
        self.add_capability("function_calling")


class TestMessageProcessor(MessageProcessor):
    """Test message processor that adds metadata to messages."""
    
    async def _process_message(self, message: Message) -> Message:
        """Process a message by adding metadata."""
        message_dict = message.to_dict()
        
        # Add or update metadata
        if "metadata" not in message_dict:
            message_dict["metadata"] = {}
        
        message_dict["metadata"]["processed_by"] = "TestMessageProcessor"
        message_dict["metadata"]["processed_at"] = datetime.utcnow().isoformat()
        
        return Message(message_dict)


class TestAgentMessages:
    """Tests for agent message handling."""
    
    @pytest.mark.asyncio
    async def test_agent_process_message(self):
        """Test agent processing a message."""
        agent = TestAgent(agent_id="test_agent", name="Test Agent")
        agent.initialize({"type": "test", "name": "Test Agent"})
        
        # Create a text message
        message = Message.create_text_message(
            sender_id="user",
            receiver_id=agent.get_id(),
            text="Hello, agent!"
        )
        
        # Process the message
        response = await agent.process_message(message)
        
        # Check the response
        assert response.get_sender_id() == agent.get_id()
        assert response.get_receiver_id() == "user"
        assert response.get_content()["text"] == "Echo: Hello, agent!"
        assert response.get_in_reply_to() == message.get_id()
        assert response.get_conversation_id() == message.get_conversation_id()
    
    @pytest.mark.asyncio
    async def test_agent_process_function_call(self):
        """Test agent processing a function call message."""
        agent = TestAgent(agent_id="test_agent", name="Test Agent")
        agent.initialize({"type": "test", "name": "Test Agent"})
        
        # Create a function call message
        message = Message.create_function_call(
            sender_id="user",
            receiver_id=agent.get_id(),
            function_name="test_function",
            arguments={"arg1": "value1"}
        )
        
        # Process the message
        response = await agent.process_message(message)
        
        # Check the response
        assert response.get_sender_id() == agent.get_id()
        assert response.get_receiver_id() == "user"
        assert response.get_message_type() == "function_result"
        assert response.get_content()["name"] == "test_function"
        assert response.get_content()["result"]["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_agent_process_dict_message(self):
        """Test agent processing a message passed as a dictionary."""
        agent = TestAgent(agent_id="test_agent", name="Test Agent")
        agent.initialize({"type": "test", "name": "Test Agent"})
        
        # Create a message dictionary
        message_dict = {
            "message_id": str(uuid.uuid4()),
            "sender_id": "user",
            "receiver_id": agent.get_id(),
            "content": {"text": "Hello from dict!", "format": "plain"},
            "timestamp": datetime.utcnow().isoformat(),
            "message_type": "text",
            "conversation_id": str(uuid.uuid4())
        }
        
        # Process the message
        response = await agent.process_message(message_dict)
        
        # Check the response
        assert response.get_sender_id() == agent.get_id()
        assert response.get_receiver_id() == "user"
        assert response.get_content()["text"] == "Echo: Hello from dict!"
    
    @pytest.mark.asyncio
    async def test_agent_with_message_processor(self):
        """Test agent with a message processor."""
        agent = TestAgent(agent_id="test_agent", name="Test Agent")
        agent.initialize({"type": "test", "name": "Test Agent"})
        
        # Add a message processor
        processor = TestMessageProcessor()
        agent.add_message_processor(processor)
        
        # Create a message
        message = Message.create_text_message(
            sender_id="user",
            receiver_id=agent.get_id(),
            text="Process this message"
        )
        
        # Process the message
        response = await agent.process_message(message)
        
        # Check that the message was processed
        assert len(agent.received_messages) == 1
        processed_message = agent.received_messages[0]
        assert "metadata" in processed_message.to_dict()
        assert processed_message.get_metadata()["processed_by"] == "TestMessageProcessor"
    
    @pytest.mark.asyncio
    async def test_agent_invalid_message(self):
        """Test agent handling an invalid message."""
        agent = TestAgent(agent_id="test_agent", name="Test Agent")
        agent.initialize({"type": "test", "name": "Test Agent"})
        
        # Create an invalid message dictionary (missing required fields)
        invalid_message = {
            "sender_id": "user",
            "content": {"text": "Invalid message"}
            # Missing required fields
        }
        
        # Process the message
        response = await agent.process_message(invalid_message)
        
        # Check that an error response was generated
        assert response["message_type"] == "error"
        assert "validation_error" in response["content"]["error_type"]
    
    @pytest.mark.asyncio
    async def test_agent_error_handling(self):
        """Test agent error handling during message processing."""
        # Create a faulty agent that raises an exception
        class FaultyAgent(TestAgent):
            async def _generate_response(self, message: Message) -> Message:
                raise ValueError("Simulated error in message processing")
        
        agent = FaultyAgent(agent_id="faulty_agent", name="Faulty Agent")
        agent.initialize({"type": "test", "name": "Faulty Agent"})
        
        # Create a message
        message = Message.create_text_message(
            sender_id="user",
            receiver_id=agent.get_id(),
            text="This will cause an error"
        )
        
        # Process the message
        response = await agent.process_message(message)
        
        # Check that an error response was generated
        assert response.get_message_type() == "error"
        assert response.get_content()["error_type"] == "processing_error"
        assert "Simulated error" in response.get_content()["error_message"]
