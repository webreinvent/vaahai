# VaahAI Console Utilities

This document provides a comprehensive guide to the console output utilities available in the VaahAI CLI. These utilities are designed to provide consistent, styled terminal output across all CLI commands.

## Table of Contents

- [Overview](#overview)
- [Basic Output Functions](#basic-output-functions)
- [Enhanced Output Functions](#enhanced-output-functions)
- [Structured Data Output](#structured-data-output)
- [Formatting Helpers](#formatting-helpers)
- [Context Managers](#context-managers)
- [Environment Handling](#environment-handling)
- [Usage Examples](#usage-examples)

## Overview

The console utilities are built on top of the [Rich](https://github.com/Textualize/rich) library and provide a consistent way to display information to the user. They include:

- Styled message output (success, error, warning, info, verbose)
- Environment-aware output filtering (quiet, verbose, non-TTY)
- Structured data presentation (tables, panels, code blocks, markdown)
- Command execution formatting
- Progress indicators and spinners
- Formatting helpers for common elements

All utilities are available in the `vaahai.cli.utils.console` module.

## Basic Output Functions

### Message Types

These functions provide consistent styling for different types of messages:

```python
from vaahai.cli.utils.console import (
    print_success,
    print_error,
    print_warning,
    print_info,
    print_verbose
)

# Success message (green with checkmark)
print_success("Operation completed successfully")

# Error message (red with X)
print_error("Failed to complete operation")

# Warning message (yellow with warning symbol)
print_warning("Proceed with caution")

# Info message (blue with info symbol)
print_info("Here's some information")

# Verbose message (only shown in verbose mode)
print_verbose("Detailed debug information")
```

### Headers and Panels

For more structured output:

```python
from vaahai.cli.utils.console import print_header, print_panel

# Print a header with optional subtitle
print_header("Main Title", "Optional subtitle")

# Print a panel with optional title and style
print_panel("Content inside panel", title="Panel Title", style="success")
```

### Code and Markdown

For displaying code and formatted text:

```python
from vaahai.cli.utils.console import print_code, print_markdown

# Display syntax-highlighted code
print_code("def hello(): print('Hello world')", language="python", title="Example Function")

# Display formatted markdown
print_markdown("# Heading\n\nThis is **bold** text and this is *italic* text.")
```

### Tables

For tabular data:

```python
from vaahai.cli.utils.console import print_table, create_table

# Quick table with headers and rows
columns = ["Name", "Type", "Description"]
rows = [
    ["config", "Command", "Manage configuration"],
    ["review", "Command", "Review code"]
]
print_table(columns, rows, title="Commands")

# More customized table
table = create_table(title="Custom Table")
table.add_column("Name", style="cyan")
table.add_column("Value", style="green")
table.add_row("Setting 1", "Enabled")
table.add_row("Setting 2", "Disabled")
console.print(table)
```

## Enhanced Output Functions

### Command Execution Formatting

For displaying command execution flow:

```python
from vaahai.cli.utils.console import (
    print_command_start,
    print_command_result,
    print_step,
    print_section
)

# Start of a command execution
print_command_start("vaahai config init", "Initialize VaahAI configuration")

# Show steps in a multi-step process
print_step(1, 3, "Checking existing configuration")
print_step(2, 3, "Creating new configuration file")
print_step(3, 3, "Setting default values")

# Show the result of a command
print_command_result(True, "Configuration initialized successfully")

# Create a section divider
print_section("Configuration Summary")
```

## Structured Data Output

For displaying structured data in various formats:

```python
from vaahai.cli.utils.console import (
    print_key_value,
    print_list,
    print_tree,
    print_columns,
    print_json
)

# Key-value pairs
print_key_value("Project", "VaahAI")
print_key_value("Version", "0.2.15")

# Bulleted lists
print_list(["First item", "Second item", "Third item"], "Sample List")

# Tree structures
tree_data = {
    "vaahai": {
        "cli": {
            "commands": "Command implementations",
            "utils": {
                "console.py": "Console utilities",
                "help.py": "Help formatting"
            }
        },
        "agents": "AI agent implementations"
    }
}
print_tree(tree_data, "Project Structure")

# Columnar layout
print_columns(["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6"], num_columns=3)

# JSON data
json_data = {
    "name": "VaahAI",
    "version": "0.2.15",
    "dependencies": {
        "typer": "0.7.0",
        "rich": "latest"
    }
}
print_json(json_data, "Project Configuration")
```

## Formatting Helpers

For consistent styling of common elements:

```python
from vaahai.cli.utils.console import (
    format_highlight,
    format_key,
    format_value,
    format_status,
    format_path,
    format_command,
    format_url
)

# Use with console.print() or within other strings
console.print(f"Highlighted text: {format_highlight('Important information')}")
console.print(f"Key: {format_key('api_key')}")
console.print(f"String value: {format_value('hello', 'string')}")
console.print(f"Number value: {format_value('42', 'number')}")
console.print(f"Boolean value: {format_value('true', 'boolean')}")
console.print(f"Status: {format_status('success')}")
console.print(f"File path: {format_path('/path/to/file.py')}")
console.print(f"Command: {format_command('vaahai config init')}")
console.print(f"URL: {format_url('https://example.com')}")
```

## Context Managers

For progress reporting and output capturing:

```python
from vaahai.cli.utils.console import progress_spinner, capture_console_output

# Show a spinner during a long-running operation
with progress_spinner("Loading data...") as spinner:
    # Do some work
    spinner.update("Processing data...")
    # Do more work

# Capture console output for testing
with capture_console_output() as output:
    print_info("Test message")
    assert "Test message" in output.getvalue()
```

## Environment Handling

The console utilities are environment-aware and respect the following settings:

- **Verbose mode**: Set the `VAAHAI_VERBOSE` environment variable to `1` or use the `--verbose` flag
- **Quiet mode**: Set the `VAAHAI_QUIET` environment variable to `1` or use the `--quiet` flag
- **Debug mode**: Set the `VAAHAI_DEBUG` environment variable to `1` for detailed tracebacks

Helper functions for environment detection:

```python
from vaahai.cli.utils.console import is_tty, is_verbose, is_quiet, should_output

# Check if running in a TTY (interactive terminal)
if is_tty():
    # Show interactive elements
    pass

# Check if verbose mode is enabled
if is_verbose():
    # Show verbose output
    pass

# Check if quiet mode is enabled
if is_quiet():
    # Suppress non-essential output
    pass

# Check if output should be shown based on type
if should_output("normal"):
    # Show normal output
    pass

if should_output("verbose"):
    # Show verbose output
    pass

if should_output("important"):
    # Show important output (always shown)
    pass
```

## Usage Examples

### Basic Command Output

```python
def my_command():
    print_header("My Command", "Does something useful")
    
    try:
        # Command logic
        print_success("Command completed successfully")
    except Exception as e:
        print_error(f"Command failed: {str(e)}")
```

### Multi-step Process

```python
def complex_command():
    print_command_start("complex-command", "Performs a multi-step operation")
    
    # Step 1
    print_step(1, 3, "Preparing data")
    # Step 1 logic
    
    # Step 2
    print_step(2, 3, "Processing data")
    # Step 2 logic
    
    # Step 3
    print_step(3, 3, "Finalizing results")
    # Step 3 logic
    
    print_command_result(True, "Complex command completed successfully")
```

### Displaying Structured Data

```python
def show_config():
    print_header("Configuration")
    
    # Show key-value pairs
    print_key_value("API Key", "****abcd")
    print_key_value("Model", "gpt-4")
    print_key_value("Debug Mode", "Enabled")
    
    # Show a tree structure
    config_data = {
        "api": {
            "key": "****abcd",
            "base_url": "https://api.example.com"
        },
        "models": ["gpt-4", "claude-3"],
        "debug": True
    }
    print_tree(config_data, "Full Configuration")
```

### Progress Reporting

```python
def long_running_task():
    with progress_spinner("Processing files...") as spinner:
        # Process first batch
        spinner.update("Processing batch 1/3...")
        # Processing logic
        
        # Process second batch
        spinner.update("Processing batch 2/3...")
        # Processing logic
        
        # Process third batch
        spinner.update("Processing batch 3/3...")
        # Processing logic
    
    print_success("All files processed successfully")
```

For a live demonstration of all available formatting options, run:

```bash
vaahai dev showcase
```

This will display a comprehensive showcase of all the Rich formatting capabilities available in the VaahAI CLI.
