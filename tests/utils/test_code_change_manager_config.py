"""
Unit tests for the configuration and backup management functionality of CodeChangeManager.

This module contains tests for the configuration options and backup management features
of the CodeChangeManager class, including backup cleanup and history tracking.
"""

import os
import shutil
import tempfile
import unittest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from vaahai.utils.code_change_manager import CodeChangeManager


class TestCodeChangeManagerConfig(unittest.TestCase):
    """Tests for the configuration and backup management functionality of CodeChangeManager."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp(prefix="vaahai_test_")
        
        # Create a test file with some content
        self.test_file_path = os.path.join(self.test_dir, "test_file.py")
        with open(self.test_file_path, "w") as f:
            f.write("def test_function():\n    # This is a test function\n    return 42\n")
        
        # Create the code change manager with a test backup directory
        self.test_backup_dir = os.path.join(self.test_dir, "backups")
        os.makedirs(self.test_backup_dir, exist_ok=True)
        
        # Create a test config file
        self.config_path = os.path.join(self.test_dir, "test_config.ini")
        with open(self.config_path, "w") as f:
            f.write("[file_modification]\n")
            f.write(f"backup_dir = {self.test_backup_dir}\n")
            f.write("max_backup_age_days = 30\n")
            f.write("confirm_changes = true\n")
            f.write("dry_run = false\n")
        
        self.manager = CodeChangeManager(self.config_path)
        self.manager.backup_dir = self.test_backup_dir
        self.manager.backup_history_file = os.path.join(self.test_backup_dir, "backup_history.json")
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove the temporary directory and all its contents
        shutil.rmtree(self.test_dir)
    
    def test_init_with_custom_config(self):
        """Test initializing with custom configuration."""
        custom_backup_dir = os.path.join(self.test_dir, "custom_backups")
        
        # Create a custom config file
        custom_config_path = os.path.join(self.test_dir, "custom_config.ini")
        with open(custom_config_path, "w") as f:
            f.write("[file_modification]\n")
            f.write(f"backup_dir = {custom_backup_dir}\n")
            f.write("max_backup_age_days = 60\n")
            f.write("confirm_changes = false\n")
            f.write("dry_run = true\n")
        
        # Create a manager with custom configuration
        manager = CodeChangeManager(custom_config_path)
        
        # Check that the configuration was set correctly
        self.assertEqual(manager.config['backup_dir'], custom_backup_dir)
        self.assertEqual(manager.config['max_backup_age_days'], 60)
        self.assertFalse(manager.config['confirm_changes'])
        self.assertTrue(manager.config['dry_run'])
        
        # Check that the backup directory was created
        self.assertTrue(os.path.exists(custom_backup_dir))
    
    def test_apply_change_dry_run(self):
        """Test applying a change in dry run mode."""
        # Set dry run mode
        self.manager.config['dry_run'] = True
        
        # Define the change to apply
        original_code = "def test_function():\n    # This is a test function\n    return 42\n"
        suggested_code = "def test_function():\n    # This is a modified function\n    return 43\n"
        
        # Apply the change
        result = self.manager.apply_change(
            self.test_file_path, 1, original_code, suggested_code
        )
        
        # Check that the change was "applied" successfully in dry run mode
        self.assertTrue(result)
        
        # Check that the file was NOT modified
        with open(self.test_file_path, "r") as f:
            content = f.read()
        self.assertEqual(content, original_code)
        
        # Check that the change was recorded
        self.assertEqual(len(self.manager.changes_applied), 1)
        self.assertEqual(self.manager.changes_applied[0]["file_path"], self.test_file_path)
        self.assertEqual(self.manager.changes_applied[0]["line_number"], 1)
        self.assertTrue(self.manager.changes_applied[0]["dry_run"])
    
    def test_save_and_load_backup_history(self):
        """Test saving and loading backup history to/from a file."""
        # Create some backups
        backup_path1 = self.manager.backup_file(self.test_file_path)
        
        # Modify the file
        with open(self.test_file_path, "w") as f:
            f.write("def test_function():\n    # Modified\n    return 43\n")
        
        backup_path2 = self.manager.backup_file(self.test_file_path)
        
        # Check that the backup history file exists
        self.assertTrue(os.path.exists(self.manager.backup_history_file))
        
        # Load the backup history
        with open(self.manager.backup_history_file, "r") as f:
            history = json.load(f)
        
        # Check that the history contains the backups
        self.assertIn(self.test_file_path, history)
        self.assertEqual(len(history[self.test_file_path]), 2)
        self.assertEqual(history[self.test_file_path][0]['backup_path'], backup_path1)
        self.assertEqual(history[self.test_file_path][1]['backup_path'], backup_path2)
        
        # Create a new manager to test loading the history
        new_manager = CodeChangeManager()
        new_manager.backup_dir = self.test_backup_dir
        new_manager.backup_history_file = self.manager.backup_history_file
        
        # Force loading the backup history
        new_manager._load_backup_history()
        
        # Check that the history was loaded correctly
        self.assertEqual(len(new_manager.backup_history[self.test_file_path]), 2)
        self.assertEqual(new_manager.backup_history[self.test_file_path][0]['backup_path'], backup_path1)
        self.assertEqual(new_manager.backup_history[self.test_file_path][1]['backup_path'], backup_path2)
    
    @patch("vaahai.utils.code_change_manager.datetime")
    @patch("os.path.getmtime")
    def test_cleanup_old_backups(self, mock_getmtime, mock_datetime):
        """Test cleaning up old backups."""
        # Set the current date
        current_date = datetime(2025, 6, 13, 12, 0, 0)
        mock_datetime.now.return_value = current_date
        
        # Create backup files
        old_backup_path = os.path.join(self.test_backup_dir, "test_file.py.20250513_120000.bak")
        new_backup_path = os.path.join(self.test_backup_dir, "test_file.py.20250612_120000.bak")
        
        with open(old_backup_path, "w") as f:
            f.write("old backup")
        with open(new_backup_path, "w") as f:
            f.write("new backup")
        
        # Mock file modification times
        def mock_mtime(path):
            if path == old_backup_path:
                return (current_date - timedelta(days=31)).timestamp()
            else:
                return (current_date - timedelta(days=1)).timestamp()
        
        mock_getmtime.side_effect = mock_mtime
        
        # Set up backup history
        self.manager.backup_history = {
            self.test_file_path: [
                {
                    "backup_path": old_backup_path,
                    "timestamp": "20250513_120000"
                },
                {
                    "backup_path": new_backup_path,
                    "timestamp": "20250612_120000"
                }
            ]
        }
        
        # Save the backup history
        self.manager._save_backup_history()
        
        # Clean up old backups
        removed_count = self.manager.cleanup_old_backups(30)
        
        # Check that one backup was removed
        self.assertEqual(removed_count, 1)
        
        # Check that the old backup file was removed
        self.assertFalse(os.path.exists(old_backup_path))
        self.assertTrue(os.path.exists(new_backup_path))
    
    @patch("builtins.input")
    def test_apply_change_with_confirmation(self, mock_input):
        """Test applying a change with confirmation."""
        # Set confirmation required
        self.manager.config['confirm_changes'] = True
        
        # Mock the input function to return 'y'
        mock_input.return_value = 'y'
        
        # Define the change to apply
        original_code = "def test_function():\n    # This is a test function\n    return 42\n"
        suggested_code = "def test_function():\n    # This is a modified function\n    return 43\n"
        
        # Apply the change
        result = self.manager.apply_change(
            self.test_file_path, 1, original_code, suggested_code
        )
        
        # Check that the change was applied successfully
        self.assertTrue(result)
        
        # Check that the file was modified correctly
        with open(self.test_file_path, "r") as f:
            modified_content = f.read()
        self.assertEqual(modified_content, suggested_code)
    
    @patch("builtins.input")
    def test_apply_change_with_confirmation_rejected(self, mock_input):
        """Test applying a change with confirmation that is rejected."""
        # Set confirmation required
        self.manager.config['confirm_changes'] = True
        
        # Mock the input function to return 'n'
        mock_input.return_value = 'n'
        
        # Define the change to apply
        original_code = "def test_function():\n    # This is a test function\n    return 42\n"
        suggested_code = "def test_function():\n    # This is a modified function\n    return 43\n"
        
        # Apply the change
        result = self.manager.apply_change(
            self.test_file_path, 1, original_code, suggested_code
        )
        
        # Check that the change was not applied
        self.assertFalse(result)
        
        # Check that the file was not modified
        with open(self.test_file_path, "r") as f:
            content = f.read()
        self.assertEqual(content, original_code)
    
    def test_apply_change_without_confirmation(self):
        """Test applying a change when confirmation is disabled."""
        # Disable confirmation
        self.manager.config['confirm_changes'] = False
        
        # Define the change to apply
        original_code = "def test_function():\n    # This is a test function\n    return 42\n"
        suggested_code = "def test_function():\n    # This is a modified function\n    return 43\n"
        
        # Apply the change
        result = self.manager.apply_change(
            self.test_file_path, 1, original_code, suggested_code
        )
        
        # Check that the change was applied successfully
        self.assertTrue(result)
        
        # Check that the file was modified correctly
        with open(self.test_file_path, "r") as f:
            modified_content = f.read()
        self.assertEqual(modified_content, suggested_code)


if __name__ == "__main__":
    unittest.main()
