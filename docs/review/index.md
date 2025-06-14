# VaahAI Review System Documentation

This document serves as the central index for all documentation related to the VaahAI review system, which provides comprehensive code analysis, reporting, and automated code improvement capabilities.

## Overview

The VaahAI review system is a powerful code analysis framework that:

- Scans code for issues related to security, performance, style, and other categories
- Provides detailed feedback with suggested fixes
- Supports multiple output formats (rich terminal, markdown, HTML, interactive)
- Enables interactive code change acceptance and application
- Includes robust safety features like file backups and validation

## Component Documentation

### CLI Commands

- [Review Command](../cli/review_command.md) - Main command for running code reviews with various options

### Core Components

- [Review Steps Registry](../review/steps_registry.md) - Registry for managing and accessing review steps
- [Review Progress Tracking](../review/progress.md) - Framework for tracking review step execution progress
- [Review Statistics Collector](../review/statistics.md) - System for collecting and analyzing review statistics
- [Key Findings Reporter](../review/key_findings.md) - Component for identifying and reporting key findings

### Reporting Components

- [Interactive Diff Reporter](../reporting/interactive_diff_reporter.md) - Terminal-based UI for reviewing and applying code changes
- [Markdown Reporter](../reporting/markdown_reporter.md) - Generator for markdown-formatted review reports
- [HTML Reporter](../reporting/html_reporter.md) - Generator for rich HTML review reports with syntax highlighting
- [Rich Reporter](../reporting/rich_reporter.md) - Terminal output formatter using the Rich library

### Utilities

- [Code Change Manager](../utils/code_change_manager.md) - Utility for safely applying code changes with backup support
- [ReviewRunner](../review/runner.md) - Utility for running multiple review steps with filtering and progress tracking

## Usage Examples

### Basic Review

```bash
vaahai review path/to/file.py
```

### Filtered Review

```bash
vaahai review --category security --severity high path/to/directory
```

### Generate Reports

```bash
# HTML report
vaahai review --format html path/to/project

# Markdown report
vaahai review --format markdown path/to/project
```

### Interactive Review with Code Changes

```bash
vaahai review --format interactive --apply-changes path/to/file.py
```

## Architecture Overview

The VaahAI review system follows a modular architecture with these key components:

1. **Review Steps Registry**: Central registry for all review steps, supporting registration, discovery, and filtering
2. **ReviewRunner**: Core execution engine that runs steps on content, files, or directories
3. **Progress Tracking**: System for monitoring and reporting execution progress
4. **Statistics Collection**: Framework for aggregating and analyzing review results
5. **Reporting System**: Multiple output formats for presenting review results
6. **Code Change Management**: Safe application of suggested code changes with backup support

## Extension Points

The review system can be extended in several ways:

1. **Custom Review Steps**: Create and register new review steps for specific checks
2. **Custom Output Formats**: Implement new report generators for different output formats
3. **Integration with CI/CD**: Run reviews as part of continuous integration pipelines
4. **Custom Filtering**: Implement additional filtering mechanisms for review steps

## Related Documentation

- [Project Task Tracking](../../specs/task_tracking.md) - Overview of completed and planned tasks
- [VaahAI CLI Documentation](../cli/index.md) - Documentation for all VaahAI CLI commands
