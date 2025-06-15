# VaahAI CLI Warning System

The VaahAI CLI includes a comprehensive warning system that displays configuration warnings and other important messages to users across all CLI commands. This document explains how the warning system works and how to use it in your code.

## Overview

The warning system is designed to:

1. Display configuration warnings when VaahAI is not properly configured
2. Show warnings in a consistent, styled format using Rich panels
3. Include actionable information like fix commands and documentation links
4. Respect global CLI options like `--quiet`
5. Avoid circular warnings (e.g., not showing config warnings during config commands)

## Warning Categories and Levels

Warnings are categorized by both type and severity:

### Warning Categories

- `CONFIGURATION`: Issues related to VaahAI configuration
- `DEPENDENCY`: Missing or incompatible dependencies
- `PERMISSION`: Permission-related issues
- `NETWORK`: Network connectivity problems
- `PERFORMANCE`: Performance-related warnings
- `SECURITY`: Security concerns
- `COMPATIBILITY`: Compatibility issues
- `GENERAL`: General warnings

### Warning Levels

- `ERROR`: Critical issues that prevent proper functioning
- `WARNING`: Important issues that may affect functionality
- `INFO`: Informational messages

## Using the Warning System

### Basic Usage

The simplest way to use the warning system is through the `check_and_display_warnings` function:

```python
from vaahai.cli.utils.warning_system import check_and_display_warnings

def my_command():
    # Check for warnings at the beginning of your command
    check_and_display_warnings(command_name="my_command")
    
    # Rest of your command logic
    # ...
```

This will automatically check for configuration issues and display appropriate warnings.

### Advanced Usage

For more control, you can create and use a `WarningSystem` instance directly:

```python
from vaahai.cli.utils.warning_system import (
    WarningSystem, WarningMessage, WarningCategory, WarningLevel
)

def my_command(quiet: bool = False):
    # Create a warning system
    system = WarningSystem(quiet=quiet)
    
    # Add configuration warnings
    system.add_config_warnings()
    
    # Add custom warnings
    system.add_warning(
        WarningMessage(
            level=WarningLevel.WARNING,
            category=WarningCategory.DEPENDENCY,
            message="Required package 'xyz' is not installed",
            details="This package is needed for advanced features.",
            fix_command="pip install xyz",
            docs_url="https://docs.vaahai.io/dependencies",
        )
    )
    
    # Display warnings
    system.display_warnings()
    
    # Rest of your command logic
    # ...
```

### Creating Custom Warning Messages

You can create custom warning messages using the `WarningMessage` class:

```python
from vaahai.cli.utils.warning_system import WarningMessage, WarningCategory, WarningLevel

warning = WarningMessage(
    level=WarningLevel.ERROR,
    category=WarningCategory.NETWORK,
    message="Unable to connect to API server",
    details="Check your internet connection and try again.",
    fix_command="vaahai config set api.url https://api.vaahai.io",
    docs_url="https://docs.vaahai.io/troubleshooting/network",
)
```

## Integration with CLI Commands

The warning system is integrated with the main CLI app in `vaahai/cli/main.py`. It automatically checks for configuration warnings for all commands except those starting with `config`.

### Respecting the `--quiet` Flag

The warning system respects the global `--quiet` flag. When this flag is set, no warnings will be displayed:

```bash
vaahai review run --quiet ./my-project
```

## Styling and Output

Warnings are displayed using Rich panels with appropriate styling:

- Error warnings have red borders and an error icon
- Warning-level warnings have yellow borders and a warning icon
- Info-level warnings have blue borders and an info icon

Each warning includes:
- A clear message
- Additional details (if provided)
- A fix command (if applicable)
- A link to documentation (if applicable)

## Implementation Details

The warning system is implemented in `vaahai/cli/utils/warning_system.py` and consists of:

1. `WarningCategory` and `WarningLevel` enums for categorization
2. `WarningMessage` class to encapsulate warning details
3. `WarningSystem` class to collect and display warnings
4. `check_and_display_warnings` function for easy integration

The system uses the VaahAI console utilities for styled output and integrates with the `ConfigValidator` to check for configuration issues.

## Best Practices

1. Use the warning system for important messages that users should be aware of
2. Include actionable information in warnings (fix commands, documentation links)
3. Categorize warnings appropriately to help users understand the issue
4. Use the appropriate warning level based on severity
5. Respect the `--quiet` flag for non-essential output
