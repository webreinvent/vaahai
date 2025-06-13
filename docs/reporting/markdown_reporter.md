# Markdown Reporter

The `MarkdownReporter` is a component of the VaahAI review system that generates structured markdown reports from code review results, providing a portable and readable format for documentation and sharing.

## Overview

The Markdown Reporter converts review results into a well-structured markdown document with:
- Summary statistics and key findings
- Detailed issue list with code blocks
- Recommendations for addressing issues
- Severity and category indicators
- Timestamped file output

## Key Features

### Structured Report Sections

- **Summary**: Overview of the review with file counts and issue statistics
- **Key Findings**: Most important issues identified during the review
- **Statistics**: Detailed breakdown of issues by severity and category
- **Recommendations**: Actionable suggestions for addressing issues
- **Detailed Issues**: Complete list of issues with code snippets and suggested fixes

### Formatting Features

- Code blocks with language-specific syntax highlighting
- Tables for statistics and findings
- Emoji indicators for severity levels and categories
- Hierarchical section organization with proper headings
- Links between sections for easy navigation

### File Management

- Saves reports to timestamped files
- Configurable output directory
- Option to preview report in terminal

## Usage

### Basic Usage

The Markdown Reporter is typically used through the VaahAI CLI review command with the `--format markdown` option:

```bash
vaahai review --format markdown path/to/file.py
```

### Programmatic Usage

```python
from vaahai.reporting.markdown_reporter import MarkdownReporter

# Create a markdown reporter
reporter = MarkdownReporter()

# Generate a report from review results
markdown_content = reporter.generate_report(review_results)

# Save the report to a file
report_path = reporter.save_report(markdown_content, "review_report")

print(f"Report saved to: {report_path}")
```

## Architecture

### Class Structure

```python
class MarkdownReporter:
    def __init__(self, output_dir: Optional[str] = None):
        # Initialize with optional output directory
        
    def generate_report(self, results: Dict[str, Any]) -> str:
        # Generate markdown report from review results
        
    def _generate_summary(self, results: Dict[str, Any]) -> str:
        # Generate summary section
        
    def _generate_key_findings(self, results: Dict[str, Any]) -> str:
        # Generate key findings section
        
    def _generate_statistics(self, results: Dict[str, Any]) -> str:
        # Generate statistics section with tables
        
    def _generate_recommendations(self, results: Dict[str, Any]) -> str:
        # Generate recommendations section
        
    def _generate_detailed_issues(self, results: Dict[str, Any]) -> str:
        # Generate detailed issues section with code blocks
        
    def save_report(self, content: str, base_name: str = "review_report") -> str:
        # Save report to a timestamped file and return the path
```

### Report Structure

The generated markdown report follows this structure:

```markdown
# VaahAI Code Review Report

Generated: 2025-06-14 02:30:22

## Summary

- Files reviewed: 10
- Files with issues: 5
- Total issues found: 15
- Review duration: 2.5 seconds

## Key Findings

1. 🔴 **Critical**: SQL Injection vulnerability in login.py
2. 🟠 **High**: Inefficient database query in users.py
3. 🟡 **Medium**: Inconsistent error handling in api.py

## Statistics

### Issues by Severity

| Severity | Count | Percentage |
|----------|-------|------------|
| Critical | 2     | 13.3%      |
| High     | 5     | 33.3%      |
| Medium   | 6     | 40.0%      |
| Low      | 2     | 13.3%      |

### Issues by Category

| Category   | Count | Percentage |
|------------|-------|------------|
| Security   | 4     | 26.7%      |
| Performance| 6     | 40.0%      |
| Style      | 3     | 20.0%      |
| Quality    | 2     | 13.3%      |

## Recommendations

1. Fix critical security vulnerabilities in login.py
2. Optimize database queries in users.py
3. Standardize error handling across the codebase

## Detailed Issues

### 1. SQL Injection in login.py (Line 25)

**Severity**: Critical  
**Category**: Security  
**File**: login.py  

```python
# Original Code
query = "SELECT * FROM users WHERE username = '" + username + "'"

# Suggested Fix
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

Description: Direct string concatenation in SQL queries can lead to SQL injection attacks...
```

## Integration with Review Command

The Markdown Reporter is integrated with the VaahAI review command to:
- Generate reports from review results
- Save reports to timestamped files
- Display a preview of the report in the terminal
- Provide a consistent output format option

## Error Handling

The Markdown Reporter includes error handling for:
- Invalid or empty review results
- File system errors when saving reports
- Missing or incomplete result data

## Related Documentation

- [Review Command](../cli/review_command.md)
- [HTML Reporter](../reporting/html_reporter.md)
- [Interactive Diff Reporter](../reporting/interactive_diff_reporter.md)
