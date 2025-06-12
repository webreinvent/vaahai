"""
Example script to demonstrate the key findings reporter.

This script creates a sample codebase with various issues and runs
the review steps to generate key findings and recommendations.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vaahai.review.steps.registry import ReviewStepRegistry
from vaahai.review.runner import ReviewRunner
from vaahai.review.steps.findings import KeyFindingsReporter
from vaahai.review.steps.statistics import ReviewStatistics
from rich.console import Console


def create_sample_files(temp_dir):
    """Create sample files with various issues for demonstration."""
    
    # File with security issues
    security_file = os.path.join(temp_dir, "security_issues.py")
    with open(security_file, "w") as f:
        f.write("""
import sqlite3
import os

def unsafe_query(user_input):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    # SQL Injection vulnerability
    cursor.execute(f"SELECT * FROM users WHERE username = '{user_input}'")
    return cursor.fetchall()

def unsafe_command(user_input):
    # Command injection vulnerability
    os.system(f"ls {user_input}")
    
def unsafe_eval(user_input):
    # Unsafe eval
    result = eval(user_input)
    return result
""")
    
    # File with performance issues
    performance_file = os.path.join(temp_dir, "performance_issues.py")
    with open(performance_file, "w") as f:
        f.write("""
def inefficient_loop():
    # Inefficient list modification during iteration
    my_list = [1, 2, 3, 4, 5]
    for i in range(len(my_list)):
        if my_list[i] % 2 == 0:
            my_list.pop(i)  # This will cause issues
    
    # Nested loop with same iterable
    result = []
    for i in range(1000):
        for j in range(1000):
            result.append(i * j)
    
    # Large memory usage
    large_list = [i for i in range(10000000)]
    
    return large_list
""")
    
    # File with style issues
    style_file = os.path.join(temp_dir, "style_issues.py")
    with open(style_file, "w") as f:
        f.write("""
# Too many global variables
var1 = "global1"
var2 = "global2"
var3 = "global3"
var4 = "global4"
var5 = "global5"

def poorly_named_function(x, y, z):
    # Too many local variables
    a = x + 1
    b = y + 2
    c = z + 3
    d = a + b
    e = b + c
    f = c + d
    g = d + e
    h = e + f
    
    # Long function
    result = 0
    for i in range(100):
        result += i
    
    for j in range(100):
        result -= j
    
    for k in range(100):
        result *= k if k != 0 else 1
    
    return result

# Duplicate code
def duplicate_function1():
    print("This is duplicate code")
    print("It appears in multiple places")
    print("And should be refactored")
    
def duplicate_function2():
    print("This is duplicate code")
    print("It appears in multiple places")
    print("And should be refactored")
""")
    
    return [security_file, performance_file, style_file]


def main():
    """Run the example script."""
    console = Console()
    
    # Create a temporary directory for sample files
    with tempfile.TemporaryDirectory() as temp_dir:
        console.print(f"[bold]Created temporary directory:[/bold] {temp_dir}")
        
        # Create sample files
        sample_files = create_sample_files(temp_dir)
        console.print(f"[bold]Created sample files:[/bold] {len(sample_files)}")
        
        # For demonstration purposes, manually create statistics and findings
        console.print("\n[bold]Creating sample review statistics...[/bold]")
        statistics = ReviewStatistics()
        
        # Add files
        for file_path in sample_files:
            statistics.add_file(file_path)
        
        # Add security issues
        statistics.add_issue(
            "sql_injection", "security", "critical",
            {"line": 10, "column": 5, "message": "SQL Injection vulnerability detected", "severity": "critical"},
            sample_files[0]
        )
        
        statistics.add_issue(
            "command_injection", "security", "critical",
            {"line": 15, "column": 5, "message": "Command Injection vulnerability detected", "severity": "critical"},
            sample_files[0]
        )
        
        statistics.add_issue(
            "unsafe_eval", "security", "high",
            {"line": 20, "column": 5, "message": "Unsafe eval() usage detected", "severity": "high"},
            sample_files[0]
        )
        
        # Add performance issues
        statistics.add_issue(
            "inefficient_loop", "performance", "medium",
            {"line": 5, "column": 5, "message": "Inefficient list modification during iteration", "severity": "medium"},
            sample_files[1]
        )
        
        statistics.add_issue(
            "nested_loop", "performance", "high",
            {"line": 10, "column": 5, "message": "Nested loop with high complexity (O(n²))", "severity": "high"},
            sample_files[1]
        )
        
        statistics.add_issue(
            "large_memory", "performance", "medium",
            {"line": 15, "column": 5, "message": "Large memory allocation detected", "severity": "medium"},
            sample_files[1]
        )
        
        # Add style issues
        for i in range(5):
            statistics.add_issue(
                "too_many_globals", "style", "low",
                {"line": i+2, "column": 1, "message": "Too many global variables", "severity": "low"},
                sample_files[2]
            )
        
        statistics.add_issue(
            "too_many_locals", "style", "low",
            {"line": 10, "column": 5, "message": "Too many local variables", "severity": "low"},
            sample_files[2]
        )
        
        # Add duplicate code issues (same message multiple times)
        for i in range(3):
            statistics.add_issue(
                "duplicate_code", "maintainability", "medium",
                {"line": 30+i, "column": 5, "message": "Duplicate code detected", "severity": "medium"},
                sample_files[2]
            )
        
        # Create findings reporter and generate findings
        findings_reporter = KeyFindingsReporter(statistics)
        key_findings = findings_reporter.generate_findings()
        recommendations = findings_reporter.get_actionable_recommendations()
        
        # Display statistics summary
        statistics_summary = statistics.get_statistics_summary()
        if statistics_summary:
            console.print("\n[bold]Review Statistics Summary:[/bold]")
            console.print(f"Files reviewed: {statistics_summary.get('total_files', 0)}")
            console.print(f"Files with issues: {statistics_summary.get('files_with_issues', 0)}")
            console.print(f"Total issues: {statistics_summary.get('total_issues', 0)}")
            console.print(f"Average issues per file: {statistics_summary.get('issues_per_file', 0):.2f}")
            
            # Issues by severity
            issues_by_severity = statistics_summary.get("issues_by_severity", {})
            if issues_by_severity:
                console.print("\n[bold]Issues by Severity:[/bold]")
                for severity, count in issues_by_severity.items():
                    severity_style = {
                        "critical": "bold red",
                        "high": "red",
                        "medium": "yellow",
                        "low": "green",
                        "info": "blue",
                    }.get(severity.lower(), "white")
                    console.print(f"[{severity_style}]{severity.upper()}[/{severity_style}]: {count}")
            
            # Issues by category
            issues_by_category = statistics_summary.get("issues_by_category", {})
            if issues_by_category:
                console.print("\n[bold]Issues by Category:[/bold]")
                for category, count in sorted(issues_by_category.items(), key=lambda x: x[1], reverse=True):
                    console.print(f"{category.upper()}: {count}")
        
        # Display key findings
        if key_findings:
            console.print("\n[bold yellow]Key Findings:[/bold yellow]")
            for finding in key_findings:
                finding_type = finding.get("type", "")
                count = finding.get("count", 0)
                message = finding.get("message", "")
                
                if finding_type == "severity":
                    severity = finding.get("severity", "").lower()
                    severity_style = {
                        "critical": "bold red",
                        "high": "red",
                        "medium": "yellow",
                        "low": "green",
                        "info": "blue",
                    }.get(severity, "white")
                    console.print(f"[{severity_style}]{severity.upper()}[/{severity_style}]: {message}")
                elif finding_type == "category":
                    category = finding.get("category", "").upper()
                    console.print(f"[bold cyan]{category}[/bold cyan]: {message}")
                elif finding_type == "common_issue":
                    console.print(f"COMMON ISSUE: {message} (found {count} times)")
        
        # Display recommendations
        if recommendations:
            console.print("\n[bold green]Recommendations:[/bold green]")
            for i, rec in enumerate(recommendations, 1):
                console.print(f"{i}. {rec}")


if __name__ == "__main__":
    main()
