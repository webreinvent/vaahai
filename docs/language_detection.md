# Language Detection

The `vaahai detect-language` command allows you to detect programming languages, versions, and frameworks used in your code files.

## Overview

This command analyzes code files and directories to identify:
- Programming languages used
- Language distribution across your project
- Version information (when detectable)
- Frameworks and libraries used

## Installation

The `detect-language` command is installed as part of the Vaahai package:

```bash
pip install vaahai
```

As of version 0.2.8, the `detect-language` command is fully integrated with the Vaahai CLI and works seamlessly when installed via pip:

```bash
# Install the latest version
pip install vaahai

# Run the command
vaahai detect-language [path] [options]
```

### Standalone Installation

While the main CLI integration has been fixed in version 0.2.8, we still provide a standalone installation method for users who prefer it or are using older versions:

```bash
# Navigate to the Vaahai project directory
cd /path/to/vaahai

# Run the installation script (requires sudo)
sudo ./bin/install-detect-language.sh

# Or for a local installation without sudo
./bin/install-detect-language.sh --local

# If using local installation, add to your PATH
export PATH="/path/to/vaahai/local/bin:$PATH"
```

After installation, you can use the command as `vaahai detect-language`.

## Usage

### Basic Usage

```bash
# Analyze a single file
vaahai detect-language path/to/file.py

# Analyze a directory (recursively)
vaahai detect-language path/to/directory
```

### Output Formats

The command supports three output formats:

```bash
# Default table format (human-readable)
vaahai detect-language path/to/file.py

# JSON format (machine-readable)
vaahai detect-language path/to/file.py --format json

# Markdown format (for documentation)
vaahai detect-language path/to/file.py --format markdown
```

### Disabling LLM Analysis

By default, the command uses both heuristic detection and LLM-based analysis. You can disable the LLM component:

```bash
vaahai detect-language path/to/file.py --no-llm
```

### Debug Mode

If you encounter issues, you can run the command in debug mode to see more detailed error information:

```bash
vaahai detect-language path/to/file.py --debug
```

## Examples

### Analyzing a Single File

```bash
vaahai detect-language app.py
```

Output:
```
Language Detection Results
Analyzed 1 files

Project Language Distribution:
┏━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ Language ┃ Files ┃ Percentage ┃
┡━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ python   │ 1     │ 100.0%     │
└──────────┴───────┴────────────┘

File Analysis:
┏━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┓
┃ File       ┃ Language ┃ Confidence ┃ Version ┃ Frameworks ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━┩
│ app.py     │ python   │ 95.0%      │ 3.10    │ Flask      │
└────────────┴──────────┴────────────┴─────────┴────────────┘
```

### Analyzing a Project Directory

```bash
vaahai detect-language src/ --format markdown
```

This will generate a markdown report of all languages used in the project.

### JSON Output for Integration

```bash
vaahai detect-language src/ --format json > language-report.json
```

This saves the language detection results in JSON format for further processing or integration with other tools.

## Features

### Smart File Handling

The language detector includes several smart features:

- **Binary file detection**: Automatically skips binary files that can't be analyzed
- **Large file handling**: Skips files over 1MB in directory scans to avoid performance issues
- **Progress reporting**: Shows progress when scanning large directories
- **Detailed error handling**: Provides clear error messages and debugging information

### Language Detection Capabilities

The detector can identify:

- Over 50 programming languages
- Version information for major languages like Python, JavaScript, Java, etc.
- Common frameworks and libraries
- Language distribution across a project

## Integration

The language detection functionality can be integrated into your CI/CD pipeline to:
- Track language usage across your project
- Ensure consistent language versions
- Document technology stack automatically

## Troubleshooting

If you encounter any issues:

1. Make sure you have the latest version of Vaahai installed
2. Check that the file paths are correct and accessible
3. For large projects, consider analyzing specific directories instead of the entire project
4. If you get timeout errors with LLM analysis, try using the `--no-llm` flag
5. If you encounter Typer CLI errors, use the standalone installation method described above
6. Use the `--debug` flag to get more detailed error information
