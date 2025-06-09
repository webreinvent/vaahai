# VaahAI CLI Documentation

This section provides comprehensive documentation for the VaahAI CLI, including its command structure, features, and usage patterns.

## Overview

VaahAI CLI is built with the Typer framework and enhanced with Rich formatting for an improved user experience. The CLI follows a modular structure with command groups, commands, and actions, providing a consistent and intuitive interface for users.

## Key Features

- **Modular Command Structure**: Organized into logical command groups (core, project, dev)
- **Enhanced Help System**: Rich-formatted help output with styled headers, tables, and descriptions
- **Interactive Prompts**: User-friendly prompts with InquirerPy integration
- **Consistent Output Formatting**: Standardized Rich-formatted output for all commands
- **Global Options**: Common options available across all commands
- **Backward Compatibility**: Direct command access alongside command groups

## Documentation Sections

- [Command Groups](command_groups.md): Overview of the command group structure
- [Rich Integration](rich_integration.md): Details on Rich formatting capabilities
- [Console Utilities](console_utilities.md): Helper functions for console output
- [Custom Help Formatting](custom_help_formatting.md): Implementation of the enhanced help system
- [CLI Architecture](/docs/architecture/cli_architecture.md): Comprehensive overview of CLI architecture, extension points, and best practices
- [Command Template](command_template.py): Example template for creating new commands

## Getting Started

To get started with the VaahAI CLI, first ensure you have installed the package:

```bash
pip install vaahai
```

Then, you can explore the available commands using the enhanced help system:

```bash
vaahai --help
```

This will display a Rich-formatted overview of all available command groups and commands, along with global options and usage examples.

For more detailed information about a specific command or command group, use:

```bash
vaahai [command_group] --help
vaahai [command_group] [command] --help
```

## CLI Structure

The VaahAI CLI follows this general structure:

```
vaahai [command_group] [command] [action] [options]
```

Where:
- `vaahai` is the main CLI application
- `command_group` is one of the logical groups (core, project, dev)
- `command` is a specific command within that group
- `action` is a subcommand or action for that command
- `options` are additional flags and parameters

For backward compatibility, direct command access (e.g., `vaahai helloworld` instead of `vaahai dev helloworld`) is also supported.
