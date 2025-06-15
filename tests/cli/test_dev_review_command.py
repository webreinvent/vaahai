"""
Tests for the developer review command.
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from typer.testing import CliRunner

from vaahai.cli.main import app


class TestDevReviewCommand(unittest.TestCase):
    """Tests for the developer review command."""
    
    def setUp(self):
        """Set up test environment."""
        self.runner = CliRunner()
        
        # Create a patch for the standard review run function
        self.review_run_patcher = patch('vaahai.cli.commands.dev_review.command.standard_review_run')
        self.mock_review_run = self.review_run_patcher.start()
        
        # Create a mock result for the review run
        self.mock_result = MagicMock()
        self.mock_result.step_timings = {
            "security.sql_injection": 1.23,
            "security.hardcoded_secrets": 0.87,
            "performance.inefficient_loops": 0.45
        }
        self.mock_review_run.return_value = self.mock_result
        
        # Create a patch for config validation
        self.config_validation_patcher = patch('vaahai.cli.commands.dev_review.command.display_config_warnings')
        self.mock_config_validation = self.config_validation_patcher.start()
        self.mock_config_validation.return_value = True
    
    def tearDown(self):
        """Clean up test environment."""
        self.review_run_patcher.stop()
        self.config_validation_patcher.stop()
    
    def test_dev_review_basic(self):
        """Test basic developer review command."""
        result = self.runner.invoke(app, ["dev", "review", "run", "./test_file.py"])
        
        # Check that the command executed successfully
        self.assertEqual(result.exit_code, 0)
        
        # Check that the review run function was called with the correct arguments
        self.mock_review_run.assert_called_once_with(
            path="./test_file.py",
            format=None,
            apply_changes=False,
            dry_run=False,
            backup_dir=None,
            no_confirm=False,
        )
    
    def test_dev_review_with_debug_level(self):
        """Test developer review command with debug level."""
        result = self.runner.invoke(app, ["dev", "review", "run", "./test_file.py", "--debug-level", "debug"])
        
        # Check that the command executed successfully
        self.assertEqual(result.exit_code, 0)
        
        # Check that the review run function was called
        self.mock_review_run.assert_called_once()
    
    def test_dev_review_with_show_config(self):
        """Test developer review command with show config option."""
        result = self.runner.invoke(app, ["dev", "review", "run", "./test_file.py", "--show-config"])
        
        # Check that the command executed successfully
        self.assertEqual(result.exit_code, 0)
        
        # Check that the config validation function was called
        self.mock_config_validation.assert_called_once_with(show_all=True)
    
    def test_dev_review_with_show_steps(self):
        """Test developer review command with show steps option."""
        # Run the command with show-steps option
        result = self.runner.invoke(app, ["dev", "review", "run", "./test_file.py", "--show-steps"])
        
        # Check that the command executed successfully
        self.assertEqual(result.exit_code, 0)
        
        # Check that the VAAHAI_STEP_TIMING environment variable was set
        self.mock_review_run.assert_called_once()
        
        # The environment variable should be set in the command implementation
        # We can't easily check it here since it's set within the process
    
    def test_dev_review_with_format_option(self):
        """Test developer review command with format option."""
        result = self.runner.invoke(app, ["dev", "review", "run", "./test_file.py", "--format", "html"])
        
        # Check that the command executed successfully
        self.assertEqual(result.exit_code, 0)
        
        # Check that the review run function was called with the correct format
        self.mock_review_run.assert_called_once_with(
            path="./test_file.py",
            format="html",
            apply_changes=False,
            dry_run=False,
            backup_dir=None,
            no_confirm=False,
        )
    
    def test_dev_review_with_apply_changes(self):
        """Test developer review command with apply changes option."""
        result = self.runner.invoke(app, ["dev", "review", "run", "./test_file.py", "--apply-changes"])
        
        # Check that the command executed successfully
        self.assertEqual(result.exit_code, 0)
        
        # Check that the review run function was called with apply_changes=True
        self.mock_review_run.assert_called_once_with(
            path="./test_file.py",
            format=None,
            apply_changes=True,
            dry_run=False,
            backup_dir=None,
            no_confirm=False,
        )
    
    @patch('vaahai.cli.commands.dev_review.command.logger')
    def test_dev_review_with_error(self, mock_logger):
        """Test developer review command when an error occurs."""
        # Make the review run function raise an exception
        self.mock_review_run.side_effect = Exception("Test error")
        
        # Run the command
        result = self.runner.invoke(app, ["dev", "review", "run", "./test_file.py"])
        
        # Check that the command failed
        self.assertEqual(result.exit_code, 1)
        
        # Check that the error was logged
        mock_logger.exception.assert_called_once()
        self.assertIn("Test error", mock_logger.exception.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
