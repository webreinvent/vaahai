# Development Tools

VaahAI uses several development tools to maintain code quality and consistency. This document describes the tools and how to use them.

## Code Quality Tools

The following tools are used to ensure code quality:

### Code Formatting

#### Black

Black is an uncompromising code formatter that formats Python code according to a consistent style.

```bash
# Format all Python files
poetry run black .

# Check formatting without changing files
poetry run black --check .
```

#### isort

isort automatically sorts and formats import statements in Python files.

```bash
# Sort imports in all Python files
poetry run isort .

# Check import sorting without changing files
poetry run isort --check .
```

### Linting

#### Flake8

Flake8 is a code linter that checks Python code for style and syntax errors.

```bash
# Run flake8 on all Python files
poetry run flake8

# Run flake8 on a specific file
poetry run flake8 path/to/file.py
```

## Running Code Quality Tools Manually

You can run all code quality tools manually using Poetry:

```bash
# Run black
poetry run black .

# Run isort
poetry run isort .

# Run flake8
poetry run flake8
```

## Configuration Files

The following configuration files are used to configure the development tools:

- `.flake8` - Flake8 configuration
- `pyproject.toml` - Contains configuration for Black and isort

## Best Practices

1. Run code quality tools before pushing changes
2. Fix all issues reported by the tools
3. Keep configuration files up to date
4. Follow the style guide enforced by the tools

## Continuous Integration

These tools are also run as part of the continuous integration pipeline to ensure that all code meets the project's quality standards before being merged.

## Future Improvements

We plan to enhance our development tools setup with:

1. Additional linting tools for specific use cases
2. Type checking with mypy
3. Security scanning tools
4. Coverage reporting integration
5. Automated dependency updates
