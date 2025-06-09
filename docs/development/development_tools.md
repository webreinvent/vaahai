# Development Tools

This document describes the development tools used in the VaahAI project and how to set them up.

## Code Quality Tools

VaahAI uses several tools to ensure code quality:

### Pre-commit Hooks

Pre-commit hooks run automatically before each commit to ensure code quality standards are met.

To install pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install
```

To run pre-commit manually on all files:

```bash
pre-commit run --all-files
```

### Code Formatting

VaahAI uses the following code formatters:

1. **Black** - Python code formatter that enforces a consistent style
2. **isort** - Import statement organizer that sorts imports alphabetically and separates them into sections

Configuration for these tools is in `pyproject.toml`.

### Linting

VaahAI uses Flake8 for linting Python code. Flake8 checks for:

- PEP 8 style guide violations
- Programming errors
- Code complexity issues

Configuration is in `.flake8`.

## Running the Tools

### Black

To format code with Black:

```bash
# Format a specific file
black path/to/file.py

# Format all Python files
black .
```

### isort

To sort imports with isort:

```bash
# Sort imports in a specific file
isort path/to/file.py

# Sort imports in all Python files
isort .
```

### Flake8

To check code with Flake8:

```bash
# Check a specific file
flake8 path/to/file.py

# Check all Python files
flake8
```

## Integration with Pre-commit

All these tools are configured to run automatically via pre-commit hooks before each commit. If any tool reports issues, the commit will be blocked until the issues are fixed.

## Configuration Files

- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `pyproject.toml` - Black and isort configuration
- `.flake8` - Flake8 configuration

## Best Practices

1. Always run pre-commit hooks before pushing changes
2. Fix all linting and formatting issues before submitting a pull request
3. Keep configuration files in sync with project requirements
4. Update tool versions periodically to benefit from improvements

## Code Quality Improvement Plan

The project has a phased approach to improving code quality. See the [Code Quality Improvement Plan](code_quality_improvement.md) for details on how we're gradually enhancing code quality across the codebase.
