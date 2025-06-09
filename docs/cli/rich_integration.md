# VaahAI CLI Rich Integration

This document provides an overview of the Rich formatting utilities available in the VaahAI CLI and how to use them in your commands.

## Overview

The VaahAI CLI uses the [Rich](https://github.com/Textualize/rich) library to provide consistent, styled terminal output across all CLI commands. The Rich integration is centralized in the `vaahai.cli.utils.console` module, which provides a set of utility functions for common formatting tasks.

## Basic Usage

Import the necessary functions from the console module:

```python
from vaahai.cli.utils.console import (
    console,
    print_header,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_verbose,
)
```

Then use these functions to output formatted text:

```python
print_header("Command Title", "Optional subtitle")
print_success("Operation completed successfully")
print_error("An error occurred")
print_warning("This is a warning message")
print_info("This is an informational message")
print_verbose("This is only shown in verbose mode")
```

## Available Utilities

### Message Types

- `print_header(title, subtitle=None)`: Print a formatted header with optional subtitle
- `print_success(message)`: Print a success message (✓)
- `print_error(message)`: Print an error message (✗)
- `print_warning(message)`: Print a warning message (⚠)
- `print_info(message)`: Print an info message (ℹ)
- `print_verbose(message)`: Print a verbose message (only shown in verbose mode)

### Panels and Blocks

- `print_panel(content, title=None, style="blue", expand=True, box=ROUNDED)`: Print content in a panel with optional title
- `print_code(code, language="python", line_numbers=True, title=None, theme="monokai")`: Print formatted code with syntax highlighting
- `print_markdown(markdown_text)`: Print formatted markdown text

### Tables

- `create_table(columns, rows, title=None, show_header=True, box=ROUNDED, padding=1, expand=False)`: Create a formatted table
- `print_table(columns, rows, title=None, show_header=True, box=ROUNDED, padding=1, expand=False)`: Create and print a formatted table

### Interactive Elements

- `ask_question(question, default=None, choices=None)`: Ask the user a question and return their response
- `confirm(question, default=False)`: Ask the user for confirmation
- `create_progress()`: Create a progress bar with VaahAI styling

### Formatted Elements

- `format_path(path)`: Format a file path with consistent styling
- `format_command(command)`: Format a command with consistent styling
- `format_url(url)`: Format a URL with consistent styling

### Environment Handling

- `is_tty()`: Check if the current environment is a TTY
- `is_verbose()`: Check if verbose mode is enabled
- `is_quiet()`: Check if quiet mode is enabled
- `should_output(level="normal")`: Determine if output should be shown based on verbosity level

## Environment Variables

The Rich integration respects the following environment variables:

- `VAAHAI_VERBOSE=1`: Enable verbose output
- `VAAHAI_QUIET=1`: Suppress non-essential output

## Example: Creating a Command with Rich Output

Here's an example of how to create a command that uses Rich formatting:

```python
import typer
from vaahai.cli.utils.console import (
    console,
    print_header,
    print_success,
    print_error,
    print_panel,
    print_table,
    ask_question,
    confirm,
)

app = typer.Typer()

@app.command()
def example():
    """Example command with Rich formatting."""
    print_header("Example Command", "Demonstrating Rich formatting")

    # Show a panel with information
    print_panel("This command demonstrates Rich formatting", title="Info")

    # Show a table
    columns = ["Name", "Value"]
    rows = [
        ["Option 1", "Value 1"],
        ["Option 2", "Value 2"],
    ]
    print_table(columns, rows, title="Options")

    # Interactive elements (only in TTY)
    try:
        if confirm("Continue with the operation?"):
            # Perform operation
            print_success("Operation completed successfully")
        else:
            print_error("Operation cancelled")
    except Exception as e:
        print_error(f"Error: {e}")
```

## Showcase Command

The VaahAI CLI includes a showcase command that demonstrates all the Rich formatting capabilities. You can run it with:

```bash
vaahai dev showcase
```

This command serves as both a demonstration and an example of how to use the formatting utilities.

## Best Practices

1. **Use the appropriate message type**: Choose the right function for the context (success, error, warning, info).
2. **Respect verbosity settings**: Use `print_verbose` for detailed information that should only be shown in verbose mode.
3. **Handle non-TTY environments**: Use try/except blocks around interactive elements and provide fallbacks.
4. **Maintain consistent styling**: Use the provided utility functions rather than direct console styling.
5. **Keep it concise**: Terminal output should be clear and to the point.

## Contributing

When adding new commands to the VaahAI CLI, please use these Rich formatting utilities to ensure a consistent user experience across all commands.
