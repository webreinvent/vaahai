"""
Integration tests for the unified detection agent with the CLI review command.

This module contains tests to verify the integration between the
LLMLanguageFrameworkCMSDetectionAgent and the VaahAI CLI review command.
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from vaahai.cli.commands.review.command import run


class TestCliDetectionIntegration(unittest.TestCase):
    """Integration tests for the unified detection agent with CLI review command."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create sample files in the temporary directory
        self.python_file_path = os.path.join(self.temp_dir.name, "test_script.py")
        with open(self.python_file_path, "w") as f:
            f.write("""
import os

def hello():
    print("Hello, world!")

if __name__ == "__main__":
    hello()
""")
        
        self.php_file_path = os.path.join(self.temp_dir.name, "test_page.php")
        with open(self.php_file_path, "w") as f:
            f.write("""
<?php
/**
 * A simple WordPress plugin file
 */

// Exit if accessed directly
if (!defined('ABSPATH')) {
    exit;
}

function wp_custom_function() {
    echo "This is a WordPress function!";
}
add_action('init', 'wp_custom_function');
?>
""")
        
        self.js_file_path = os.path.join(self.temp_dir.name, "test_component.jsx")
        with open(self.js_file_path, "w") as f:
            f.write("""
import React, { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div className="counter">
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}

export default Counter;
""")
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()
    
    @patch("vaahai.review.agents.detection.LLMLanguageFrameworkCMSDetectionAgent.run")
    def test_unified_detection_in_review_command(self, mock_run):
        """Test that unified detection is used in the review command."""
        # Mock the detection agent's run method to return a known value
        mock_run.return_value = {
            "primary_language": {"name": "Python", "confidence": 0.95},
            "primary_framework": {"name": "Django", "confidence": 0.85},
            "primary_cms": {"name": None, "confidence": 0.0}
        }
        
        # Run the CLI command with our test file
        with patch("vaahai.cli.commands.review.command.ReviewStepRegistry") as mock_registry:
            # Mock the registry to avoid running actual review steps
            mock_registry_instance = MagicMock()
            mock_registry_instance.get_all_steps.return_value = []
            mock_registry.return_value = mock_registry_instance
            
            # Mock the InquirerPy.prompt to avoid interactive prompts
            with patch("vaahai.cli.commands.review.command.prompt") as mock_prompt:
                mock_prompt.return_value = {"format": "rich"}
                
                result = self.runner.invoke(
                    run, 
                    [self.python_file_path, "--debug"],
                    catch_exceptions=False
                )
        
        # Check that our detection was called with the expected parameters
        mock_run.assert_called_once()
        
        # Check that the file path was passed as the second argument
        self.assertEqual(mock_run.call_args[0][1], self.python_file_path)
        
        # Check that the detection results appear in the output
        self.assertIn("Language: Python", result.output)
        self.assertIn("Framework: Django", result.output)
        
        # Verify the status code
        self.assertEqual(result.exit_code, 0)
    
    @patch("vaahai.review.agents.detection.LLMLanguageFrameworkCMSDetectionAgent.run")
    @patch("vaahai.agents.applications.language_detection.agent.LanguageDetectionAgent.run")
    @patch("vaahai.agents.applications.framework_detection.agent.FrameworkDetectionAgent.run")
    def test_fallback_to_separate_agents(self, mock_fw_run, mock_lang_run, mock_unified_run):
        """Test fallback to separate agents when unified detection fails."""
        # Make unified detection fail with an exception
        mock_unified_run.side_effect = Exception("Unified detection failed")
        
        # Setup mocks for the separate agents
        mock_lang_run.return_value = {
            "primary_language": {"name": "Python", "confidence": 0.9}
        }
        mock_fw_run.return_value = {
            "primary_framework": {"name": "Flask", "confidence": 0.7}
        }
        
        # Run the CLI command with our test file
        with patch("vaahai.cli.commands.review.command.ReviewStepRegistry") as mock_registry:
            # Mock the registry to avoid running actual review steps
            mock_registry_instance = MagicMock()
            mock_registry_instance.get_all_steps.return_value = []
            mock_registry.return_value = mock_registry_instance
            
            # Mock the InquirerPy.prompt to avoid interactive prompts
            with patch("vaahai.cli.commands.review.command.prompt") as mock_prompt:
                mock_prompt.return_value = {"format": "rich"}
                
                result = self.runner.invoke(
                    run, 
                    [self.python_file_path, "--debug"],
                    catch_exceptions=False
                )
        
        # Check that fallback agents were called
        mock_lang_run.assert_called_once()
        mock_fw_run.assert_called_once()
        
        # Check that the fallback detection results appear in the output
        self.assertIn("Language: Python", result.output)
        self.assertIn("Warning: Unified detection failed", result.output)
        
        # Verify the status code
        self.assertEqual(result.exit_code, 0)
    
    @patch("vaahai.review.agents.detection.LLMLanguageFrameworkCMSDetectionAgent.run")
    def test_directory_detection_with_sampling(self, mock_run):
        """Test directory detection with file sampling."""
        # Mock the detection agent's run method to return a known value
        mock_run.return_value = {
            "primary_language": {"name": "JavaScript", "confidence": 0.9},
            "primary_framework": {"name": "React", "confidence": 0.8},
            "primary_cms": {"name": None, "confidence": 0.0}
        }
        
        # Run the CLI command with our test directory
        with patch("vaahai.cli.commands.review.command.ReviewStepRegistry") as mock_registry:
            # Mock the registry to avoid running actual review steps
            mock_registry_instance = MagicMock()
            mock_registry_instance.get_all_steps.return_value = []
            mock_registry.return_value = mock_registry_instance
            
            # Mock the InquirerPy.prompt to avoid interactive prompts
            with patch("vaahai.cli.commands.review.command.prompt") as mock_prompt:
                mock_prompt.return_value = {"format": "rich"}
                
                result = self.runner.invoke(
                    run, 
                    [self.temp_dir.name, "--debug"],
                    catch_exceptions=False
                )
        
        # Check that our detection was called with the expected parameters
        mock_run.assert_called_once()
        
        # The first argument should be a string containing content from sample files
        self.assertIsInstance(mock_run.call_args[0][0], str)
        
        # The second argument should be the directory path
        self.assertEqual(mock_run.call_args[0][1], self.temp_dir.name)
        
        # Check that the detection results appear in the output
        self.assertIn("Language: JavaScript", result.output)
        self.assertIn("Framework: React", result.output)
        
        # Verify the status code
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
