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
- [Warning System](warning_system.md): Configuration warning system across CLI commands
- [Model Command](model_command.md): Managing and selecting LLM models based on capabilities
- [Review Command](review_command.md): Comprehensive code review with multiple output formats and interactive features
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

## Featured Commands

### Review Command

The `review` command is a powerful code analysis tool that scans your codebase for issues related to security, performance, style, and other categories:

```bash
# Basic usage
vaahai review path/to/file.py

# With output format selection
vaahai review path/to/file.py --format html

# With interactive code change acceptance
vaahai review path/to/file.py --format interactive --apply-changes

# With filtering by category and severity
vaahai review path/to/directory --category security --severity high
```

For detailed documentation on the review command, see [Review Command](review_command.md).

### Model Command

The `model` command helps you manage and select LLM models based on their capabilities:

```bash
# List available models
vaahai model list

# Get details about a specific model
vaahai model info gpt-4

# Filter models by capability
vaahai model list --capability code
```

For more information, see [Model Command](model_command.md).
