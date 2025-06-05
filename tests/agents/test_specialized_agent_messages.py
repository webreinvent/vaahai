"""
Tests for specialized agent message handling functionality in VaahAI.

This module contains integration tests for the message handling capabilities
of specialized agent implementations.
"""

import pytest
import uuid
from datetime import datetime
import asyncio
from typing import Dict, Any, Union, List

from vaahai.agents.messages import Message, MessageProcessor
from vaahai.agents.exceptions import MessageValidationError
from tests.agents.mock_agents import MockAgentFactory


class TestSpecializedAgentMessages:
    """Tests for specialized agent message handling."""
    
    @pytest.mark.asyncio
    async def test_code_review_agent_message_handling(self):
        """Test CodeReviewAgent handling messages."""
        # Create a code review agent
        config = {
            "type": "code_review",
            "name": "Code Reviewer",
            "model": "gpt-4",
            "temperature": 0.2,
            "review_criteria": ["readability", "security", "performance"]
        }
        
        agent_factory = MockAgentFactory()
        agent = agent_factory.create_agent(config["type"], config)
        
        # Create a text message with code to review
        code_content = """
        def add_numbers(a, b):
            return a + b
        """
        
        message = Message.create_text_message(
            sender_id="user",
            receiver_id=agent.get_id(),
            text=f"Please review this code:\n```python\n{code_content}\n```",
            format="markdown"
        )
        
        # Process the message
        response = await agent.process_message(message)
        
        # Verify the response structure
        assert response.get_sender_id() == agent.get_id()
        assert response.get_receiver_id() == "user"
        assert response.is_text_message()
        assert response.get_in_reply_to() == message.get_id()
        assert response.get_conversation_id() == message.get_conversation_id()
    
    @pytest.mark.asyncio
    async def test_security_audit_agent_message_handling(self):
        """Test SecurityAuditAgent handling messages."""
        # Create a security audit agent
        config = {
            "type": "security_audit",
            "name": "Security Auditor",
            "model": "gpt-4",
            "temperature": 0.1,
            "security_checks": ["sql_injection", "xss", "csrf"]
        }
        
        agent_factory = MockAgentFactory()
        agent = agent_factory.create_agent(config["type"], config)
        
        # Create a text message with code to audit
        code_content = """
        def get_user(user_id):
            query = f"SELECT * FROM users WHERE id = {user_id}"
            return execute_query(query)
        """
        
        message = Message.create_text_message(
            sender_id="user",
            receiver_id=agent.get_id(),
            text=f"Check this code for security issues:\n```python\n{code_content}\n```",
            format="markdown"
        )
        
        # Process the message
        response = await agent.process_message(message)
        
        # Verify the response structure
        assert response.get_sender_id() == agent.get_id()
        assert response.get_receiver_id() == "user"
        assert response.is_text_message()
        assert response.get_in_reply_to() == message.get_id()
        assert response.get_conversation_id() == message.get_conversation_id()
    
    @pytest.mark.asyncio
    async def test_language_detection_agent_message_handling(self):
        """Test LanguageDetectionAgent handling messages."""
        # Create a language detection agent
        config = {
            "type": "language_detection",
            "name": "Language Detector",
            "model": "gpt-3.5-turbo",
            "temperature": 0.0
        }
        
        agent_factory = MockAgentFactory()
        agent = agent_factory.create_agent(config["type"], config)
        
        # Create a text message with code to detect language
        code_content = """
        function calculateSum(a, b) {
            return a + b;
        }
        """
        
        message = Message.create_text_message(
            sender_id="user",
            receiver_id=agent.get_id(),
            text=f"What programming language is this?\n```\n{code_content}\n```",
            format="markdown"
        )
        
        # Process the message
        response = await agent.process_message(message)
        
        # Verify the response structure
        assert response.get_sender_id() == agent.get_id()
        assert response.get_receiver_id() == "user"
        assert response.is_text_message()
        assert response.get_in_reply_to() == message.get_id()
        assert response.get_conversation_id() == message.get_conversation_id()
    
    @pytest.mark.asyncio
    async def test_report_generation_agent_message_handling(self):
        """Test ReportGenerationAgent handling messages."""
        # Create a report generation agent
        config = {
            "type": "report_generation",
            "name": "Report Generator",
            "model": "gpt-4",
            "temperature": 0.3,
            "report_formats": ["markdown", "html"]
        }
        
        agent_factory = MockAgentFactory()
        agent = agent_factory.create_agent(config["type"], config)
        
        # Create a text message requesting a report
        message = Message.create_text_message(
            sender_id="user",
            receiver_id=agent.get_id(),
            text="Generate a report on the project status with the following data: Tasks completed: 10, Tasks in progress: 5, Tasks blocked: 2",
            format="plain"
        )
        
        # Process the message
        response = await agent.process_message(message)
        
        # Verify the response structure
        assert response.get_sender_id() == agent.get_id()
        assert response.get_receiver_id() == "user"
        assert response.is_text_message()
        assert response.get_in_reply_to() == message.get_id()
        assert response.get_conversation_id() == message.get_conversation_id()
    
    @pytest.mark.asyncio
    async def test_function_call_handling(self):
        """Test agent handling function call messages."""
        # Create an assistant agent that can handle function calls
        config = {
            "type": "assistant",
            "name": "Function Handler",
            "model": "gpt-4",
            "temperature": 0.0,
            "tools": [
                {
                    "name": "get_weather",
                    "description": "Get the weather for a location",
                    "parameters": {
                        "location": {
                            "type": "string",
                            "description": "The location to get weather for"
                        }
                    }
                }
            ]
        }
        
        agent_factory = MockAgentFactory()
        agent = agent_factory.create_agent(config["type"], config)
        
        # Create a function call message
        message = Message.create_function_call(
            sender_id="user",
            receiver_id=agent.get_id(),
            function_name="get_weather",
            arguments={"location": "San Francisco"},
            description="Get weather for San Francisco"
        )
        
        # Process the message
        response = await agent.process_message(message)
        
        # Verify the response structure
        assert response.get_sender_id() == agent.get_id()
        assert response.get_receiver_id() == "user"
        assert response.is_function_result()
        assert response.get_in_reply_to() == message.get_id()
        assert response.get_conversation_id() == message.get_conversation_id()
    
    @pytest.mark.asyncio
    async def test_message_with_metadata(self):
        """Test handling messages with metadata."""
        # Create an agent
        config = {
            "type": "conversational",
            "name": "Metadata Handler",
            "model": "gpt-3.5-turbo"
        }
        
        agent_factory = MockAgentFactory()
        agent = agent_factory.create_agent(config["type"], config)
        
        # Create a message with metadata
        message_data = {
            "message_id": str(uuid.uuid4()),
            "sender_id": "user",
            "receiver_id": agent.get_id(),
            "content": {"text": "Hello with metadata", "format": "plain"},
            "timestamp": datetime.utcnow().isoformat(),
            "message_type": "text",
            "conversation_id": str(uuid.uuid4()),
            "metadata": {
                "source": "web_interface",
                "user_info": {
                    "username": "test_user",
                    "role": "developer"
                },
                "priority": "high"
            }
        }
        
        message = Message(message_data)
        
        # Process the message
        response = await agent.process_message(message)
        
        # Verify the response structure
        assert response.get_sender_id() == agent.get_id()
        assert response.get_receiver_id() == "user"
        assert response.is_text_message()
        assert response.get_in_reply_to() == message.get_id()
        assert response.get_conversation_id() == message.get_conversation_id()
    
    @pytest.mark.asyncio
    async def test_conversation_threading(self):
        """Test conversation threading with messages."""
        # Create an agent
        config = {
            "type": "conversational",
            "name": "Conversation Agent",
            "model": "gpt-3.5-turbo"
        }
        
        agent_factory = MockAgentFactory()
        agent = agent_factory.create_agent(config["type"], config)
        
        # Create a conversation with multiple messages
        conversation_id = str(uuid.uuid4())
        
        # First message
        message1 = Message.create_text_message(
            sender_id="user",
            receiver_id=agent.get_id(),
            text="Hello, how are you?",
            conversation_id=conversation_id
        )
        
        response1 = await agent.process_message(message1)
        
        # Second message, replying to the first response
        message2 = Message.create_text_message(
            sender_id="user",
            receiver_id=agent.get_id(),
            text="Tell me more about yourself",
            in_reply_to=response1.get_id(),
            conversation_id=conversation_id
        )
        
        response2 = await agent.process_message(message2)
        
        # Verify the conversation threading
        assert response1.get_conversation_id() == conversation_id
        assert response2.get_conversation_id() == conversation_id
        assert response2.get_in_reply_to() == message2.get_id()
        
        # The conversation should be maintained in the agent
        assert len(agent.get_message_history()) >= 2  # At least the 2 messages we sent
