# Review Steps Registry

The Review Steps Registry is a central component of VaahAI's code review system that manages the registration, discovery, and execution of review steps.

## Overview

Review steps are individual code analysis units that examine code for specific issues such as security vulnerabilities, performance bottlenecks, style violations, or other concerns. The registry provides a unified interface for registering, discovering, and executing these steps.

## Core Components

### ReviewStep

The `ReviewStep` class represents a single review step with the following properties:

- **ID**: Unique identifier for the step
- **Name**: Human-readable name
- **Description**: Detailed description of what the step checks for
- **Category**: Category of the review step (security, performance, style, etc.)
- **Severity**: Importance level (critical, high, medium, low)
- **Tags**: Additional labels for filtering and organization
- **Run Function**: The function that performs the actual review

### ReviewStepRegistry

The `ReviewStepRegistry` class manages the collection of review steps:

- Provides decorator-based registration of steps
- Validates step configurations against JSON schema
- Supports filtering by ID, category, severity, and tags
- Handles both built-in and custom review steps

### ReviewStepCategory

The `ReviewStepCategory` enum defines standard categories for review steps:

- `SECURITY`: Security vulnerabilities and risks
- `PERFORMANCE`: Performance issues and optimizations
- `STYLE`: Code style and formatting issues
- `QUALITY`: Code quality and maintainability
- `COMPATIBILITY`: Compatibility issues across platforms or versions
- `DOCUMENTATION`: Documentation completeness and quality
- `OTHER`: Miscellaneous issues

### ReviewStepSeverity

The `ReviewStepSeverity` enum defines severity levels for issues:

- `CRITICAL`: Critical issues that must be fixed immediately
- `HIGH`: Important issues that should be addressed soon
- `MEDIUM`: Issues that should be fixed when convenient
- `LOW`: Minor issues that could be improved

## Using the Registry

### Registering a Review Step

```python
from vaahai.review.steps.registry import review_step
from vaahai.review.steps.base import ReviewStepCategory, ReviewStepSeverity

@review_step(
    id="security:sql_injection",
    name="SQL Injection Detection",
    description="Detects potential SQL injection vulnerabilities",
    category=ReviewStepCategory.SECURITY,
    severity=ReviewStepSeverity.CRITICAL,
    tags=["security", "injection", "database"]
)
def detect_sql_injection(content, file_path=None, **kwargs):
    # Implementation of the review step
    issues = []
    # ... analysis logic ...
    return issues
```

### Filtering Review Steps

```python
from vaahai.review.steps.registry import ReviewStepRegistry

registry = ReviewStepRegistry()

# Get all security steps
security_steps = registry.get_steps(category="security")

# Get all critical severity steps
critical_steps = registry.get_steps(severity="critical")

# Get steps by specific IDs
specific_steps = registry.get_steps(step_ids=["security:sql_injection", "performance:inefficient_loops"])

# Get steps by tags
tagged_steps = registry.get_steps(tags=["injection"])
```

## ReviewRunner

The `ReviewRunner` utility class simplifies running multiple review steps:

```python
from vaahai.review.runner import ReviewRunner

# Create a runner with optional filtering
runner = ReviewRunner(
    step_ids=["security:sql_injection"],
    categories=["security"],
    severities=["critical", "high"],
    tags=["injection"]
)

# Run on a single file
results = runner.run_on_file("path/to/file.py")

# Run on a directory
results = runner.run_on_directory("path/to/directory")

# Run on content string
results = runner.run_on_content("SELECT * FROM users WHERE id = " + user_id)
```

## Progress Tracking

The `ReviewProgress` class tracks the status and timing of review steps:

- Records step status (pending, in-progress, completed, failed, skipped)
- Tracks start and end times for each step
- Calculates execution duration
- Provides progress percentage and summary

## Statistics Collection

The `ReviewStatistics` class collects and analyzes issue statistics:

- Counts issues by severity, category, and step
- Identifies most common issues and key findings
- Calculates aggregated statistics
- Generates summary reports

## Built-in Review Steps

VaahAI includes several built-in review steps:

### Security
- SQL Injection Detection
- Command Injection Detection
- Path Traversal Detection
- Insecure Deserialization

### Performance
- Inefficient Loops
- Large Memory Usage
- Redundant Computations

### Style
- Line Length Violations
- Naming Convention Violations
- Indentation Inconsistencies

### Quality
- Duplicate Code
- Complex Functions
- Magic Numbers

## Extending with Custom Steps

You can create custom review steps by:

1. Creating a new Python module with your step function
2. Decorating the function with `@review_step`
3. Implementing the review logic to return issues in the standard format
4. Importing your module to register the step with the registry

## Related Documentation

- [Review Command](../cli/review_command.md)
- [Key Findings Reporter](../reporting/key_findings_reporter.md)
- [Interactive Diff Reporter](../reporting/interactive_diff_reporter.md)
