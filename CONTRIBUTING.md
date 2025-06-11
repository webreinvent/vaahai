# Contributing to VaahAI

Thank you for your interest in contributing to VaahAI! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Workflow](#development-workflow)
- [Branching Strategy](#branching-strategy)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please be kind and courteous to others, and avoid any form of harassment or discriminatory behavior.

## Development Workflow

We follow an incremental development approach with small, achievable tasks to enable frequent releases and clear progress tracking.

### Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/vaahai.git
   cd vaahai
   ```
3. Set up the upstream remote:
   ```bash
   git remote add upstream https://github.com/webreinvent/vaahai.git
   ```
4. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
5. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Development Cycle

1. Verify previous task completion with appropriate tests
2. Update relevant documentation in `/specs`, `/docs`, and `/ai_docs`
3. Create a git commit with a clear message including task IDs
4. Create a merge/pull request to the `develop` branch
5. Select the next task from `task_tracking.md`
6. Create a new branch for the task
7. Implement the task with proper testing
8. Submit your changes for review

## Branching Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- Feature branches: Created from `develop` or previous task branches

### Branch Naming Convention

Use the following format for branch names:

```
feature/P<phase>-task-<task-id>-<short-description>
```

Example: `feature/P1-task-2.1-autogen-research`

## Pull Request Process

1. Create a pull request from your feature branch to the `develop` branch
2. Include a descriptive title that references the task ID
3. Add a detailed description of the changes made
4. Reference related issues or tasks
5. Request appropriate reviewers
6. Add relevant labels and milestones
7. Ensure all tests pass and documentation is updated
8. Address review comments promptly

## Coding Standards

We follow standard Python coding conventions with some project-specific guidelines:

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use 4 spaces for indentation (no tabs)
- Maximum line length of 88 characters (following Black defaults)
- Use docstrings for all public modules, functions, classes, and methods
- Use type hints for function parameters and return values

### Code Formatting

We use the following tools for code formatting and linting:

- [Black](https://black.readthedocs.io/) for code formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [flake8](https://flake8.pycqa.org/) for linting

Run the following commands before committing:

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8
```

## Testing Guidelines

- Write tests for all new functionality
- Maintain or improve code coverage with each contribution
- Tests should be placed in the `tests/` directory
- Use pytest for running tests

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=vaahai
```

## Documentation

- Update documentation for any feature, API change, or bug fix
- Follow the existing documentation style
- Documentation should be clear, concise, and include examples
- Update the following as needed:
  - Code docstrings
  - `/specs` for technical specifications
  - `/docs` for user and developer documentation
  - `/ai_docs` for AI-specific documentation

## Issue Reporting

When reporting issues, please include:

1. A clear and descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Environment information (OS, Python version, etc.)
6. Any relevant logs or error messages

Use issue templates when available.

---

Thank you for contributing to VaahAI! Your efforts help make this project better for everyone.
