"""
Tests for the agent factory implementation.

This module tests the agent factory's ability to create different types of agents
and validate their configurations.
"""

import unittest
from unittest.mock import patch, MagicMock
import asyncio
import logging

from vaahai.agents.factory import AgentFactory
from vaahai.agents.exceptions import AgentTypeNotFoundError, AgentInitializationError
from vaahai.agents.impl import (
    ConversationalAgent,
    AssistantAgent,
    UserProxyAgent,
    SpecializedAgent,
    CodeReviewAgent,
    SecurityAuditAgent,
    LanguageDetectionAgent,
    ReportGenerationAgent
)


class TestAgentFactory(unittest.TestCase):
    """Test cases for the agent factory."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = AgentFactory()
        logging.basicConfig(level=logging.ERROR)  # Suppress log messages during tests

    def test_factory_initialization(self):
        """Test that the factory initializes with default agent types."""
        agent_types = self.factory.list_components()
        expected_types = [
            "conversational", "assistant", "user_proxy", "specialized",
            "code_review", "security_audit", "language_detection", "report_generation"
        ]
        for agent_type in expected_types:
            self.assertIn(agent_type, agent_types)

    def test_create_conversational_agent(self):
        """Test creating a conversational agent."""
        config = {
            "name": "Test Conversational Agent",
            "type": "conversational",
            "max_history_length": 10
        }
        agent = self.factory.create_agent("conversational", config)
        self.assertIsInstance(agent, ConversationalAgent)
        self.assertEqual(agent.get_name(), "ConversationalAgent")

    def test_create_assistant_agent(self):
        """Test creating an assistant agent."""
        config = {
            "name": "Test Assistant Agent",
            "type": "assistant",
            "system_prompt": "You are a helpful assistant.",
            "tools": []
        }
        agent = self.factory.create_agent("assistant", config)
        self.assertIsInstance(agent, AssistantAgent)
        self.assertEqual(agent.get_name(), "AssistantAgent")

    def test_create_user_proxy_agent(self):
        """Test creating a user proxy agent."""
        config = {
            "name": "Test User Proxy Agent",
            "type": "user_proxy",
            "human_input_mode": "ALWAYS"
        }
        agent = self.factory.create_agent("user_proxy", config)
        self.assertIsInstance(agent, UserProxyAgent)
        self.assertEqual(agent.get_name(), "UserProxyAgent")

    def test_create_specialized_agents(self):
        """Test creating specialized agents."""
        specialized_configs = {
            "code_review": {
                "name": "Test Code Review Agent",
                "type": "code_review",
                "domain": "code_quality",
                "expertise": ["python", "code_review"],
                "languages": ["python", "javascript"],
                "review_criteria": ["style", "complexity"]
            },
            "security_audit": {
                "name": "Test Security Audit Agent",
                "type": "security_audit",
                "domain": "security",
                "expertise": ["web_security", "penetration_testing"],
                "compliance_standards": ["OWASP", "PCI-DSS"],
                "vulnerability_categories": ["injection", "xss"]
            },
            "language_detection": {
                "name": "Test Language Detection Agent",
                "type": "language_detection",
                "domain": "language_analysis",
                "expertise": ["programming_languages", "syntax_analysis"],
                "detectable_languages": ["python", "javascript", "java"]
            },
            "report_generation": {
                "name": "Test Report Generation Agent",
                "type": "report_generation",
                "domain": "reporting",
                "expertise": ["technical_documentation", "data_visualization"],
                "supported_formats": ["markdown", "html"],
                "visualization_types": ["table", "chart"]
            }
        }

        for agent_type, config in specialized_configs.items():
            agent = self.factory.create_agent(agent_type, config)
            self.assertEqual(agent.get_name(), config["name"])
            self.assertEqual(agent.get_domain(), config["domain"])
            self.assertEqual(agent.get_expertise(), config["expertise"])

    def test_invalid_agent_type(self):
        """Test that creating an invalid agent type raises an error."""
        with self.assertRaises(AgentTypeNotFoundError):
            self.factory.create_agent("nonexistent_agent_type", {})

    @patch('vaahai.agents.impl.conversational.ConversationalAgent.process_message')
    async def test_agent_process_message(self, mock_process_message):
        """Test that agents can process messages."""
        mock_process_message.return_value = "Response from agent"
        
        config = {
            "name": "Test Agent",
            "type": "conversational"
        }
        agent = self.factory.create_agent("conversational", config)
        
        response = await agent.process_message("Hello, agent!")
        mock_process_message.assert_called_once_with("Hello, agent!")
        self.assertEqual(response, "Response from agent")

    def test_convenience_methods(self):
        """Test the convenience methods for creating agents."""
        config = {
            "name": "Test Agent",
            "type": "conversational"
        }
        
        conversational = AgentFactory.create_conversational_agent(config)
        self.assertIsInstance(conversational, ConversationalAgent)
        
        assistant_config = {
            "name": "Test Agent",
            "type": "assistant"
        }
        assistant = AgentFactory.create_assistant_agent(assistant_config)
        self.assertIsInstance(assistant, AssistantAgent)
        
        user_proxy_config = {
            "name": "Test User Proxy Agent",
            "type": "user_proxy"
        }
        user_proxy = AgentFactory.create_user_proxy_agent(user_proxy_config)
        self.assertIsInstance(user_proxy, UserProxyAgent)
        
        code_review_config = {
            "name": "Test Agent",
            "type": "code_review",
            "domain": "code_quality",
            "expertise": ["python", "code_review"]
        }
        code_review = AgentFactory.create_code_review_agent(code_review_config)
        self.assertIsInstance(code_review, CodeReviewAgent)
        
        security_audit_config = {
            "name": "Test Agent",
            "type": "security_audit",
            "domain": "security",
            "expertise": ["web_security"]
        }
        security_audit = AgentFactory.create_security_audit_agent(security_audit_config)
        self.assertIsInstance(security_audit, SecurityAuditAgent)
        
        language_detection_config = {
            "name": "Test Agent",
            "type": "language_detection",
            "domain": "language_analysis",
            "expertise": ["programming_languages"]
        }
        language_detection = AgentFactory.create_language_detection_agent(language_detection_config)
        self.assertIsInstance(language_detection, LanguageDetectionAgent)
        
        report_generation_config = {
            "name": "Test Agent",
            "type": "report_generation",
            "domain": "reporting",
            "expertise": ["technical_documentation"]
        }
        report_generation = AgentFactory.create_report_generation_agent(report_generation_config)
        self.assertIsInstance(report_generation, ReportGenerationAgent)


def run_async_test(coro):
    """Helper function to run async tests."""
    return asyncio.run(coro)


if __name__ == '__main__':
    unittest.main()
