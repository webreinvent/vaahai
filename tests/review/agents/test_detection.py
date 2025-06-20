"""
Tests for the LLMLanguageFrameworkCMSDetectionAgent.

This module contains tests for the LLMLanguageFrameworkCMSDetectionAgent
which uses the default LLM provider to detect language, framework, and CMS.
"""

import json
import unittest
from unittest.mock import MagicMock, patch

import pytest

from vaahai.review.agents.detection import LLMLanguageFrameworkCMSDetectionAgent


class TestLLMLanguageFrameworkCMSDetectionAgent(unittest.TestCase):
    """Test cases for the LLMLanguageFrameworkCMSDetectionAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = {"name": "TestLLMDetection"}
        
    @patch("vaahai.review.agents.detection.get_llm_client")
    @patch("vaahai.review.agents.detection.ConfigManager")
    def test_initialization(self, mock_config_manager, mock_get_llm_client):
        """Test agent initialization."""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_manager.return_value = mock_config_instance
        mock_config_instance.get_default_llm_provider.return_value = "openai"
        mock_llm_client = MagicMock()
        mock_get_llm_client.return_value = mock_llm_client
        
        # Create agent
        agent = LLMLanguageFrameworkCMSDetectionAgent(self.config)
        
        # Verify initialization
        self.assertEqual(agent.name, "TestLLMDetection")
        mock_config_instance.get_default_llm_provider.assert_called_once()
        mock_get_llm_client.assert_called_once_with("openai")
        
    @patch("vaahai.review.agents.detection.get_llm_client")
    @patch("vaahai.review.agents.detection.ConfigManager")
    def test_run_with_valid_response(self, mock_config_manager, mock_get_llm_client):
        """Test run method with a valid LLM response."""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_manager.return_value = mock_config_instance
        mock_config_instance.get_default_llm_provider.return_value = "openai"
        mock_llm_client = MagicMock()
        mock_get_llm_client.return_value = mock_llm_client
        
        # Mock LLM response
        mock_llm_client.complete.return_value = """
        I've analyzed the code and here's what I found:
        
        ```json
        {
          "language": {"name": "Python", "confidence": 0.95},
          "framework": {"name": "Django", "confidence": 0.85},
          "cms": {"name": null, "confidence": 0.0}
        }
        ```
        """
        
        # Create agent and run detection
        agent = LLMLanguageFrameworkCMSDetectionAgent(self.config)
        result = agent.run("def hello(): print('Hello world')", "test.py")
        
        # Verify result
        self.assertEqual(result["primary_language"]["name"], "Python")
        self.assertEqual(result["primary_language"]["confidence"], 0.95)
        self.assertEqual(result["primary_framework"]["name"], "Django")
        self.assertEqual(result["primary_framework"]["confidence"], 0.85)
        self.assertIsNone(result["primary_cms"]["name"])
        self.assertEqual(result["primary_cms"]["confidence"], 0.0)
        
        # Verify prompt includes file path
        call_args = mock_llm_client.complete.call_args[0][0]
        self.assertIn("test.py", call_args)
        
    @patch("vaahai.review.agents.detection.get_llm_client")
    @patch("vaahai.review.agents.detection.ConfigManager")
    def test_run_with_single_quotes(self, mock_config_manager, mock_get_llm_client):
        """Test run method with single quotes in JSON response."""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_manager.return_value = mock_config_instance
        mock_llm_client = MagicMock()
        mock_get_llm_client.return_value = mock_llm_client
        
        # Mock LLM response with single quotes
        mock_llm_client.complete.return_value = """
        {
          'language': {'name': 'JavaScript', 'confidence': 0.9},
          'framework': {'name': 'React', 'confidence': 0.8},
          'cms': {'name': null, 'confidence': 0.0}
        }
        """
        
        # Create agent and run detection
        agent = LLMLanguageFrameworkCMSDetectionAgent(self.config)
        result = agent.run("const App = () => <div>Hello</div>")
        
        # Verify result
        self.assertEqual(result["primary_language"]["name"], "JavaScript")
        self.assertEqual(result["primary_framework"]["name"], "React")
        
    @patch("vaahai.review.agents.detection.get_llm_client")
    @patch("vaahai.review.agents.detection.ConfigManager")
    def test_run_with_invalid_response(self, mock_config_manager, mock_get_llm_client):
        """Test run method with an invalid LLM response."""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_manager.return_value = mock_config_instance
        mock_llm_client = MagicMock()
        mock_get_llm_client.return_value = mock_llm_client
        
        # Mock invalid LLM response
        mock_llm_client.complete.return_value = "This is not valid JSON"
        
        # Create agent and run detection
        agent = LLMLanguageFrameworkCMSDetectionAgent(self.config)
        result = agent.run("some code")
        
        # Verify default result on error
        self.assertEqual(result["primary_language"]["name"], "Unknown")
        self.assertEqual(result["primary_language"]["confidence"], 0.0)
        self.assertIsNone(result["primary_framework"]["name"])
        self.assertEqual(result["primary_framework"]["confidence"], 0.0)
        
    @patch("vaahai.review.agents.detection.get_llm_client")
    @patch("vaahai.review.agents.detection.ConfigManager")
    def test_run_with_missing_fields(self, mock_config_manager, mock_get_llm_client):
        """Test run method with missing fields in response."""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_manager.return_value = mock_config_instance
        mock_llm_client = MagicMock()
        mock_get_llm_client.return_value = mock_llm_client
        
        # Mock LLM response with missing fields
        mock_llm_client.complete.return_value = """
        {
          "language": {"name": "PHP", "confidence": 0.75}
        }
        """
        
        # Create agent and run detection
        agent = LLMLanguageFrameworkCMSDetectionAgent(self.config)
        result = agent.run("<?php echo 'Hello'; ?>")
        
        # Verify result with default values for missing fields
        self.assertEqual(result["primary_language"]["name"], "PHP")
        self.assertEqual(result["primary_language"]["confidence"], 0.75)
        self.assertIsNone(result["primary_framework"]["name"])
        self.assertEqual(result["primary_framework"]["confidence"], 0.0)
        self.assertIsNone(result["primary_cms"]["name"])
        self.assertEqual(result["primary_cms"]["confidence"], 0.0)
        
    @patch("vaahai.review.agents.detection.get_llm_client")
    @patch("vaahai.review.agents.detection.ConfigManager")
    def test_run_with_null_language(self, mock_config_manager, mock_get_llm_client):
        """Test run method with null language in response."""
        # Setup mocks
        mock_config_instance = MagicMock()
        mock_config_manager.return_value = mock_config_instance
        mock_llm_client = MagicMock()
        mock_get_llm_client.return_value = mock_llm_client
        
        # Mock LLM response with null language
        mock_llm_client.complete.return_value = """
        {
          "language": {"name": null, "confidence": 0.0},
          "framework": {"name": null, "confidence": 0.0},
          "cms": {"name": null, "confidence": 0.0}
        }
        """
        
        # Create agent and run detection
        agent = LLMLanguageFrameworkCMSDetectionAgent(self.config)
        result = agent.run("some unknown code")
        
        # Verify result with "Unknown" for null language
        self.assertEqual(result["primary_language"]["name"], "Unknown")
        self.assertEqual(result["primary_language"]["confidence"], 0.0)
