"""
Unit tests for the CodeChangeManager class.

This module contains tests for the code change management functionality,
including file backups and applying/rejecting suggested code changes.
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from vaahai.utils.code_change_manager import CodeChangeManager


class TestCodeChangeManager(unittest.TestCase):
    """Tests for the CodeChangeManager class."""
    
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
        
        self.manager = CodeChangeManager()
        self.manager.backup_dir = self.test_backup_dir
        
        # Enable test mode for non-interactive testing
        self.manager.set_test_mode(True, 'y')
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove the temporary directory and all its contents
        shutil.rmtree(self.test_dir)
    
    def test_backup_file(self):
        """Test creating a backup of a file."""
        # Backup the test file
        backup_path = self.manager.backup_file(self.test_file_path)
        
        # Check that the backup file exists
        self.assertTrue(os.path.exists(backup_path))
        
        # Check that the backup file has the same content as the original
        with open(self.test_file_path, "r") as f1, open(backup_path, "r") as f2:
            self.assertEqual(f1.read(), f2.read())
    
    def test_backup_file_nonexistent(self):
        """Test trying to backup a non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.manager.backup_file(os.path.join(self.test_dir, "nonexistent.py"))
    
    @patch("vaahai.utils.code_change_manager.datetime")
    def test_backup_file_path_format(self, mock_datetime):
        """Test the format of the backup file path."""
        # Mock the datetime to get a predictable backup filename
        mock_datetime.now.return_value.strftime.return_value = "20250613_123456"
        
        # Backup the test file
        backup_path = self.manager.backup_file(self.test_file_path)
        
        # Check the backup path format
        expected_path = os.path.join(
            self.test_backup_dir, 
            "test_file.py.20250613_123456.bak"
        )
        self.assertEqual(backup_path, expected_path)
    
    def test_apply_change_success(self):
        """Test successfully applying a code change."""
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
        
        # Check that the change was recorded
        self.assertEqual(len(self.manager.changes_applied), 1)
        self.assertEqual(self.manager.changes_applied[0]["file_path"], self.test_file_path)
        self.assertEqual(self.manager.changes_applied[0]["line_number"], 1)
    
    def test_apply_change_nonexistent_file(self):
        """Test applying a change to a non-existent file."""
        result = self.manager.apply_change(
            os.path.join(self.test_dir, "nonexistent.py"),
            1,
            "def test():\n    pass\n",
            "def test():\n    return True\n"
        )
        
        # The change should fail
        self.assertFalse(result)
        
        # No changes should be recorded
        self.assertEqual(len(self.manager.changes_applied), 0)
    
    def test_apply_change_content_mismatch(self):
        """Test applying a change when the original code doesn't match the file."""
        # Define a change with incorrect original code
        original_code = "def wrong_function():\n    return 99\n"
        suggested_code = "def wrong_function():\n    return 100\n"
        
        # Apply the change
        result = self.manager.apply_change(
            self.test_file_path, 1, original_code, suggested_code
        )
        
        # The change should fail due to content mismatch
        self.assertFalse(result)
        
        # No changes should be recorded
        self.assertEqual(len(self.manager.changes_applied), 0)
        
        # The file should remain unchanged
        with open(self.test_file_path, "r") as f:
            content = f.read()
        self.assertEqual(content, "def test_function():\n    # This is a test function\n    return 42\n")
    
    def test_reject_change(self):
        """Test rejecting a code change."""
        # Reject a change
        self.manager.reject_change(self.test_file_path, 1)
        
        # Check that the rejection was recorded
        self.assertEqual(len(self.manager.changes_rejected), 1)
        self.assertEqual(self.manager.changes_rejected[0]["file_path"], self.test_file_path)
        self.assertEqual(self.manager.changes_rejected[0]["line_number"], 1)
    
    def test_get_summary(self):
        """Test getting a summary of applied and rejected changes."""
        # Apply and reject some changes
        self.manager.apply_change(
            self.test_file_path, 1,
            "def test_function():\n    # This is a test function\n    return 42\n",
            "def test_function():\n    # This is a modified function\n    return 43\n"
        )
        self.manager.reject_change(self.test_file_path, 10)
        
        # Get the summary
        summary = self.manager.get_summary()
        
        # Check the summary content
        self.assertEqual(summary["applied"], 1)
        self.assertEqual(summary["rejected"], 1)
        self.assertEqual(len(summary["applied_changes"]), 1)
        self.assertEqual(len(summary["rejected_changes"]), 1)
        self.assertEqual(summary["applied_changes"][0]["file_path"], self.test_file_path)
        self.assertEqual(summary["rejected_changes"][0]["file_path"], self.test_file_path)


if __name__ == "__main__":
    unittest.main()
