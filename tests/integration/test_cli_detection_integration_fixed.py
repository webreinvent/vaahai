"""
Integration tests for the CLI review command with detection agent.

This module contains tests to verify the integration between the
CLI review command and the unified detection agent.
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

# app will be imported in setUp after patching
# from vaahai.cli.main import app 
from vaahai.review.agents.detection import LLMLanguageFrameworkCMSDetectionAgent
from vaahai.review.runner import ReviewRunner


class TestCLIDetectionIntegration(unittest.TestCase):
    """Integration tests for the CLI review command with detection agent."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.runner = CliRunner()
        
        # Start patcher for the CLI command's run function
        self.run_command_patcher = patch("vaahai.cli.commands.review.command.run")
        self.mock_run_command = self.run_command_patcher.start()
        self.addCleanup(self.run_command_patcher.stop) # Ensure patch is stopped
        
        # Import app after patching command.run
        from vaahai.cli.main import app
        self.app = app
        
        # Create a sample Python file
        self.python_file_path = os.path.join(self.temp_dir.name, "test_script.py")
        with open(self.python_file_path, "w") as f:
            f.write("""
import os

def hello():
    print("Hello, world!")

if __name__ == "__main__":
    hello()
""")
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()
        # self.run_command_patcher.stop() # Handled by addCleanup
    
    def test_cli_review_with_detection(self):
        """Test CLI review command with detection agent."""
        # Mock the run command to avoid execution
        self.mock_run_command.return_value = None
        
        # Run the CLI command
        result = self.runner.invoke(
            self.app, 
            ["review", "run", self.python_file_path, "--format", "rich"],
            catch_exceptions=False
        )
        
        # Check that the command executed successfully
        self.assertEqual(result.exit_code, 0)
        
        # Verify that the run command was called with the correct parameters
        self.mock_run_command.assert_called_once()
        args, kwargs = self.mock_run_command.call_args
        self.assertEqual(kwargs.get("format"), "rich")
        self.assertTrue(str(kwargs.get("path")).endswith("test_script.py"))
    
    def test_cli_review_with_fallback_detection(self):
        """Test CLI review command with fallback to separate detection agents."""
        # Mock the run command to avoid execution
        self.mock_run_command.return_value = None
        
        # Run the CLI command
        result = self.runner.invoke(
            self.app, 
            ["review", "run", self.python_file_path, "--format", "rich"],
            catch_exceptions=False
        )
        
        # Check that the command executed successfully
        self.assertEqual(result.exit_code, 0)
        
        # Verify that the run command was called with the correct parameters
        self.mock_run_command.assert_called_once()
        args, kwargs = self.mock_run_command.call_args
        self.assertEqual(kwargs.get("format"), "rich")
        self.assertTrue(str(kwargs.get("path")).endswith("test_script.py"))
    
    def test_cli_review_directory_detection(self):
        """Test CLI review command with directory detection."""
        # Mock the run command to avoid execution
        self.mock_run_command.return_value = None
        
        # Create a sample directory structure
        nested_dir = os.path.join(self.temp_dir.name, "nested")
        os.makedirs(nested_dir, exist_ok=True)
        with open(os.path.join(nested_dir, "app.py"), "w") as f:
            f.write("from flask import Flask\napp = Flask(__name__)")
        
        # Run the CLI command on the directory
        result = self.runner.invoke(
            self.app, 
            ["review", "run", self.temp_dir.name, "--format", "rich"],
            catch_exceptions=False
        )
        
        # Check that the command executed successfully
        self.assertEqual(result.exit_code, 0)
        
        # Verify that the run command was called with the correct parameters
        self.mock_run_command.assert_called_once()
        args, kwargs = self.mock_run_command.call_args
        self.assertEqual(kwargs.get("format"), "rich")
        self.assertEqual(str(kwargs.get("path")), self.temp_dir.name)


if __name__ == "__main__":
    unittest.main()
