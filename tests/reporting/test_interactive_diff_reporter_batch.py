"""
Unit tests for the batch processing and undo functionality of InteractiveDiffReporter.

This module contains tests for the batch mode, undo, and apply pending changes features
of the InteractiveDiffReporter class.
"""

import unittest
from unittest.mock import patch, MagicMock, call, ANY

from rich.console import Console
from rich.panel import Panel
from rich.live import Live

from vaahai.reporting.interactive_diff_reporter import InteractiveDiffReporter, generate_interactive_diff_report
from vaahai.utils.code_change_manager import CodeChangeManager


class TestInteractiveDiffReporterBatch(unittest.TestCase):
    """Test cases for the batch processing and undo functionality of InteractiveDiffReporter."""
    
    def setUp(self):
        """Set up test environment."""
        # Create mock console
        self.mock_console = MagicMock(spec=Console)
        
        # Create mock code change manager
        self.mock_manager = MagicMock(spec=CodeChangeManager)
        self.mock_manager.set_test_mode = MagicMock()
        
        # Set up necessary attributes on the mock manager
        self.mock_manager.config = {'confirm_changes': False}  # Disable confirmation for tests
        self.mock_manager.pending_changes = [{'file_path': '/path/to/file1.py', 'line_number': 42}]
        
        # Set up default return value for get_summary to avoid comparison issues
        self.mock_manager.get_summary.return_value = {
            "applied": 0,
            "rejected": 0,
            "pending": 0,
            "applied_changes": [],
            "rejected_changes": [],
            "pending_changes": []
        }
        
        # Create mock results with multiple issues
        self.mock_results = {
            "status": "success",
            "results": [
                {
                    "step_id": "style_check",
                    "issues": [
                        {
                            "severity": "medium",
                            "file_path": "/path/to/file1.py",
                            "line_number": 42,
                            "message": "Line too long (90 characters)",
                            "code_snippet": "def very_long_function_name_that_exceeds_line_length_limit(param1, param2, param3, param4, param5):",
                            "suggested_code": "def very_long_function_name_that_exceeds_line_length_limit(\n    param1, param2, param3, param4, param5):"
                        },
                        {
                            "severity": "low",
                            "file_path": "/path/to/file2.py",
                            "line_number": 10,
                            "message": "Missing docstring",
                            "code_snippet": "def test_function():\n    return True",
                            "suggested_code": "def test_function():\n    \"\"\"Test function.\"\"\"\n    return True"
                        }
                    ]
                }
            ]
        }
    
    @patch('rich.live.Live')
    def test_batch_mode_toggle(self, mock_live):
        """Test toggling batch mode."""
        # Create a mock Live context manager
        mock_live_instance = MagicMock()
        mock_live.return_value.__enter__.return_value = mock_live_instance
        
        # Create reporter with code change manager
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console, self.mock_manager)
        
        # Mock the input method to simulate keyboard input: 'b' (toggle batch), 'q' (quit)
        self.mock_console.input.side_effect = ['b', 'q']
        
        # Call the method
        reporter._handle_navigation(mock_live_instance)
        
        # Verify batch mode was toggled
        self.assertTrue(reporter.batch_mode)
        
        # Verify console.print was called with batch mode status
        self.mock_console.print.assert_any_call("[yellow]Batch mode enabled[/yellow]")
        
        # Verify layout was updated
        mock_live_instance.update.assert_called()
    
    @patch('rich.live.Live')
    def test_accept_change_in_batch_mode(self, mock_live):
        """Test accepting a change in batch mode."""
        # Create a mock Live context manager
        mock_live_instance = MagicMock()
        mock_live.return_value.__enter__.return_value = mock_live_instance
        
        # Create reporter with code change manager
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console, self.mock_manager)
        
        # Enable batch mode
        reporter.batch_mode = True
        
        # Enable test mode on the code change manager
        self.mock_manager.set_test_mode.assert_called_once_with(True, 'y')
        
        # Mock the input method to simulate keyboard input: 'a' (accept), 'q' (quit)
        self.mock_console.input.side_effect = ['a', 'q']
        
        # Call the method
        reporter._handle_navigation(mock_live_instance)
        
        # Verify add_pending_change was called on the manager
        self.mock_manager.add_pending_change.assert_called_once()
        
        # Verify apply_change was NOT called (since we're in batch mode)
        self.mock_manager.apply_change.assert_not_called()
        
        # Verify console.print was called with the expected message
        self.mock_console.print.assert_any_call("[green]Change added to batch for /path/to/file1.py[/green]")
        
        # Verify the issue status was updated to 'accepted'
        # The issue_id is constructed as f"{step_id}:{file_path}:{line_number}"
        expected_issue_id = "style_check:/path/to/file1.py:42"
        self.assertEqual(reporter.issue_statuses[expected_issue_id], "accepted")
        
        # Verify layout was updated
        mock_live_instance.update.assert_called()
    
    @patch('rich.live.Live')
    def test_accept_change_not_in_batch_mode(self, mock_live):
        """Test accepting a change when not in batch mode."""
        # Create a mock Live context manager
        mock_live_instance = MagicMock()
        mock_live.return_value.__enter__.return_value = mock_live_instance
        
        # Create reporter with code change manager
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console, self.mock_manager)
        
        # Ensure batch mode is disabled
        reporter.batch_mode = False
        
        # Mock the input method to simulate keyboard input: 'a' (accept), 'q' (quit)
        self.mock_console.input.side_effect = ['a', 'q']
        
        # Set up manager.apply_change to return True
        self.mock_manager.apply_change.return_value = True
        
        # Call the method
        reporter._handle_navigation(mock_live_instance)
        
        # Verify apply_change was called on the manager
        self.mock_manager.apply_change.assert_called_once()
        
        # Verify add_pending_change was NOT called
        self.mock_manager.add_pending_change.assert_not_called()
        
        # Verify console.print was called with the expected message
        self.mock_console.print.assert_any_call("[green]Change applied to /path/to/file1.py[/green]")
        
        # Verify the issue status was updated to 'accepted'
        # The issue_id is constructed as f"{step_id}:{file_path}:{line_number}"
        expected_issue_id = "style_check:/path/to/file1.py:42"
        self.assertEqual(reporter.issue_statuses[expected_issue_id], "accepted")
        
        # Verify layout was updated
        mock_live_instance.update.assert_called()
    
    @patch('rich.live.Live')
    def test_apply_pending_changes(self, mock_live):
        """Test applying pending changes."""
        # Create a mock Live context manager
        mock_live_instance = MagicMock()
        mock_live.return_value.__enter__.return_value = mock_live_instance
        
        # Create reporter with code change manager
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console, self.mock_manager)
        
        # Enable batch mode and add some pending changes
        reporter.batch_mode = True
        
        # Mock the input method to simulate keyboard input: 'p' (apply pending), 'q' (quit)
        self.mock_console.input.side_effect = ['p', 'q']
        
        # Set up manager.apply_pending_changes to return a result
        self.mock_manager.apply_pending_changes.return_value = {
            "applied": 2,
            "failed": 0,
            "details": []
        }
        
        # Call the method
        reporter._handle_navigation(mock_live_instance)
        
        # Verify apply_pending_changes was called on the manager
        self.mock_manager.apply_pending_changes.assert_called_once()
        
        # Verify console.print was called with the results - match the exact message from the implementation
        self.mock_console.print.assert_any_call("[green]Applied 2 changes[/green]")
        
        # Verify layout was updated
        mock_live_instance.update.assert_called()
    
    @patch('rich.live.Live')
    def test_undo_last_change(self, mock_live):
        """Test undoing the last change."""
        # Create a mock Live context manager
        mock_live_instance = MagicMock()
        mock_live.return_value.__enter__.return_value = mock_live_instance
        
        # Create reporter with code change manager
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console, self.mock_manager)
        
        # Mock the input method to simulate keyboard input: 'u' (undo), 'q' (quit)
        self.mock_console.input.side_effect = ['u', 'q']
        
        # Set up manager.undo_last_change to return True
        self.mock_manager.undo_last_change.return_value = True
        
        # Call the method
        reporter._handle_navigation(mock_live_instance)
        
        # Verify undo_last_change was called on the manager
        self.mock_manager.undo_last_change.assert_called_once()
        
        # Verify console.print was called with success message
        self.mock_console.print.assert_any_call("[green]Successfully undid last change[/green]")
        
        # Verify layout was updated
        mock_live_instance.update.assert_called()
    
    @patch('rich.live.Live')
    def test_undo_last_change_failure(self, mock_live):
        """Test undoing the last change when it fails."""
        # Create a mock Live context manager
        mock_live_instance = MagicMock()
        mock_live.return_value.__enter__.return_value = mock_live_instance
        
        # Create reporter with code change manager
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console, self.mock_manager)
        
        # Mock the input method to simulate keyboard input: 'u' (undo), 'q' (quit)
        self.mock_console.input.side_effect = ['u', 'q']
        
        # Set up manager.undo_last_change to return False
        self.mock_manager.undo_last_change.return_value = False
        
        # Call the method
        reporter._handle_navigation(mock_live_instance)
        
        # Verify undo_last_change was called on the manager
        self.mock_manager.undo_last_change.assert_called_once()
        
        # Verify console.print was called with error message
        self.mock_console.print.assert_any_call("[yellow]No changes to undo or undo failed[/yellow]")
        
        # Verify layout was updated
        mock_live_instance.update.assert_called()
    
    def test_show_changes_summary_with_pending(self):
        """Test showing changes summary with pending changes."""
        # Create reporter with code change manager
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console, self.mock_manager)
        
        # Set up manager.get_summary to return a summary with pending changes
        self.mock_manager.get_summary.return_value = {
            "applied": 2,
            "rejected": 1,
            "pending": 3,
            "applied_changes": [{"file_path": "/path/to/file1.py"}, {"file_path": "/path/to/file2.py"}],
            "rejected_changes": [{"file_path": "/path/to/file3.py"}],
            "pending_changes": [
                {"file_path": "/path/to/file4.py"},
                {"file_path": "/path/to/file5.py"},
                {"file_path": "/path/to/file6.py"}
            ]
        }
        
        # Call the method
        reporter._show_changes_summary()
        
        # Verify get_summary was called on the manager
        self.mock_manager.get_summary.assert_called_once()
        
        # Verify console.print was called with the expected number of times
        # The actual implementation makes multiple print calls for headers and each change
        # 1 for the header, 1 for applied count, 1 for rejected count, 1 for pending count, 1 for pending note
        # 1 for applied header, 2 for applied changes (one for each file)
        # 1 for rejected header, 1 for rejected change
        # 1 for pending header, 3 for pending changes (one for each file)
        # Total: 14 calls
        self.assertEqual(self.mock_console.print.call_count, 14)
        
        # Verify specific messages were printed
        self.mock_console.print.assert_any_call("\n[bold blue]Changes Summary[/bold blue]")
        self.mock_console.print.assert_any_call("[green]Applied changes:[/green] 2")
        self.mock_console.print.assert_any_call("[yellow]Rejected changes:[/yellow] 1")
        self.mock_console.print.assert_any_call("[blue]Pending changes:[/blue] 3")
    
    @patch('vaahai.reporting.interactive_diff_reporter.InteractiveDiffReporter')
    def test_generate_interactive_diff_report_with_manager(self, mock_reporter_class):
        """Test the generate_interactive_diff_report helper function with a CodeChangeManager."""
        # Create a mock reporter instance
        mock_reporter = MagicMock()
        mock_reporter_class.return_value = mock_reporter
        
        # Create a mock code change manager
        mock_manager = MagicMock(spec=CodeChangeManager)
        
        # Call the helper function with the manager
        generate_interactive_diff_report(self.mock_results, self.mock_console, mock_manager)
        
        # Verify reporter was created with the correct arguments including the manager
        mock_reporter_class.assert_called_once_with(self.mock_results, self.mock_console, mock_manager)
        
        # Verify display_interactive_report was called
        mock_reporter.display_interactive_report.assert_called_once()


if __name__ == "__main__":
    unittest.main()
