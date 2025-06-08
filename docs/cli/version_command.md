# VaahAI Version Command

This document describes the version command and version flag functionality in VaahAI CLI.

## Overview

VaahAI provides two ways to check the installed version:

1. Using the `--version` flag with the main command
2. Using the dedicated `version` command

Both methods display the current version of VaahAI installed on your system.

## Using the `--version` Flag

The `--version` flag is a global option that can be used with the main `vaahai` command:

```bash
vaahai --version
```

This will display the current version and exit immediately, without executing any other commands.

**Aliases**: `-v`

**Example output**:
```
VaahAI version: 0.2.18
```

## Using the `version` Command

For backward compatibility and additional version-related functionality, VaahAI also provides a dedicated version command:

```bash
vaahai version show
```

This command displays the version information in a styled panel using Rich formatting.

**Example output**:
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃           Version Information          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│                                        │
│  VaahAI version: 0.2.18                │
│                                        │
└────────────────────────────────────────┘
```

## Implementation Details

The version information is retrieved using Python's `importlib.metadata` module, which reads the package version from the installed metadata.

If VaahAI is running in development mode (not installed as a package), the version will be displayed as "unknown (development mode)".

## Related Global Options

Other global options available in VaahAI CLI:

- `--verbose`, `-V`: Enable verbose output with detailed logs and information
- `--quiet`, `-q`: Suppress non-essential output
- `--config`: Specify an alternative configuration file path
- `--help`, `-h`: Show help message and exit
