"""
Unit tests for the undo and revert functionality of CodeChangeManager.

This module contains tests for the undo and revert features of the
CodeChangeManager class, including backup history and restoration.
"""

import os
import shutil
import tempfile
import unittest
import json
from unittest.mock import patch

from vaahai.utils.code_change_manager import CodeChangeManager


class TestCodeChangeManagerUndo(unittest.TestCase):
    """Tests for the undo and revert functionality of CodeChangeManager."""
    
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
        self.manager.backup_history_file = os.path.join(self.test_backup_dir, "backup_history.json")
        
        # Enable test mode for non-interactive testing
        self.manager.set_test_mode(True, 'y')
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove the temporary directory and all its contents
        shutil.rmtree(self.test_dir)
    
    def test_undo_last_change(self):
        """Test undoing the last applied change."""
        # Apply a change
        original_code = "def test_function():\n    # This is a test function\n    return 42\n"
        suggested_code = "def test_function():\n    # This is a modified function\n    return 43\n"
        
        self.manager.apply_change(
            self.test_file_path, 1, original_code, suggested_code
        )
        
        # Check that the file was modified
        with open(self.test_file_path, "r") as f:
            modified_content = f.read()
        self.assertEqual(modified_content, suggested_code)
        
        # Undo the change
        result = self.manager.undo_last_change()
        
        # Check that the undo was successful
        self.assertTrue(result)
        
        # Check that the file was restored to its original content
        with open(self.test_file_path, "r") as f:
            restored_content = f.read()
        self.assertEqual(restored_content, original_code)
        
        # Check that the change was removed from applied changes
        self.assertEqual(len(self.manager.changes_applied), 0)
    
    def test_undo_last_change_no_changes(self):
        """Test undoing when there are no changes to undo."""
        # Try to undo with no changes applied
        result = self.manager.undo_last_change()
        
        # Check that the undo failed
        self.assertFalse(result)
    
    def test_undo_last_change_missing_backup(self):
        """Test undoing when the backup file is missing."""
        # Apply a change
        original_code = "def test_function():\n    # This is a test function\n    return 42\n"
        suggested_code = "def test_function():\n    # This is a modified function\n    return 43\n"
        
        self.manager.apply_change(
            self.test_file_path, 1, original_code, suggested_code
        )
        
        # Delete the backup file
        backup_path = self.manager.changes_applied[0]["backup_path"]
        os.remove(backup_path)
        
        # Try to undo the change
        result = self.manager.undo_last_change()
        
        # Check that the undo failed
        self.assertFalse(result)
        
        # Check that the file still has the modified content
        with open(self.test_file_path, "r") as f:
            content = f.read()
        self.assertEqual(content, suggested_code)
    
    def test_get_latest_backup(self):
        """Test getting the latest backup of a file."""
        # Create multiple backups
        backup1 = self.manager.backup_file(self.test_file_path)
        
        # Modify the file
        with open(self.test_file_path, "w") as f:
            f.write("def test_function():\n    # Modified\n    return 43\n")
        
        backup2 = self.manager.backup_file(self.test_file_path)
        
        # Get the latest backup
        latest_backup = self.manager.get_latest_backup(self.test_file_path)
        
        # Check that the latest backup is the second one
        self.assertEqual(latest_backup, backup2)
    
    def test_get_latest_backup_no_backups(self):
        """Test getting the latest backup when there are no backups."""
        # Get the latest backup for a file with no backups
        latest_backup = self.manager.get_latest_backup(self.test_file_path)
        
        # Check that no backup was found
        self.assertIsNone(latest_backup)
    
    def test_restore_from_backup(self):
        """Test restoring a file from backup."""
        # Create a backup
        backup_path = self.manager.backup_file(self.test_file_path)
        
        # Modify the file
        modified_content = "def test_function():\n    # Modified\n    return 43\n"
        with open(self.test_file_path, "w") as f:
            f.write(modified_content)
        
        # Check that the file was modified
        with open(self.test_file_path, "r") as f:
            content = f.read()
        self.assertEqual(content, modified_content)
        
        # Restore from the backup
        result = self.manager.restore_from_backup(self.test_file_path, backup_path)
        
        # Check that the restore was successful
        self.assertTrue(result)
        
        # Check that the file was restored to its original content
        with open(self.test_file_path, "r") as f:
            restored_content = f.read()
        self.assertEqual(restored_content, "def test_function():\n    # This is a test function\n    return 42\n")
    
    def test_restore_from_backup_latest(self):
        """Test restoring a file from the latest backup."""
        # Create a backup
        self.manager.backup_file(self.test_file_path)
        
        # Modify the file
        modified_content = "def test_function():\n    # Modified\n    return 43\n"
        with open(self.test_file_path, "w") as f:
            f.write(modified_content)
        
        # Restore from the latest backup without specifying a backup path
        result = self.manager.restore_from_backup(self.test_file_path)
        
        # Check that the restore was successful
        self.assertTrue(result)
        
        # Check that the file was restored to its original content
        with open(self.test_file_path, "r") as f:
            restored_content = f.read()
        self.assertEqual(restored_content, "def test_function():\n    # This is a test function\n    return 42\n")
    
    def test_restore_from_backup_nonexistent(self):
        """Test restoring from a non-existent backup."""
        # Try to restore from a non-existent backup
        result = self.manager.restore_from_backup(
            self.test_file_path,
            os.path.join(self.test_backup_dir, "nonexistent.bak")
        )
        
        # Check that the restore failed
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
