# HTML Reporter

The `HTMLReporter` is a component of the VaahAI review system that generates rich, interactive HTML reports from code review results, providing a visually appealing and user-friendly format for documentation and sharing.

## Overview

The HTML Reporter converts review results into a comprehensive HTML document with:
- Summary statistics and key findings
- Detailed issue list with syntax-highlighted code blocks
- Interactive elements for navigation and filtering
- Visual indicators for severity and category
- Responsive design for viewing on different devices

## Key Features

### Rich Visual Presentation

- Syntax-highlighted code blocks using Pygments
- Color-coded severity indicators
- Category icons and badges
- Collapsible sections for better organization
- Responsive layout with CSS styling

### Interactive Elements

- Collapsible issue details
- Filtering options by severity and category
- Jump-to navigation for quick access to sections
- Copy buttons for code snippets
- Expandable code context

### Report Structure

- Summary dashboard with statistics and charts
- Key findings section highlighting critical issues
- Detailed recommendations with actionable steps
- Complete issue list with code context and suggested fixes
- Metadata section with review information

## Usage

### Basic Usage

The HTML Reporter is typically used through the VaahAI CLI review command with the `--format html` option:

```bash
vaahai review --format html path/to/file.py
```

### Programmatic Usage

```python
from vaahai.reporting.html_reporter import HTMLReporter

# Create an HTML reporter
reporter = HTMLReporter()

# Generate a report from review results
html_content = reporter.generate_report(review_results)

# Save the report to a file
report_path = reporter.save_report(html_content, "review_report")

print(f"Report saved to: {report_path}")
```

## Architecture

### Class Structure

```python
class HTMLReporter:
    def __init__(self, output_dir: Optional[str] = None):
        # Initialize with optional output directory
        
    def generate_report(self, results: Dict[str, Any]) -> str:
        # Generate HTML report from review results
        
    def _generate_header(self, results: Dict[str, Any]) -> str:
        # Generate HTML header with metadata and CSS
        
    def _generate_summary(self, results: Dict[str, Any]) -> str:
        # Generate summary section with statistics
        
    def _generate_key_findings(self, results: Dict[str, Any]) -> str:
        # Generate key findings section
        
    def _generate_recommendations(self, results: Dict[str, Any]) -> str:
        # Generate recommendations section
        
    def _generate_detailed_issues(self, results: Dict[str, Any]) -> str:
        # Generate detailed issues section with syntax-highlighted code
        
    def _highlight_code(self, code: str, language: str) -> str:
        # Highlight code using Pygments
        
    def save_report(self, content: str, base_name: str = "review_report") -> str:
        # Save report to a timestamped file and return the path
```

### HTML Structure

The generated HTML report follows this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VaahAI Code Review Report</title>
    <style>
        /* CSS styling for the report */
    </style>
</head>
<body>
    <header>
        <h1>VaahAI Code Review Report</h1>
        <p>Generated: 2025-06-14 02:30:22</p>
    </header>
    
    <section id="summary">
        <h2>Summary</h2>
        <div class="stats-container">
            <!-- Statistics panels -->
        </div>
    </section>
    
    <section id="key-findings">
        <h2>Key Findings</h2>
        <div class="findings-list">
            <!-- List of key findings -->
        </div>
    </section>
    
    <section id="recommendations">
        <h2>Recommendations</h2>
        <div class="recommendations-list">
            <!-- List of recommendations -->
        </div>
    </section>
    
    <section id="detailed-issues">
        <h2>Detailed Issues</h2>
        <div class="issues-container">
            <!-- Detailed issues with code blocks -->
        </div>
    </section>
    
    <script>
        // JavaScript for interactive elements
    </script>
</body>
</html>
```

## CSS Styling

The HTML Reporter includes comprehensive CSS styling for:
- Typography and layout
- Color schemes for severity levels
- Code block styling with syntax highlighting
- Responsive design for different screen sizes
- Interactive elements like collapsible sections

## JavaScript Features

The report includes JavaScript for:
- Collapsible sections
- Filtering issues by severity and category
- Copy-to-clipboard functionality for code snippets
- Navigation between sections
- Toggling between original and suggested code

## Integration with Review Command

The HTML Reporter is integrated with the VaahAI review command to:
- Generate reports from review results
- Save reports to timestamped files
- Open reports in the default browser (optional)
- Display a preview of the report in the terminal

## Error Handling

The HTML Reporter includes error handling for:
- Invalid or empty review results
- File system errors when saving reports
- Missing or incomplete result data
- Unsupported code languages for syntax highlighting

## Related Documentation

- [Review Command](../cli/review_command.md)
- [Markdown Reporter](../reporting/markdown_reporter.md)
- [Interactive Diff Reporter](../reporting/interactive_diff_reporter.md)
