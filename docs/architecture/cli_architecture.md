# VaahAI CLI Architecture

This document provides an overview of the VaahAI CLI architecture, focusing on the command structure, key components, and extension points.

## Overview

The VaahAI CLI is built using [Typer](https://typer.tiangolo.com/), a modern CLI framework for Python based on [Click](https://click.palletsprojects.com/). The CLI is enhanced with [Rich](https://rich.readthedocs.io/) for beautiful terminal output and [InquirerPy](https://inquirerpy.readthedocs.io/) for interactive prompts.

The architecture follows a modular approach with command groups, allowing for easy extension and maintenance. The CLI is structured to support the core functionality of VaahAI, including configuration management, AI agent interactions, and various analysis commands.

## Command Group Structure

The VaahAI CLI is organized into logical command groups:

```
vaahai
├── core commands (root level)
│   ├── config
│   │   └── init
│   └── helloworld
├── project
│   └── (project-related commands)
├── dev
│   └── (development-related commands)
├── audit
│   └── (code audit commands)
└── review
    └── (code review commands)
```

### Command Groups

1. **Core Commands** (root level):
   - Basic commands like `config`, `helloworld`
   - Entry point for the application

2. **Project Commands** (`vaahai project`):
   - Commands for managing VaahAI projects
   - Organized under the `project` namespace

3. **Dev Commands** (`vaahai dev`):
   - Development and debugging utilities
   - Includes showcase commands for Rich formatting and InquirerPy prompts

4. **Audit Commands** (`vaahai audit`):
   - Code audit functionality
   - Analyzes code for security, compliance, and quality

5. **Review Commands** (`vaahai review`):
   - Code review functionality
   - Focuses on improving code quality and catching bugs

## Key Components

### CLI Entry Point

The main entry point is defined in `vaahai/cli/main.py`, which creates the Typer application and registers all command groups.

### Command Registration

Commands are registered using the `create_typer_app` utility function from `vaahai/cli/utils/help.py`, which ensures consistent help formatting across all commands.

### Utility Modules

- **console.py**: Rich integration for terminal output formatting
- **help.py**: Custom help command formatting
- **config.py**: Configuration management
- **prompts.py**: Interactive prompt utilities using InquirerPy

## Adding New Commands

### Creating a New Command

1. Create a new directory under the appropriate command group:

```
vaahai/cli/commands/[group]/[command_name]/
```

2. Create the following files:
   - `__init__.py`: For package initialization
   - `command.py`: For command implementation

3. Implement the command using the template below:

```python
"""
[Command description]
"""
from typing import Optional

import typer
from rich.panel import Panel

from vaahai.cli.utils.console import console
from vaahai.cli.utils.help import CustomHelpCommand, create_typer_app

# Create command app
app = create_typer_app(
    name="command_name",
    help="Command description",
    short_help="Short description",
)

@app.callback(cls=CustomHelpCommand)
def callback():
    """Command group description."""
    pass

@app.command()
def main(
    param: str = typer.Option(..., help="Parameter description"),
):
    """Main command implementation."""
    console.print(Panel.fit(f"Command executed with param: {param}"))
    return 0
```

4. Register the command in the appropriate command group's `__init__.py`:

```python
from vaahai.cli.commands.[group].[command_name].command import app as command_name_app

__all__ = ["command_name_app"]
```

### Creating a New Command Group

1. Create a new directory under `vaahai/cli/commands/`:

```
vaahai/cli/commands/[group_name]/
```

2. Create an `__init__.py` file with the following content:

```python
"""
[Group description]
"""
import typer

from vaahai.cli.utils.help import CustomHelpGroup, create_typer_app

app = create_typer_app(
    name="group_name",
    help="Group description",
    short_help="Short description",
    cls=CustomHelpGroup,
)

# Import and add subcommands
# from vaahai.cli.commands.[group_name].[command] import app as command_app
# app.add_typer(command_app, name="command")

__all__ = ["app"]
```

3. Register the command group in `vaahai/cli/main.py`:

```python
from vaahai.cli.commands.[group_name] import app as group_name_app
app.add_typer(group_name_app, name="group_name")
```

## Best Practices

1. **Command Organization**:
   - Keep related commands in the same command group
   - Use subcommands for complex functionality
   - Follow the established directory structure

2. **Command Implementation**:
   - Use the `create_typer_app` utility for consistent help formatting
   - Apply `cls=CustomHelpCommand` to all command decorators
   - Provide comprehensive help text for commands and options
   - Return appropriate exit codes (0 for success, non-zero for errors)

3. **Output Formatting**:
   - Use the console utilities from `vaahai.cli.utils.console` for consistent output
   - Follow the established styling patterns for different message types
   - Use panels, tables, and other Rich components appropriately

4. **User Interaction**:
   - Use prompt utilities from `vaahai.cli.utils.prompts` for user input
   - Provide clear feedback for user actions
   - Handle errors gracefully with informative messages
