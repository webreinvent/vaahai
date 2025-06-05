"""
Mock agent implementations for testing message handling.

This module contains mock implementations of agents that work with
the Message class for testing purposes.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from vaahai.agents.base import BaseAgent
from vaahai.agents.messages import Message


class MockConversationalAgent(BaseAgent):
    """Mock conversational agent for testing."""
    
    def __init__(self, agent_id=None, name=None):
        super().__init__(agent_id, name)
        self.message_history = []
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the agent with configuration."""
        self._name = config.get("name", "Mock Conversational Agent")
        self._model = config.get("model", "gpt-3.5-turbo")
        self._temperature = config.get("temperature", 0.7)
        self._initialized = True
    
    def _initialize_capabilities(self) -> None:
        """Initialize agent capabilities."""
        self.add_capability("text_processing")
    
    async def _generate_response(self, message: Message) -> Message:
        """Generate a response to the given message."""
        # Store the message in history
        self.message_history.append(message)
        
        # Create a response
        return Message.create_text_message(
            sender_id=self.get_id(),
            receiver_id=message.get_sender_id(),
            text=f"Agent {self._name} received your message.",
            in_reply_to=message.get_id(),
            conversation_id=message.get_conversation_id()
        )
    
    def get_message_history(self) -> List[Message]:
        """Get the message history."""
        return self.message_history


class MockAssistantAgent(MockConversationalAgent):
    """Mock assistant agent for testing."""
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the agent with configuration."""
        super().initialize(config)
        self._tools = config.get("tools", [])
        self._system_prompt = config.get("system_prompt", "You are a helpful assistant.")
    
    def _initialize_capabilities(self) -> None:
        """Initialize agent capabilities."""
        super()._initialize_capabilities()
        self.add_capability("function_calling")
        self.add_capability("tool_use")
    
    async def _generate_response(self, message: Message) -> Message:
        """Generate a response to the given message."""
        # Store the message in history
        self.message_history.append(message)
        
        # Handle different message types
        if message.is_text_message():
            return Message.create_text_message(
                sender_id=self.get_id(),
                receiver_id=message.get_sender_id(),
                text=f"Assistant {self._name} is processing your text request.",
                in_reply_to=message.get_id(),
                conversation_id=message.get_conversation_id()
            )
        elif message.is_function_call():
            function_name = message.get_content().get("name", "unknown")
            return Message.create_function_result(
                sender_id=self.get_id(),
                receiver_id=message.get_sender_id(),
                function_name=function_name,
                result={"status": "success", "message": f"Function {function_name} executed"},
                in_reply_to=message.get_id(),
                conversation_id=message.get_conversation_id()
            )
        else:
            return Message.create_text_message(
                sender_id=self.get_id(),
                receiver_id=message.get_sender_id(),
                text=f"Assistant {self._name} received your message.",
                in_reply_to=message.get_id(),
                conversation_id=message.get_conversation_id()
            )


class MockSpecializedAgent(MockConversationalAgent):
    """Base class for mock specialized agents."""
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the agent with configuration."""
        super().initialize(config)
        self._specialization = config.get("specialization", "general")
    
    def _initialize_capabilities(self) -> None:
        """Initialize agent capabilities."""
        super()._initialize_capabilities()
        self.add_capability("specialized_analysis")


class MockCodeReviewAgent(MockSpecializedAgent):
    """Mock code review agent for testing."""
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the agent with configuration."""
        super().initialize(config)
        self._review_criteria = config.get("review_criteria", ["readability", "security"])
    
    def _initialize_capabilities(self) -> None:
        """Initialize agent capabilities."""
        super()._initialize_capabilities()
        self.add_capability("code_analysis")
    
    async def _generate_response(self, message: Message) -> Message:
        """Generate a response to the given message."""
        # Store the message in history
        self.message_history.append(message)
        
        return Message.create_text_message(
            sender_id=self.get_id(),
            receiver_id=message.get_sender_id(),
            text=f"Code Review Agent {self._name} has analyzed your code based on: {', '.join(self._review_criteria)}.",
            in_reply_to=message.get_id(),
            conversation_id=message.get_conversation_id()
        )


class MockSecurityAuditAgent(MockSpecializedAgent):
    """Mock security audit agent for testing."""
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the agent with configuration."""
        super().initialize(config)
        self._security_checks = config.get("security_checks", ["sql_injection", "xss"])
    
    def _initialize_capabilities(self) -> None:
        """Initialize agent capabilities."""
        super()._initialize_capabilities()
        self.add_capability("security_analysis")
    
    async def _generate_response(self, message: Message) -> Message:
        """Generate a response to the given message."""
        # Store the message in history
        self.message_history.append(message)
        
        return Message.create_text_message(
            sender_id=self.get_id(),
            receiver_id=message.get_sender_id(),
            text=f"Security Audit Agent {self._name} has checked your code for: {', '.join(self._security_checks)}.",
            in_reply_to=message.get_id(),
            conversation_id=message.get_conversation_id()
        )


class MockLanguageDetectionAgent(MockSpecializedAgent):
    """Mock language detection agent for testing."""
    
    def _initialize_capabilities(self) -> None:
        """Initialize agent capabilities."""
        super()._initialize_capabilities()
        self.add_capability("language_detection")
    
    async def _generate_response(self, message: Message) -> Message:
        """Generate a response to the given message."""
        # Store the message in history
        self.message_history.append(message)
        
        return Message.create_text_message(
            sender_id=self.get_id(),
            receiver_id=message.get_sender_id(),
            text=f"Language Detection Agent {self._name} has detected the language in your code.",
            in_reply_to=message.get_id(),
            conversation_id=message.get_conversation_id()
        )


class MockReportGenerationAgent(MockSpecializedAgent):
    """Mock report generation agent for testing."""
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the agent with configuration."""
        super().initialize(config)
        self._report_formats = config.get("report_formats", ["markdown"])
    
    def _initialize_capabilities(self) -> None:
        """Initialize agent capabilities."""
        super()._initialize_capabilities()
        self.add_capability("report_generation")
    
    async def _generate_response(self, message: Message) -> Message:
        """Generate a response to the given message."""
        # Store the message in history
        self.message_history.append(message)
        
        return Message.create_text_message(
            sender_id=self.get_id(),
            receiver_id=message.get_sender_id(),
            text=f"Report Generation Agent {self._name} has generated a report in {', '.join(self._report_formats)} format.",
            in_reply_to=message.get_id(),
            conversation_id=message.get_conversation_id()
        )


class MockAgentFactory:
    """Mock agent factory for testing."""
    
    def __init__(self):
        """Initialize the mock agent factory."""
        self._agent_classes = {
            "conversational": MockConversationalAgent,
            "assistant": MockAssistantAgent,
            "specialized": MockSpecializedAgent,
            "code_review": MockCodeReviewAgent,
            "security_audit": MockSecurityAuditAgent,
            "language_detection": MockLanguageDetectionAgent,
            "report_generation": MockReportGenerationAgent
        }
    
    def create_agent(self, agent_type: str, config: Dict[str, Any]) -> BaseAgent:
        """Create an agent of the specified type."""
        if agent_type not in self._agent_classes:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent_class = self._agent_classes[agent_type]
        agent = agent_class()
        agent.initialize(config)
        return agent
