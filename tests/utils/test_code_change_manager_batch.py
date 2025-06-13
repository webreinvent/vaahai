"""
Unit tests for the batch processing functionality of CodeChangeManager.

This module contains tests for the batch processing features of the
CodeChangeManager class, including pending changes and batch application.
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from vaahai.utils.code_change_manager import CodeChangeManager


class TestCodeChangeManagerBatch(unittest.TestCase):
    """Tests for the batch processing functionality of CodeChangeManager."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp(prefix="vaahai_test_")
        
        # Create test files with some content
        self.test_file_path = os.path.join(self.test_dir, "test_file.py")
        with open(self.test_file_path, "w") as f:
            f.write("def test_function():\n    # This is a test function\n    return 42\n")
        
        self.test_file_path2 = os.path.join(self.test_dir, "test_file2.py")
        with open(self.test_file_path2, "w") as f:
            f.write("def another_function():\n    # This is another function\n    return 100\n")
        
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
    
    def test_add_pending_change(self):
        """Test adding a change to the pending changes list."""
        # Add a pending change
        self.manager.add_pending_change(
            self.test_file_path, 1,
            "def test_function():\n    # This is a test function\n    return 42\n",
            "def test_function():\n    # This is a modified function\n    return 43\n"
        )
        
        # Check that the change was added to pending changes
        self.assertEqual(len(self.manager.pending_changes), 1)
        self.assertEqual(self.manager.pending_changes[0]["file_path"], self.test_file_path)
        self.assertEqual(self.manager.pending_changes[0]["line_number"], 1)
    
    def test_apply_pending_changes_single(self):
        """Test applying a single pending change."""
        # Add a pending change
        original_code = "def test_function():\n    # This is a test function\n    return 42\n"
        suggested_code = "def test_function():\n    # This is a modified function\n    return 43\n"
        
        self.manager.add_pending_change(
            self.test_file_path, 1, original_code, suggested_code
        )
        
        # Apply pending changes
        results = self.manager.apply_pending_changes()
        
        # Check the results
        self.assertEqual(results["total"], 1)
        self.assertEqual(results["applied"], 1)
        self.assertEqual(results["failed"], 0)
        
        # Check that the file was modified correctly
        with open(self.test_file_path, "r") as f:
            modified_content = f.read()
        self.assertEqual(modified_content, suggested_code)
        
        # Check that pending changes were cleared
        self.assertEqual(len(self.manager.pending_changes), 0)
        
        # Check that the change was moved to applied changes
        self.assertEqual(len(self.manager.changes_applied), 1)
    
    def test_apply_pending_changes_multiple(self):
        """Test applying multiple pending changes."""
        # Add pending changes to different files
        self.manager.add_pending_change(
            self.test_file_path, 1,
            "def test_function():\n    # This is a test function\n    return 42\n",
            "def test_function():\n    # This is a modified function\n    return 43\n"
        )
        
        self.manager.add_pending_change(
            self.test_file_path2, 1,
            "def another_function():\n    # This is another function\n    return 100\n",
            "def another_function():\n    # This is a modified function\n    return 101\n"
        )
        
        # Apply pending changes
        results = self.manager.apply_pending_changes()
        
        # Check the results
        self.assertEqual(results["total"], 2)
        self.assertEqual(results["applied"], 2)
        self.assertEqual(results["failed"], 0)
        
        # Check that both files were modified correctly
        with open(self.test_file_path, "r") as f:
            content1 = f.read()
        self.assertEqual(content1, "def test_function():\n    # This is a modified function\n    return 43\n")
        
        with open(self.test_file_path2, "r") as f:
            content2 = f.read()
        self.assertEqual(content2, "def another_function():\n    # This is a modified function\n    return 101\n")
        
        # Check that pending changes were cleared
        self.assertEqual(len(self.manager.pending_changes), 0)
        
        # Check that the changes were moved to applied changes
        self.assertEqual(len(self.manager.changes_applied), 2)
    
    def test_apply_pending_changes_with_failure(self):
        """Test applying pending changes with one failing."""
        # Add one valid change
        self.manager.add_pending_change(
            self.test_file_path, 1,
            "def test_function():\n    # This is a test function\n    return 42\n",
            "def test_function():\n    # This is a modified function\n    return 43\n"
        )
        
        # Add one invalid change (wrong original code)
        self.manager.add_pending_change(
            self.test_file_path2, 1,
            "def wrong_function():\n    return 99\n",  # This doesn't match the file content
            "def wrong_function():\n    return 100\n"
        )
        
        # Apply pending changes
        results = self.manager.apply_pending_changes()
        
        # Check the results
        self.assertEqual(results["total"], 2)
        self.assertEqual(results["applied"], 1)
        self.assertEqual(results["failed"], 1)
        
        # Check that only the first file was modified
        with open(self.test_file_path, "r") as f:
            content1 = f.read()
        self.assertEqual(content1, "def test_function():\n    # This is a modified function\n    return 43\n")
        
        with open(self.test_file_path2, "r") as f:
            content2 = f.read()
        self.assertEqual(content2, "def another_function():\n    # This is another function\n    return 100\n")
        
        # Check that pending changes were cleared
        self.assertEqual(len(self.manager.pending_changes), 0)
        
        # Check that only the successful change was moved to applied changes
        self.assertEqual(len(self.manager.changes_applied), 1)
    
    def test_get_summary_with_pending(self):
        """Test getting a summary with pending changes."""
        # Add a pending change
        self.manager.add_pending_change(
            self.test_file_path, 1,
            "def test_function():\n    # This is a test function\n    return 42\n",
            "def test_function():\n    # This is a modified function\n    return 43\n"
        )
        
        # Apply a change directly
        self.manager.apply_change(
            self.test_file_path2, 1,
            "def another_function():\n    # This is another function\n    return 100\n",
            "def another_function():\n    # This is a modified function\n    return 101\n"
        )
        
        # Reject a change
        self.manager.reject_change(self.test_file_path, 10)
        
        # Get the summary
        summary = self.manager.get_summary()
        
        # Check the summary content
        self.assertEqual(summary["applied"], 1)
        self.assertEqual(summary["rejected"], 1)
        self.assertEqual(summary["pending"], 1)
        self.assertEqual(len(summary["applied_changes"]), 1)
        self.assertEqual(len(summary["rejected_changes"]), 1)
        self.assertEqual(len(summary["pending_changes"]), 1)


if __name__ == "__main__":
    unittest.main()
