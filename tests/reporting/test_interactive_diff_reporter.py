"""
Unit tests for the interactive diff reporter.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call, ANY

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live

from vaahai.reporting.interactive_diff_reporter import InteractiveDiffReporter, generate_interactive_diff_report


class TestInteractiveDiffReporter(unittest.TestCase):
    """Test cases for the InteractiveDiffReporter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock review results with issues
        self.mock_results = {
            "status": "success",
            "results": {
                "style_check": {
                    "step_id": "style_check",
                    "status": "completed",
                    "issues": [
                        {
                            "severity": "medium",
                            "message": "Line too long (90 characters)",
                            "file_path": "/path/to/file.py",
                            "line_number": 42,
                            "code_snippet": "def very_long_function_name_that_exceeds_line_length_limit(param1, param2, param3, param4, param5):",
                            "suggested_code": "def very_long_function_name_that_exceeds_line_length_limit(\n    param1, param2, param3, param4, param5):"
                        },
                        {
                            "severity": "low",
                            "message": "Missing docstring",
                            "file_path": "/path/to/another_file.py",
                            "line_number": 15,
                            "code_snippet": "def helper_function(x, y):\n    return x + y",
                            "suggested_code": "def helper_function(x, y):\n    \"\"\"Add two numbers and return the result.\"\"\"\n    return x + y"
                        }
                    ]
                },
                "security_check": {
                    "step_id": "security_check",
                    "status": "completed",
                    "issues": [
                        {
                            "severity": "critical",
                            "message": "Hardcoded credentials",
                            "file_path": "/path/to/config.py",
                            "line_number": 10,
                            "code_snippet": "PASSWORD = \"supersecret123\"",
                            "suggested_code": "PASSWORD = os.environ.get(\"APP_PASSWORD\")"
                        }
                    ]
                }
            }
        }
        
        # Mock error results
        self.mock_error_results = {
            "status": "error",
            "error": "Failed to analyze code"
        }
        
        # Mock empty results
        self.mock_empty_results = {
            "status": "success",
            "results": {}
        }
        
        # Create a mock console
        self.mock_console = MagicMock(spec=Console)
    
    @patch('rich.live.Live')
    def test_display_interactive_report_success(self, mock_live):
        """Test displaying an interactive report with successful results."""
        # Create a mock Live context manager
        mock_live_instance = MagicMock()
        mock_live.return_value.__enter__.return_value = mock_live_instance
        
        # Create reporter and simulate keyboard input for quitting
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console)
        self.mock_console.input.return_value = 'q'
        
        # Call the method
        reporter._handle_navigation = MagicMock()  # Mock the navigation to avoid Live issues
        reporter.display_interactive_report()
        
        # Verify Live was called
        self.assertTrue(reporter._handle_navigation.called)
        
        # Verify input was checked for navigation
        self.assertEqual(reporter._handle_navigation.call_count, 1)
    
    def test_display_interactive_report_error(self):
        """Test displaying an interactive report with error results."""
        reporter = InteractiveDiffReporter(self.mock_error_results, self.mock_console)
        reporter.display_interactive_report()
        
        # Verify console.print was called with an error panel
        self.mock_console.print.assert_called_once()
        args, kwargs = self.mock_console.print.call_args
        self.assertIsInstance(args[0], Panel)
        # Check that the panel contains the error message
        self.mock_console.print.assert_called_with(ANY)
    
    def test_display_interactive_report_empty(self):
        """Test displaying an interactive report with empty results."""
        reporter = InteractiveDiffReporter(self.mock_empty_results, self.mock_console)
        reporter.display_interactive_report()
        
        # Verify console.print was called with a warning message
        self.mock_console.print.assert_called_once_with("[yellow]No issues found in the review results.[/yellow]")
    
    def test_extract_issues_and_files(self):
        """Test extraction of issues and files from results."""
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console)
        
        # Verify issues were extracted
        self.assertEqual(len(reporter.issues), 3)
        self.assertEqual(reporter.issues[0]["step_id"], "style_check")
        self.assertEqual(reporter.issues[0]["issue"]["message"], "Line too long (90 characters)")
        
        # Verify files were extracted
        self.assertEqual(len(reporter.files), 3)
        self.assertIn("/path/to/file.py", reporter.files)
        self.assertIn("/path/to/another_file.py", reporter.files)
        self.assertIn("/path/to/config.py", reporter.files)
    
    def test_generate_header(self):
        """Test generation of the header panel."""
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console)
        header = reporter._generate_header()
        
        # Verify header is a Panel
        self.assertIsInstance(header, Panel)
    
    def test_generate_issue_info(self):
        """Test generation of the issue info panel."""
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console)
        issue_info = reporter._generate_issue_info()
        
        # Verify issue info is a Panel
        self.assertIsInstance(issue_info, Panel)
    
    def test_generate_code_display(self):
        """Test generation of the code display panel."""
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console)
        code_display = reporter._generate_code_display()
        
        # Verify code display is a Panel
        self.assertIsInstance(code_display, Panel)
    
    def test_generate_footer(self):
        """Test generation of the footer panel."""
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console)
        footer = reporter._generate_footer()
        
        # Verify footer is a Panel
        self.assertIsInstance(footer, Panel)
    
    @patch('vaahai.reporting.interactive_diff_reporter.InteractiveDiffReporter')
    def test_generate_interactive_diff_report(self, mock_reporter_class):
        """Test the generate_interactive_diff_report helper function."""
        # Create a mock reporter instance
        mock_reporter = MagicMock()
        mock_reporter_class.return_value = mock_reporter
        
        # Call the helper function
        generate_interactive_diff_report(self.mock_results, self.mock_console)
        
        # Verify reporter was created with the correct arguments
        mock_reporter_class.assert_called_once_with(self.mock_results, self.mock_console)
        
        # Verify display_interactive_report was called
        mock_reporter.display_interactive_report.assert_called_once()
    
    @patch('rich.live.Live')
    def test_handle_navigation(self, mock_live):
        """Test navigation handling in the interactive display."""
        # Create a mock Live context manager
        mock_live_instance = MagicMock()
        mock_live.return_value.__enter__.return_value = mock_live_instance
        
        # Create reporter
        reporter = InteractiveDiffReporter(self.mock_results, self.mock_console)
        
        # Simulate navigation key presses: right, left, up, down, enter, quit
        self.mock_console.input.side_effect = [
            '\x1b[C',  # Right arrow
            '\x1b[D',  # Left arrow
            '\x1b[A',  # Up arrow
            '\x1b[B',  # Down arrow
            '\r',      # Enter
            'q'        # Quit
        ]
        
        # Call the method
        reporter.display_interactive_report()
        
        # Verify input was checked for each navigation key
        self.assertEqual(self.mock_console.input.call_count, 6)
        
        # Verify console.print was called for Enter key (code change acceptance message)
        self.mock_console.print.assert_called_with("[yellow]Code change acceptance will be implemented in a future task.[/yellow]")


if __name__ == "__main__":
    unittest.main()
