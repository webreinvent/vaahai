# Vaahai Testing Strategy

This document outlines the comprehensive testing approach for the Vaahai project, covering all levels from unit tests to end-to-end integration.

## Testing Levels

### Unit Testing

Unit tests focus on testing individual components in isolation, with dependencies mocked or stubbed.

**Key Areas:**
- Individual agent functionality
- Command handlers
- Configuration management
- Utility functions
- LLM provider adapters

**Tools:**
- pytest for test execution
- unittest.mock for mocking dependencies
- pytest-cov for coverage reporting

**Example Unit Test:**

```python
def test_language_detector_python_file(mocker):
    # Arrange
    mock_config = mocker.Mock()
    detector = LanguageDetectorAgent(config=mock_config)
    
    # Mock file content
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="def hello_world(): print('Hello World')"))
    mocker.patch("os.path.exists", return_value=True)
    
    # Act
    result = detector.detect_file("test.py")
    
    # Assert
    assert result["language"] == "python"
    assert result["confidence"] >= 0.9
```

### Integration Testing

Integration tests verify that components work together correctly.

**Key Areas:**
- Agent collaboration
- Command execution flow
- Configuration loading and application
- LLM integration

**Tools:**
- pytest for test execution
- VCR.py for recording and replaying API responses
- docker-compose for testing Docker integration

**Example Integration Test:**

```python
def test_review_command_integration(mocker):
    # Arrange
    config = ConfigManager()
    config.set("llm.provider", "mock")
    
    # Mock LLM responses
    mock_llm = mocker.patch("vaahai.llm.MockProvider")
    mock_llm.return_value.generate.return_value = "This code looks good but could use better error handling."
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w+") as temp:
        temp.write("def test(): return 42")
        temp.flush()
        
        # Act
        cmd = ReviewCommand(config=config)
        result = cmd.execute(path=temp.name, output_format="terminal")
        
    # Assert
    assert result.success
    assert "error handling" in result.data["review"]
```

### End-to-End Testing

End-to-end tests verify the entire system works as expected from the user's perspective.

**Key Areas:**
- CLI command execution
- Full workflow execution
- Output formatting
- Error handling

**Tools:**
- pytest for test execution
- typer.testing for CLI testing
- docker-compose for testing Docker integration

**Example End-to-End Test:**

```python
from typer.testing import CliRunner
from vaahai.__main__ import app

def test_review_command_e2e():
    # Arrange
    runner = CliRunner()
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w+") as temp:
        temp.write("def test(): return 42")
        temp.flush()
        
        # Act
        result = runner.invoke(app, ["review", temp.name, "--output", "terminal"])
        
    # Assert
    assert result.exit_code == 0
    assert "Review completed" in result.stdout
```

## Testing Strategies

### Mock LLM Testing

To avoid excessive API calls during testing, we use a mock LLM provider that returns predefined responses.

```python
class MockLLMProvider:
    def __init__(self, config):
        self.config = config
        self.responses = {
            "language_detection": "The language is Python 3.8+",
            "framework_detection": "This appears to be a Django project",
            "code_review": "The code has 3 issues: 1. Missing error handling...",
        }
    
    def generate(self, prompt, context=None):
        # Return appropriate mock response based on prompt content
        if "language" in prompt.lower():
            return self.responses["language_detection"]
        elif "framework" in prompt.lower():
            return self.responses["framework_detection"]
        else:
            return self.responses["code_review"]
```

### Snapshot Testing

For testing output formatting, we use snapshot testing to compare generated output with expected output.

```python
def test_markdown_formatter_snapshot(snapshot):
    # Arrange
    formatter = MarkdownFormatter()
    data = {
        "file": "test.py",
        "issues": [
            {"severity": "high", "description": "Missing error handling"},
            {"severity": "medium", "description": "Function too complex"}
        ]
    }
    
    # Act
    result = formatter.format(data)
    
    # Assert
    snapshot.assert_match(result, "markdown_output.md")
```

### Parameterized Testing

For testing components with multiple configurations or inputs, we use parameterized testing.

```python
@pytest.mark.parametrize("file_extension,expected_language", [
    (".py", "python"),
    (".js", "javascript"),
    (".rb", "ruby"),
    (".go", "go"),
    (".java", "java"),
])
def test_language_detection_by_extension(file_extension, expected_language, mocker):
    # Arrange
    detector = LanguageDetectorAgent(config=mocker.Mock())
    
    # Act
    result = detector.detect_file(f"test{file_extension}")
    
    # Assert
    assert result["language"] == expected_language
```

### Property-Based Testing

For testing components with complex input spaces, we use property-based testing.

```python
@given(st.text(min_size=1), st.integers(min_value=1, max_value=100))
def test_file_scanner_properties(path, max_size):
    # Arrange
    scanner = FileScanner(max_size_mb=max_size)
    
    # Act & Assert
    try:
        result = scanner.scan(path)
        if result.success:
            assert all(file["size_bytes"] <= max_size * 1024 * 1024 for file in result.files)
    except FileNotFoundError:
        pass  # Expected for random paths
```

## Test Coverage Goals

| Component | Coverage Target |
|-----------|----------------|
| Core utilities | 95% |
| Configuration | 90% |
| Agents | 85% |
| Commands | 85% |
| LLM integration | 80% |
| CLI interface | 80% |

## Continuous Integration

Tests are run automatically on:
- Every push to the main branch
- Every pull request
- Scheduled nightly builds

The CI pipeline includes:
1. Linting with flake8
2. Type checking with mypy
3. Unit tests
4. Integration tests
5. Coverage reporting
6. End-to-end tests

## Test Data Management

Test data is managed through:
1. Fixtures for common test data
2. Factory methods for generating test objects
3. VCR cassettes for API responses
4. Snapshot files for output comparison

## Mocking Strategy

External dependencies are mocked using:
1. unittest.mock for Python standard library
2. pytest-mock for pytest integration
3. VCR.py for HTTP requests
4. Custom mock implementations for LLM providers

## Test Environment

Tests are run in:
1. Local development environment
2. CI environment (GitHub Actions)
3. Docker containers for isolation

## Test Documentation

Each test should include:
1. Clear description of what is being tested
2. Arrange-Act-Assert pattern
3. Comments explaining complex test logic
4. References to requirements or issues being verified
