"""
Unit tests for the key findings reporter.
"""

import unittest
from unittest.mock import MagicMock, patch

from vaahai.review.steps.findings import KeyFindingsReporter
from vaahai.review.steps.statistics import ReviewStatistics
from vaahai.review.steps.base import ReviewStepCategory, ReviewStepSeverity


class TestKeyFindingsReporter(unittest.TestCase):
    """Test cases for the KeyFindingsReporter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.statistics = ReviewStatistics()
        self.reporter = KeyFindingsReporter(self.statistics)
    
    def test_init(self):
        """Test initialization of KeyFindingsReporter."""
        # Test with statistics
        reporter = KeyFindingsReporter(self.statistics)
        self.assertEqual(reporter.statistics, self.statistics)
        
        # Test without statistics
        reporter = KeyFindingsReporter()
        self.assertIsInstance(reporter.statistics, ReviewStatistics)
    
    def test_set_statistics(self):
        """Test setting statistics."""
        new_statistics = ReviewStatistics()
        self.reporter.set_statistics(new_statistics)
        self.assertEqual(self.reporter.statistics, new_statistics)
    
    def test_generate_findings_empty(self):
        """Test generating findings with empty statistics."""
        findings = self.reporter.generate_findings()
        self.assertEqual(findings, [])
    
    def test_generate_findings_with_critical_issues(self):
        """Test generating findings with critical issues."""
        # Add critical security issues
        self.statistics.add_issue(
            "security_step", "security", "critical",
            {"line": 10, "column": 5, "message": "Critical security issue", "severity": "critical"},
            "/path/to/file.py"
        )
        
        findings = self.reporter.generate_findings()
        
        # Should have at least 2 findings: one from severity and one from category
        self.assertGreaterEqual(len(findings), 2)
        
        # Check for severity finding
        severity_findings = [f for f in findings if f.get("type") == "severity" and f.get("severity") == "critical"]
        self.assertEqual(len(severity_findings), 1)
        self.assertEqual(severity_findings[0]["count"], 1)
        
        # Check for category finding
        category_findings = [f for f in findings if f.get("type") == "category" and f.get("category") == "security"]
        self.assertEqual(len(category_findings), 1)
        self.assertEqual(category_findings[0]["count"], 1)
    
    def test_generate_findings_with_performance_issues(self):
        """Test generating findings with performance issues."""
        # Add performance issues
        self.statistics.add_issue(
            "performance_step", "performance", "medium",
            {"line": 10, "column": 5, "message": "Performance issue", "severity": "medium"},
            "/path/to/file.py"
        )
        
        findings = self.reporter.generate_findings()
        
        # Check for category finding
        category_findings = [f for f in findings if f.get("type") == "category" and f.get("category") == "performance"]
        self.assertEqual(len(category_findings), 1)
        self.assertEqual(category_findings[0]["count"], 1)
    
    def test_generate_findings_with_maintainability_issues(self):
        """Test generating findings with maintainability issues."""
        # Add style issues
        self.statistics.add_issue(
            "style_step", "style", "low",
            {"line": 10, "column": 5, "message": "Style issue", "severity": "low"},
            "/path/to/file.py"
        )
        
        findings = self.reporter.generate_findings()
        
        # Check for category finding
        category_findings = [f for f in findings if f.get("type") == "category" and f.get("category") == "maintainability"]
        self.assertEqual(len(category_findings), 1)
        self.assertEqual(category_findings[0]["count"], 1)
    
    def test_generate_findings_with_common_issues(self):
        """Test generating findings with common issues."""
        # Add multiple instances of the same issue
        common_message = "Common issue"
        for i in range(3):
            self.statistics.add_issue(
                f"step{i}", "style", "medium",
                {"line": 10+i, "column": 5, "message": common_message, "severity": "medium"},
                f"/path/to/file{i}.py"
            )
        
        findings = self.reporter.generate_findings()
        
        # Check for common issue finding
        common_findings = [f for f in findings if f.get("type") == "common_issue" and f.get("message") == common_message]
        self.assertEqual(len(common_findings), 1)
        self.assertEqual(common_findings[0]["count"], 3)
    
    def test_generate_findings_max_limit(self):
        """Test limiting the number of findings."""
        # Add various issues
        for i in range(20):
            self.statistics.add_issue(
                f"step{i}", "style", "medium",
                {"line": 10+i, "column": 5, "message": f"Issue {i}", "severity": "medium"},
                f"/path/to/file{i}.py"
            )
        
        # Set max_findings to 5
        findings = self.reporter.generate_findings(max_findings=5)
        
        # Should have exactly 5 findings
        self.assertEqual(len(findings), 5)
    
    def test_sort_findings_by_priority(self):
        """Test sorting findings by priority."""
        # Create findings with different priorities
        self.reporter.findings = [
            {"type": "category", "category": "best_practice", "count": 5, "priority": 4},
            {"type": "severity", "severity": "critical", "count": 1, "priority": 1},
            {"type": "category", "category": "performance", "count": 3, "priority": 2},
            {"type": "common_issue", "message": "Common issue", "count": 4, "priority": 3},
        ]
        
        # Sort findings
        self.reporter._sort_findings_by_priority()
        
        # Check order
        self.assertEqual(self.reporter.findings[0]["priority"], 1)
        self.assertEqual(self.reporter.findings[1]["priority"], 2)
        self.assertEqual(self.reporter.findings[2]["priority"], 3)
        self.assertEqual(self.reporter.findings[3]["priority"], 4)
    
    def test_get_actionable_recommendations(self):
        """Test getting actionable recommendations."""
        # Add various issues
        self.statistics.add_issue(
            "security_step", "security", "critical",
            {"line": 10, "column": 5, "message": "Critical security issue", "severity": "critical"},
            "/path/to/file1.py"
        )
        
        self.statistics.add_issue(
            "performance_step", "performance", "high",
            {"line": 20, "column": 5, "message": "Performance issue", "severity": "high"},
            "/path/to/file2.py"
        )
        
        # Add common issue
        common_message = "Common style issue"
        for i in range(3):
            self.statistics.add_issue(
                f"style_step{i}", "style", "medium",
                {"line": 30+i, "column": 5, "message": common_message, "severity": "medium"},
                f"/path/to/file{i+3}.py"
            )
        
        # Generate findings first
        self.reporter.generate_findings()
        
        # Get recommendations
        recommendations = self.reporter.get_actionable_recommendations()
        
        # Should have recommendations
        self.assertGreater(len(recommendations), 0)
        
        # Check for critical issue recommendation
        critical_recs = [r for r in recommendations if "critical" in r.lower()]
        self.assertEqual(len(critical_recs), 1)
        
        # Check for security recommendation
        security_recs = [r for r in recommendations if "security" in r.lower()]
        self.assertEqual(len(security_recs), 1)
        
        # Check for common issue recommendation
        common_recs = [r for r in recommendations if "recurring issue" in r.lower()]
        self.assertEqual(len(common_recs), 1)


if __name__ == "__main__":
    unittest.main()
