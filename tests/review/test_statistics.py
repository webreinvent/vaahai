"""
Unit tests for the review statistics collector.
"""

import unittest
from unittest.mock import MagicMock, patch

from vaahai.review.steps.statistics import ReviewStatistics
from vaahai.review.steps.base import ReviewStepCategory, ReviewStepSeverity


class TestReviewStatistics(unittest.TestCase):
    """Test cases for the ReviewStatistics class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.statistics = ReviewStatistics()
    
    def test_init(self):
        """Test initialization of ReviewStatistics."""
        self.assertEqual(self.statistics.total_files, 0)
        self.assertEqual(self.statistics.files_with_issues, 0)
        self.assertEqual(self.statistics.total_issues, 0)
        self.assertEqual(self.statistics.issues_by_severity, {})
        self.assertEqual(self.statistics.issues_by_category, {})
        self.assertEqual(self.statistics.issues_by_step, {})
        self.assertEqual(self.statistics.unique_issues, set())
        self.assertEqual(self.statistics.file_statistics, {})
        self.assertEqual(self.statistics.step_statistics, {})
    
    def test_reset(self):
        """Test resetting statistics."""
        # Add some data
        self.statistics.total_files = 5
        self.statistics.files_with_issues = 3
        self.statistics.total_issues = 10
        self.statistics.issues_by_severity = {"critical": 2, "high": 3, "medium": 5}
        
        # Reset
        self.statistics.reset()
        
        # Verify reset
        self.assertEqual(self.statistics.total_files, 0)
        self.assertEqual(self.statistics.files_with_issues, 0)
        self.assertEqual(self.statistics.total_issues, 0)
        self.assertEqual(self.statistics.issues_by_severity, {})
    
    def test_add_file(self):
        """Test adding a file."""
        file_path = "/path/to/file.py"
        self.statistics.add_file(file_path)
        
        self.assertEqual(self.statistics.total_files, 1)
        self.assertIn(file_path, self.statistics.file_statistics)
        self.assertEqual(self.statistics.file_statistics[file_path]["issues"], 0)
    
    def test_add_issue(self):
        """Test adding an issue."""
        file_path = "/path/to/file.py"
        step_id = "test_step"
        step_category = "security"
        step_severity = "high"
        
        issue = {
            "line": 10,
            "column": 5,
            "message": "Test issue",
            "severity": "critical"
        }
        
        # Add file first
        self.statistics.add_file(file_path)
        
        # Add issue
        self.statistics.add_issue(step_id, step_category, step_severity, issue, file_path)
        
        # Verify issue was added
        self.assertEqual(self.statistics.total_issues, 1)
        self.assertEqual(self.statistics.files_with_issues, 1)
        self.assertEqual(self.statistics.issues_by_severity["critical"], 1)
        self.assertEqual(self.statistics.issues_by_category["security"], 1)
        self.assertEqual(self.statistics.issues_by_step["test_step"], 1)
        
        # Verify file statistics
        file_stats = self.statistics.file_statistics[file_path]
        self.assertEqual(file_stats["issues"], 1)
        self.assertEqual(file_stats["issues_by_severity"]["critical"], 1)
        self.assertEqual(file_stats["issues_by_category"]["security"], 1)
        self.assertEqual(file_stats["issues_by_step"]["test_step"], 1)
        
        # Verify step statistics
        step_stats = self.statistics.step_statistics[step_id]
        self.assertEqual(step_stats["issues"], 1)
        self.assertEqual(step_stats["category"], "security")
        self.assertEqual(step_stats["severity"], "high")
    
    def test_add_duplicate_issue(self):
        """Test adding a duplicate issue."""
        file_path = "/path/to/file.py"
        step_id = "test_step"
        step_category = "security"
        step_severity = "high"
        
        issue = {
            "line": 10,
            "column": 5,
            "message": "Test issue",
            "severity": "critical"
        }
        
        # Add file first
        self.statistics.add_file(file_path)
        
        # Add issue twice
        self.statistics.add_issue(step_id, step_category, step_severity, issue, file_path)
        self.statistics.add_issue(step_id, step_category, step_severity, issue, file_path)
        
        # Verify issue was added only once
        self.assertEqual(self.statistics.total_issues, 1)
    
    def test_add_step_result(self):
        """Test adding a step result."""
        file_path = "/path/to/file.py"
        step_id = "test_step"
        step_category = "security"
        step_severity = "high"
        
        step_result = {
            "status": "success",
            "issues": [
                {
                    "line": 10,
                    "column": 5,
                    "message": "Test issue 1",
                    "severity": "critical"
                },
                {
                    "line": 20,
                    "column": 15,
                    "message": "Test issue 2",
                    "severity": "medium"
                }
            ]
        }
        
        # Add file first
        self.statistics.add_file(file_path)
        
        # Add step result
        self.statistics.add_step_result(step_id, step_category, step_severity, step_result, file_path)
        
        # Verify issues were added
        self.assertEqual(self.statistics.total_issues, 2)
        self.assertEqual(self.statistics.files_with_issues, 1)
        self.assertEqual(self.statistics.issues_by_severity["critical"], 1)
        self.assertEqual(self.statistics.issues_by_severity["medium"], 1)
        self.assertEqual(self.statistics.issues_by_category["security"], 2)
        self.assertEqual(self.statistics.issues_by_step["test_step"], 2)
    
    def test_get_statistics_summary(self):
        """Test getting statistics summary."""
        # Add some data
        file_path1 = "/path/to/file1.py"
        file_path2 = "/path/to/file2.py"
        
        self.statistics.add_file(file_path1)
        self.statistics.add_file(file_path2)
        
        step_result1 = {
            "status": "success",
            "issues": [
                {
                    "line": 10,
                    "column": 5,
                    "message": "Critical issue",
                    "severity": "critical"
                }
            ]
        }
        
        step_result2 = {
            "status": "success",
            "issues": [
                {
                    "line": 20,
                    "column": 15,
                    "message": "High issue",
                    "severity": "high"
                },
                {
                    "line": 30,
                    "column": 25,
                    "message": "Medium issue",
                    "severity": "medium"
                }
            ]
        }
        
        self.statistics.add_step_result("step1", "security", "critical", step_result1, file_path1)
        self.statistics.add_step_result("step2", "style", "medium", step_result2, file_path2)
        
        # Get summary
        summary = self.statistics.get_statistics_summary()
        
        # Verify summary
        self.assertEqual(summary["total_files"], 2)
        self.assertEqual(summary["files_with_issues"], 2)
        self.assertEqual(summary["total_issues"], 3)
        self.assertEqual(summary["issues_per_file"], 1.5)
        self.assertEqual(summary["issues_by_severity"]["critical"], 1)
        self.assertEqual(summary["issues_by_severity"]["high"], 1)
        self.assertEqual(summary["issues_by_severity"]["medium"], 1)
        self.assertEqual(summary["issues_by_category"]["security"], 1)
        self.assertEqual(summary["issues_by_category"]["style"], 2)
        self.assertEqual(summary["issues_by_step"]["step1"], 1)
        self.assertEqual(summary["issues_by_step"]["step2"], 2)
    
    def test_get_file_statistics(self):
        """Test getting file statistics."""
        file_path = "/path/to/file.py"
        
        # Add file and issue
        self.statistics.add_file(file_path)
        self.statistics.add_issue(
            "test_step", "security", "high",
            {"line": 10, "column": 5, "message": "Test issue", "severity": "critical"},
            file_path
        )
        
        # Get file statistics
        file_stats = self.statistics.get_file_statistics(file_path)
        
        # Verify file statistics
        self.assertEqual(file_stats["issues"], 1)
        self.assertEqual(file_stats["issues_by_severity"]["critical"], 1)
        self.assertEqual(file_stats["issues_by_category"]["security"], 1)
        self.assertEqual(file_stats["issues_by_step"]["test_step"], 1)
    
    def test_get_step_statistics(self):
        """Test getting step statistics."""
        step_id = "test_step"
        
        # Add issue
        self.statistics.add_issue(
            step_id, "security", "high",
            {"line": 10, "column": 5, "message": "Test issue", "severity": "critical"},
            "/path/to/file.py"
        )
        
        # Get step statistics
        step_stats = self.statistics.get_step_statistics(step_id)
        
        # Verify step statistics
        self.assertEqual(step_stats["issues"], 1)
        self.assertEqual(step_stats["category"], "security")
        self.assertEqual(step_stats["severity"], "high")
    
    def test_get_key_findings(self):
        """Test getting key findings."""
        # Add some data with critical and high severity issues
        self.statistics.add_issue(
            "step1", "security", "critical",
            {"line": 10, "column": 5, "message": "Critical issue", "severity": "critical"},
            "/path/to/file1.py"
        )
        
        self.statistics.add_issue(
            "step2", "security", "high",
            {"line": 20, "column": 15, "message": "High issue", "severity": "high"},
            "/path/to/file2.py"
        )
        
        # Add duplicate messages to test common issues
        common_message = "Common issue"
        for i in range(3):
            self.statistics.add_issue(
                f"step{i+3}", "style", "medium",
                {"line": 30+i, "column": 25, "message": common_message, "severity": "medium"},
                f"/path/to/file{i+3}.py"
            )
        
        # Get key findings
        findings = self.statistics.get_key_findings(max_findings=3)
        
        # Verify findings
        self.assertEqual(len(findings), 3)
        
        # First finding should be critical issue
        self.assertEqual(findings[0]["type"], "severity")
        self.assertEqual(findings[0]["severity"], "critical")
        self.assertEqual(findings[0]["count"], 1)
        
        # Second finding should be high issue
        self.assertEqual(findings[1]["type"], "severity")
        self.assertEqual(findings[1]["severity"], "high")
        self.assertEqual(findings[1]["count"], 1)
        
        # Third finding should be common issue
        self.assertEqual(findings[2]["type"], "common_issue")
        self.assertEqual(findings[2]["message"], common_message)
        self.assertEqual(findings[2]["count"], 3)


if __name__ == "__main__":
    unittest.main()
