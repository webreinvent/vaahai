# VaahAI Testing Guide

This document provides guidelines and best practices for testing the VaahAI project.

## Test Structure

The VaahAI test suite is organized as follows:

```
vaahai/test/
├── conftest.py           # Global pytest fixtures
├── data/                 # Test data and fixtures
├── utils/                # Test utilities and helpers
│   ├── base_test.py      # Base test class
│   ├── cli_helpers.py    # CLI testing helpers
│   └── mock_helpers.py   # Mock objects and utilities
├── unit/                 # Unit tests
│   ├── test_cli_utils.py # Tests for CLI utility functions
│   ├── test_help_utils.py # Tests for help formatting utilities
│   └── test_version.py   # Tests for version command
├── integration/          # Integration tests
│   └── test_config_integration.py # Tests for config command
└── cli/                  # Legacy CLI tests (being migrated)
```

## Test Categories

### Unit Tests

Unit tests focus on testing individual components in isolation. They should be fast, independent, and not rely on external services.

Example:
```python
def test_print_success():
    with patch("rich.console.Console.print") as mock_print:
        print_success("Test message")
        mock_print.assert_called_once()
        # Check that the call contains success styling
        assert any("green" in str(arg) for arg in mock_print.call_args[0])
```

### Integration Tests

Integration tests verify that different components work together correctly. They may involve multiple modules but should still avoid external dependencies when possible.

Example:
```python
def test_config_init_creates_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir)
        
        # Run config init with the temporary config path
        with patch.dict(os.environ, {"VAAHAI_CONFIG_DIR": str(config_path)}):
            init_result = self.invoke_cli(["config", "init"])
            assert_command_success(init_result)
        
        # Verify the config directory was created
        assert config_path.exists()
        assert config_path.is_dir()
```

### CLI Tests

CLI tests verify the functionality of the command-line interface. They use the `CliRunner` from Typer to simulate CLI invocations.

Example:
```python
def test_version_command():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "VaahAI version" in result.stdout
```

## Test Utilities

### BaseTest Class

The `BaseTest` class provides common functionality for tests:

```python
from vaahai.test.utils.base_test import BaseTest

class TestMyFeature(BaseTest):
    def test_something(self):
        result = self.invoke_cli(["command", "--option"])
        self.assert_command_success(result, "Expected output")
```

### CLI Helpers

The `cli_helpers` module provides utilities for testing CLI commands:

```python
from vaahai.test.utils.cli_helpers import assert_command_success

def test_my_command():
    result = self.invoke_cli(["my-command", "--option"])
    assert_command_success(result, "Expected output")
```

### Mock Helpers

The `mock_helpers` module provides mock objects and utilities for testing:

```python
from unittest.mock import patch, MagicMock

def test_with_mocks():
    with patch("module.function") as mock_function:
        mock_function.return_value = "mocked result"
        # Test code that uses the mocked function
        pass
```

## Testing Rich Output

When testing Rich-formatted output, focus on verifying function calls rather than exact string matching:

```python
@patch("rich.console.Console.print")
def test_rich_output(mock_print):
    print_panel("Test content", title="Test Title")
    mock_print.assert_called_once()
    # Check that a Panel was created with the right content
    args = mock_print.call_args[0]
    assert isinstance(args[0], Panel)
    assert "Test content" in str(args[0])
```

## Fixtures

Global fixtures are defined in `conftest.py`:

```python
@pytest.fixture
def cli_runner():
    return CliRunner()

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir
```

## Running Tests

Run all tests:

```bash
poetry run pytest
```

Run tests with coverage:

```bash
poetry run pytest --cov=vaahai
```

Run specific test files:

```bash
poetry run pytest vaahai/test/unit/test_cli_utils.py
```

Run tests matching a pattern:

```bash
poetry run pytest -k "config"
```

## Best Practices

1. **Test Independence**: Each test should be independent and not rely on the state from other tests.

2. **Use Fixtures**: Use fixtures for common setup and teardown operations.

3. **Mock External Dependencies**: Use mocks for external services and dependencies.

4. **Test Edge Cases**: Include tests for error conditions and edge cases.

5. **Keep Tests Fast**: Tests should run quickly to encourage frequent testing.

6. **Descriptive Test Names**: Use descriptive test names that explain what is being tested.

7. **Test Coverage**: Aim for high test coverage (at least 80%).

8. **Parameterized Tests**: Use parameterized tests for testing multiple similar cases.

9. **Isolate File System Operations**: Use temporary directories and mock file operations when testing code that interacts with the file system.

10. **Test Rich Output Carefully**: When testing Rich-formatted output, focus on function calls and content rather than exact string matching.

## Adding New Tests

When adding new features, follow these steps:

1. Create unit tests for individual components.
2. Create integration tests for component interactions.
3. Create CLI tests for command-line functionality.
4. Ensure all tests pass before submitting a pull request.

## Current Test Coverage

As of the latest update, the VaahAI test suite has approximately 35% code coverage. Key areas covered include:

- CLI utility functions (console.py)
- Help formatting utilities (help.py)
- Version command
- Config command integration

Areas that need additional test coverage:

- CLI entry point error handling
- Command groups structure
- InquirerPy integration
- Remaining CLI commands

## Test-Driven Development

Consider using Test-Driven Development (TDD) for new features:

1. Write a failing test that defines the expected behavior.
2. Implement the minimum code needed to make the test pass.
3. Refactor the code while keeping the tests passing.
4. Repeat for additional functionality.
