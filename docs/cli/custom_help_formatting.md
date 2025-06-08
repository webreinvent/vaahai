# Custom Help Formatting in VaahAI CLI

This document explains how to implement and use the custom Rich-formatted help in VaahAI CLI commands.

## Overview

VaahAI CLI uses custom Typer command and group classes to override the default help display and provide Rich-formatted help output. This ensures a consistent, visually appealing, and informative help display across all CLI commands.

## Key Components

1. **CustomHelpCommand**: A custom `TyperCommand` subclass that overrides the `get_help` method to display Rich-formatted help for individual commands.

2. **CustomHelpGroup**: A custom `TyperGroup` subclass that overrides the `get_help` method to display Rich-formatted help for command groups and the main CLI app.

3. **Utility Functions**:
   - `create_typer_app()`: Creates a Typer app with custom help formatting applied.

## How to Use

### Creating a Command Group

To create a command group with custom help formatting, use the `create_typer_app()` function:

```python
from vaahai.cli.utils.help import create_typer_app

# Create a command group with custom help formatting
app = create_typer_app(
    name="command_name",
    help="Description of the command",
    add_completion=False,
)
```

### Creating Commands

To create a command with custom help formatting, use the `@app.command()` decorator with the `cls=CustomHelpCommand` parameter:

```python
from vaahai.cli.utils.help import CustomHelpCommand

@app.command("subcommand", cls=CustomHelpCommand)
def subcommand():
    """
    Description of the subcommand.
    """
    # Command implementation
```

### Complete Example

Here's a complete example of a command implementation with custom help formatting:

```python
"""
Example command implementation.
"""

import typer
from vaahai.cli.utils.console import print_success
from vaahai.cli.utils.help import create_typer_app, CustomHelpCommand

# Create the command group with custom help formatting
app = create_typer_app(
    name="example",
    help="Example command with custom help formatting",
    add_completion=False,
)


@app.callback()
def callback():
    """
    Callback for the example command group.
    """
    pass


@app.command("run", cls=CustomHelpCommand)
def run(
    path: str = typer.Argument(..., help="Path to process"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """
    Run the example command.
    """
    print_success(f"Processing {path}")
```

## Help Output Format

The custom help formatting provides:

1. **Main CLI Help**:
   - Styled header with app name and description
   - Usage section
   - Command groups table with examples
   - Direct access commands table with examples
   - Global options table
   - Environment variables panel
   - Quick reference panel

2. **Command Group Help**:
   - Styled header with command group name and description
   - Usage section
   - Subcommands table
   - Options table (if applicable)
   - Arguments table (if applicable)
   - Examples panel (if available)

3. **Command Help**:
   - Styled header with command name and description
   - Usage section
   - Options table (if applicable)
   - Arguments table (if applicable)
   - Examples panel (if available)

## Best Practices

1. Always use `create_typer_app()` for creating command groups.
2. Always specify `cls=CustomHelpCommand` when creating commands with `@app.command()`.
3. Provide clear and concise help text for commands, options, and arguments.
4. Follow the template in `docs/cli/command_template.py` for consistent implementation.

## Troubleshooting

If the custom help formatting is not working correctly:

1. Ensure you've imported `create_typer_app` and `CustomHelpCommand` from `vaahai.cli.utils.help`.
2. Verify that you're using `create_typer_app()` to create your command group.
3. Check that you've specified `cls=CustomHelpCommand` in your `@app.command()` decorator.
4. Make sure your docstrings are properly formatted.
