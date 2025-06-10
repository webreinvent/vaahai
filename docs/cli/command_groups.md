# VaahAI CLI Command Groups

This document provides an overview of the command group structure in the VaahAI CLI. For a more comprehensive explanation of the CLI architecture, including extension points and best practices, see the [CLI Architecture Documentation](/docs/architecture/cli_architecture.md).

## Overview

The VaahAI CLI is organized into logical command groups to improve usability and maintainability. Each group contains related commands that serve a specific purpose.

## Enhanced Help System

All command groups and commands feature a Rich-formatted custom help system that provides:

- Styled headers with command name and description
- Organized tables for subcommands and options
- Consistent formatting across all command levels
- Detailed descriptions and usage examples
- Visual separation between different sections

To access the enhanced help for any command group:

```bash
vaahai [command_group] --help
```

For example:
```bash
vaahai core --help
vaahai project --help
vaahai dev --help
```

For more details about the custom help implementation, see [Custom Help Formatting](custom_help_formatting.md).

## Command Group Structure

The CLI is organized into the following command groups:

### Core Commands

Core commands handle fundamental functionality like configuration and version information:

- `vaahai config`: Configuration management
  - `vaahai config init`: Set up initial configuration
  - `vaahai config show`: Display current configuration
- `vaahai version`: Display version information
- `vaahai model`: Model selection and management
  - `vaahai model list`: List available models with filtering options
  - `vaahai model info`: Show detailed information about a specific model
  - `vaahai model set`: Set the current model for a provider
  - `vaahai model recommend`: Get recommended model based on capabilities
  - `vaahai model capabilities`: List available model capabilities

### Project Commands

Project commands are used for analyzing and improving code:

- `vaahai review`: Code review commands
  - `vaahai review run`: Run a code review on specified path
- `vaahai audit`: Security and compliance audit commands
  - `vaahai audit run`: Run a security/compliance audit on specified path

### Development Commands

Development commands are primarily used during development and testing:

- `vaahai dev helloworld`: Test command to verify proper functioning
- `vaahai dev showcase`: Demonstrate Rich formatting capabilities

## Backward Compatibility

For backward compatibility, direct command access is also supported. For example, both of these commands are equivalent:

```bash
vaahai dev helloworld run
vaahai helloworld run
```

## Command Help

Each command and command group supports the `--help` flag to display detailed usage information:

```bash
# Show help for all commands
vaahai --help

# Show help for a command group
vaahai dev --help

# Show help for a specific command
vaahai config --help
```

## Global Options

The following options are available for all commands:

- `--verbose`: Enable verbose output (can also be set with `VAAHAI_VERBOSE=1`)
- `--quiet`: Suppress non-essential output (can also be set with `VAAHAI_QUIET=1`)
- `--config PATH`: Specify a custom configuration file path
- `--help`: Show help message and exit

## Implementation Details

The command group structure is implemented using Typer's `typer.Typer()` instances for each group, which are then added to the main application using `app.add_typer()`.

For example, the core command group is defined as:

```python
# Create the core commands group
core_app = typer.Typer(
    help="Core commands for configuration and system information"
)

# Add commands to the core group
core_app.add_typer(config_app, name="config")
core_app.add_typer(version_app, name="version")
```

And then added to the main application:

```python
# Add command groups to the main app
app.add_typer(core_app, name="core")
```

## Adding New Commands

When adding new commands to the VaahAI CLI, follow these guidelines:

1. Determine which command group the new command belongs to (core, project, or dev)
2. Create a new module in the appropriate command group directory
3. Define a `typer.Typer()` instance for your command using the `create_typer_app` utility
4. Implement the command functionality using Typer decorators with `cls=CustomHelpCommand`
5. Register your command with the appropriate command group

For detailed instructions and best practices, refer to the [CLI Architecture Documentation](/docs/architecture/cli_architecture.md).

For example, to add a new command to the core group:

```python
# In vaahai/cli/commands/core/mycommand.py
from vaahai.cli.utils.help import create_typer_app, CustomHelpCommand

mycommand_app = create_typer_app(help="My new command")

@mycommand_app.callback()
def callback():
    """My new command."""
    pass

@mycommand_app.command("run", cls=CustomHelpCommand)
def run():
    """Run my new command."""
    # Command implementation here
    pass

# In vaahai/cli/commands/core/__init__.py
from vaahai.cli.commands.core.mycommand import mycommand_app

# Add to core_app
core_app.add_typer(mycommand_app, name="mycommand")
```

## Testing Command Groups

When testing command groups, ensure that:

1. The command group appears in the help output
2. Commands within the group are accessible
3. Direct command access (for backward compatibility) works correctly

See `vaahai/tests/cli/test_command_groups.py` for examples of command group tests.
