# Vaahai API Specification

## Overview

This document outlines the API specifications for Vaahai, including both internal APIs for component interaction and external APIs for integration with other systems. These specifications define the interfaces, data models, and behaviors that ensure consistent and reliable operation.

## Internal APIs

### Configuration API

The Configuration API provides access to application settings from various components.

#### ConfigManager

```python
class ConfigManager:
    def load(self, config_path: Optional[str] = None) -> None:
        """
        Load configuration from all sources with proper precedence.
        
        Args:
            config_path: Optional path to a specific configuration file
        
        Raises:
            ConfigError: If configuration loading fails
        """
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by its key.
        
        Args:
            key: Dot-notation path to the configuration value
            default: Default value if key is not found
            
        Returns:
            The configuration value or default if not found
        """
        
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Dot-notation path to the configuration value
            value: Value to set
        """
        
    def save(self, config_path: Optional[str] = None) -> None:
        """
        Save current configuration to a file.
        
        Args:
            config_path: Path to save configuration to
            
        Raises:
            ConfigError: If saving fails
        """
```

#### ConfigSchema

```python
class ConfigSchema(BaseModel):
    """Pydantic model defining configuration structure"""
    
    class LLMConfig(BaseModel):
        provider: str = "openai"
        model: str = "gpt-4"
        api_key: Optional[str] = None
        temperature: float = 0.7
        max_tokens: int = 4000
        
    class StaticAnalysisConfig(BaseModel):
        enabled: bool = True
        tools: List[str] = ["pylint", "flake8", "bandit"]
        
    class ReviewConfig(BaseModel):
        depth: str = "standard"  # quick, standard, thorough
        focus: Optional[str] = None  # security, performance, style
        
    class OutputConfig(BaseModel):
        format: str = "terminal"  # terminal, markdown, html
        color: bool = True
        
    llm: LLMConfig = LLMConfig()
    static_analysis: StaticAnalysisConfig = StaticAnalysisConfig()
    review: ReviewConfig = ReviewConfig()
    output: OutputConfig = OutputConfig()
```

### Scanner API

The Scanner API handles file discovery and content extraction.

#### CodeScanner

```python
class CodeScanner:
    def scan(
        self,
        path: str,
        include: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None,
        recursive: bool = True
    ) -> List[FileInfo]:
        """
        Scan a path for code files.
        
        Args:
            path: Path to scan (file or directory)
            include: Patterns to include (e.g., ["*.py"])
            exclude: Patterns to exclude (e.g., ["*_test.py"])
            recursive: Whether to scan directories recursively
            
        Returns:
            List of FileInfo objects for matching files
            
        Raises:
            ScanError: If scanning fails
        """
        
    def detect_language(self, file_path: str) -> str:
        """
        Detect the programming language of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Language identifier (e.g., "python", "javascript")
        """
```

#### FileInfo

```python
class FileInfo:
    """Data class containing file metadata and content"""
    
    path: str
    relative_path: str
    language: str
    size: int
    content: str
    encoding: str
    line_count: int
    
    def get_lines(self, start: int, end: int) -> List[str]:
        """
        Get specific lines from the file.
        
        Args:
            start: Start line (0-indexed)
            end: End line (inclusive)
            
        Returns:
            List of lines
        """
```

### Analyzer API

The Analyzer API handles static analysis tool integration.

#### AnalyzerRegistry

```python
class AnalyzerRegistry:
    def register_analyzer(self, analyzer: Analyzer) -> None:
        """
        Register a static analyzer.
        
        Args:
            analyzer: Analyzer instance to register
        """
        
    def get_analyzer_for_language(self, language: str) -> Analyzer:
        """
        Get an appropriate analyzer for a language.
        
        Args:
            language: Language identifier
            
        Returns:
            Analyzer instance for the language
            
        Raises:
            AnalyzerError: If no analyzer is available for the language
        """
        
    def get_available_analyzers(self) -> List[str]:
        """
        Get a list of available analyzers.
        
        Returns:
            List of analyzer identifiers
        """
```

#### Analyzer

```python
class Analyzer(ABC):
    """Abstract base class for static analyzers"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the analyzer"""
        
    @property
    @abstractmethod
    def supported_languages(self) -> List[str]:
        """Languages supported by this analyzer"""
        
    @abstractmethod
    def analyze(
        self,
        file_path: str,
        config: Optional[Dict[str, Any]] = None
    ) -> List[AnalysisResult]:
        """
        Analyze a file.
        
        Args:
            file_path: Path to the file to analyze
            config: Optional analyzer-specific configuration
            
        Returns:
            List of analysis results
            
        Raises:
            AnalyzerError: If analysis fails
        """
        
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the analyzer is available in the current environment.
        
        Returns:
            True if available, False otherwise
        """
```

#### AnalysisResult

```python
class AnalysisResult:
    """Normalized representation of a static analysis finding"""
    
    tool: str
    file_path: str
    line: int
    column: Optional[int]
    severity: str  # critical, error, warning, info
    code: str
    message: str
    suggestion: Optional[str]
```

### LLM Provider API

The LLM Provider API handles interaction with language model services.

#### LLMProviderFactory

```python
class LLMProviderFactory:
    @staticmethod
    def create(
        provider_name: str,
        **kwargs
    ) -> LLMProvider:
        """
        Create an LLM provider instance.
        
        Args:
            provider_name: Name of the provider (e.g., "openai", "ollama")
            **kwargs: Provider-specific configuration
            
        Returns:
            LLM provider instance
            
        Raises:
            LLMProviderError: If provider creation fails
        """
```

#### LLMProvider

```python
class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the provider"""
        
    @abstractmethod
    def complete(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a completion from the LLM.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Provider-specific parameters
            
        Returns:
            LLM response
            
        Raises:
            LLMProviderError: If completion fails
        """
        
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is available.
        
        Returns:
            True if available, False otherwise
        """
```

#### LLMResponse

```python
class LLMResponse:
    """Normalized representation of an LLM response"""
    
    content: str
    tokens_used: int
    model: str
    provider: str
    metadata: Dict[str, Any]
```

### Orchestration API

The Orchestration API handles the coordination of the review process.

#### AgentOrchestrator

```python
class AgentOrchestrator:
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize the orchestrator.
        
        Args:
            llm_provider: LLM provider to use
        """
        
    def review_code(
        self,
        code: str,
        language: str,
        static_analysis_results: Optional[List[AnalysisResult]] = None,
        review_depth: str = "standard",
        review_focus: Optional[str] = None
    ) -> ReviewResult:
        """
        Review code using LLM.
        
        Args:
            code: Code to review
            language: Programming language
            static_analysis_results: Optional static analysis results
            review_depth: Review depth (quick, standard, thorough)
            review_focus: Optional focus area (security, performance, style)
            
        Returns:
            Review result
            
        Raises:
            OrchestratorError: If review fails
        """
        
    def explain_code(
        self,
        code: str,
        language: str,
        detail_level: str = "standard"
    ) -> ExplanationResult:
        """
        Generate explanation for code.
        
        Args:
            code: Code to explain
            language: Programming language
            detail_level: Level of detail (brief, standard, detailed)
            
        Returns:
            Explanation result
            
        Raises:
            OrchestratorError: If explanation fails
        """
        
    def generate_documentation(
        self,
        code: str,
        language: str,
        docstring_style: str = "google"
    ) -> DocumentationResult:
        """
        Generate documentation for code.
        
        Args:
            code: Code to document
            language: Programming language
            docstring_style: Docstring style (google, numpy, rst)
            
        Returns:
            Documentation result
            
        Raises:
            OrchestratorError: If documentation generation fails
        """
```

#### ReviewResult

```python
class ReviewResult:
    """Structured representation of a code review"""
    
    file_path: str
    language: str
    summary: str
    strengths: List[str]
    issues: List[ReviewIssue]
    suggestions: List[str]
    metrics: Dict[str, Any]
```

#### ReviewIssue

```python
class ReviewIssue:
    """Representation of an issue identified in review"""
    
    file_path: str
    line: int
    column: Optional[int]
    severity: str  # critical, important, minor
    category: str  # bug, security, performance, style
    message: str
    explanation: str
    suggestion: Optional[str]
    source: str  # llm, static_analysis
```

### Formatter API

The Formatter API handles the presentation of review results.

#### FormatterRegistry

```python
class FormatterRegistry:
    def register_formatter(self, formatter: Formatter) -> None:
        """
        Register a formatter.
        
        Args:
            formatter: Formatter instance to register
        """
        
    def get_formatter(self, format_name: str) -> Formatter:
        """
        Get a formatter by name.
        
        Args:
            format_name: Name of the formatter
            
        Returns:
            Formatter instance
            
        Raises:
            FormatterError: If formatter is not found
        """
        
    def get_available_formatters(self) -> List[str]:
        """
        Get a list of available formatters.
        
        Returns:
            List of formatter names
        """
```

#### Formatter

```python
class Formatter(ABC):
    """Abstract base class for formatters"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the formatter"""
        
    @abstractmethod
    def format(
        self,
        review_result: ReviewResult,
        **kwargs
    ) -> FormattedOutput:
        """
        Format a review result.
        
        Args:
            review_result: Review result to format
            **kwargs: Formatter-specific parameters
            
        Returns:
            Formatted output
            
        Raises:
            FormatterError: If formatting fails
        """
```

#### FormattedOutput

```python
class FormattedOutput:
    """Representation of formatted output"""
    
    content: str
    format: str
    metadata: Dict[str, Any]
```

## External APIs

### CLI API

The CLI API defines the command-line interface for Vaahai.

#### Main Command

```
vaahai [OPTIONS] COMMAND [ARGS]...
```

Options:
- `--version`: Show version and exit
- `--help`: Show help message and exit

Commands:
- `review`: Review code with AI assistance
- `analyze`: Run static analysis on code
- `config`: Manage configuration
- `explain`: Generate code explanations
- `document`: Generate code documentation

#### Review Command

```
vaahai review [OPTIONS] PATH
```

Arguments:
- `PATH`: Path to file or directory to review

Options:
- `--depth [quick|standard|thorough]`: Review depth
- `--focus [security|performance|style]`: Review focus
- `--output [terminal|markdown|html]`: Output format
- `--output-file PATH`: Output file path
- `--interactive`: Enable interactive fix application
- `--include TEXT`: Patterns to include (can be used multiple times)
- `--exclude TEXT`: Patterns to exclude (can be used multiple times)
- `--config PATH`: Path to configuration file
- `--save-history`: Save review results to history
- `--private`: Use only local resources
- `--help`: Show help message and exit

#### Analyze Command

```
vaahai analyze [OPTIONS] PATH
```

Arguments:
- `PATH`: Path to file or directory to analyze

Options:
- `--tool TEXT`: Static analysis tool to use (can be used multiple times)
- `--output [terminal|markdown|html]`: Output format
- `--output-file PATH`: Output file path
- `--include TEXT`: Patterns to include (can be used multiple times)
- `--exclude TEXT`: Patterns to exclude (can be used multiple times)
- `--config PATH`: Path to configuration file
- `--help`: Show help message and exit

#### Config Command

```
vaahai config [OPTIONS] COMMAND [ARGS]...
```

Commands:
- `get`: Get a configuration value
- `set`: Set a configuration value
- `list`: List all configuration values
- `init`: Initialize configuration file

Options:
- `--help`: Show help message and exit

### Python API

The Python API allows programmatic use of Vaahai.

#### Vaahai Client

```python
from vaahai import VaahaiClient

# Initialize client
client = VaahaiClient()

# Review code
result = client.review_code(
    code="def example(): pass",
    language="python",
    review_depth="standard"
)

# Print results
print(result.summary)
for issue in result.issues:
    print(f"{issue.severity}: {issue.message}")

# Review file
file_result = client.review_file("path/to/file.py")

# Review directory
dir_results = client.review_directory(
    "path/to/directory",
    include=["*.py"],
    exclude=["*_test.py"]
)

# Run static analysis
analysis_results = client.analyze_file("path/to/file.py")

# Generate explanation
explanation = client.explain_code(
    code="def complex_function(): pass",
    language="python"
)

# Generate documentation
documentation = client.generate_documentation(
    code="def undocumented_function(): pass",
    language="python",
    docstring_style="google"
)
```

### Integration API

The Integration API allows integration with other development tools.

#### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/webreinvent/vaahai-pre-commit
    rev: v1.0.0
    hooks:
      - id: vaahai-review
        args: [--depth=quick, --focus=security]
```

#### GitHub Action

```yaml
# .github/workflows/vaahai-review.yml
name: Vaahai Code Review

on:
  pull_request:
    branches: [ main ]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install vaahai
      - name: Run Vaahai review
        run: |
          vaahai review . --output markdown --output-file review.md
        env:
          VAAHAI_LLM_OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      - name: Comment PR
        uses: actions/github-script@v5
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

## Data Models

### Configuration Model

```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-4",
    "api_key": null,
    "temperature": 0.7,
    "max_tokens": 4000
  },
  "static_analysis": {
    "enabled": true,
    "tools": ["pylint", "flake8", "bandit"]
  },
  "review": {
    "depth": "standard",
    "focus": null
  },
  "output": {
    "format": "terminal",
    "color": true
  }
}
```

### Review Result Model

```json
{
  "file_path": "path/to/file.py",
  "language": "python",
  "summary": "Overall good quality code with some minor issues.",
  "strengths": [
    "Good function naming",
    "Consistent style",
    "Comprehensive error handling"
  ],
  "issues": [
    {
      "file_path": "path/to/file.py",
      "line": 42,
      "column": 10,
      "severity": "important",
      "category": "security",
      "message": "Potential SQL injection vulnerability",
      "explanation": "User input is directly concatenated into SQL query.",
      "suggestion": "Use parameterized queries instead of string concatenation.",
      "source": "llm"
    }
  ],
  "suggestions": [
    "Consider adding type hints for better IDE support",
    "Add more comprehensive docstrings"
  ],
  "metrics": {
    "issue_count": 5,
    "critical_issues": 0,
    "important_issues": 2,
    "minor_issues": 3
  }
}
```

### Analysis Result Model

```json
{
  "tool": "pylint",
  "file_path": "path/to/file.py",
  "line": 42,
  "column": 10,
  "severity": "error",
  "code": "E1102",
  "message": "not-callable: X is not callable",
  "suggestion": "Ensure X is a callable object or function."
}
```

## Error Handling

### Error Hierarchy

```
VaahaiError
├── ConfigError
│   ├── ConfigLoadError
│   ├── ConfigValidationError
│   └── ConfigSaveError
├── ScanError
│   ├── FileNotFoundError
│   ├── PermissionError
│   └── EncodingError
├── AnalyzerError
│   ├── AnalyzerNotFoundError
│   ├── AnalyzerExecutionError
│   └── AnalyzerParseError
├── LLMProviderError
│   ├── AuthenticationError
│   ├── RateLimitError
│   ├── TokenLimitError
│   └── ServiceUnavailableError
├── OrchestratorError
│   ├── PromptGenerationError
│   ├── ResponseParsingError
│   └── ReviewGenerationError
└── FormatterError
    ├── FormatterNotFoundError
    └── OutputGenerationError
```

### Error Response Format

```json
{
  "error": {
    "type": "LLMProviderError",
    "code": "authentication_error",
    "message": "Invalid API key provided",
    "details": {
      "provider": "openai",
      "status_code": 401
    },
    "suggestion": "Check your API key or environment variables"
  }
}
```

## Authentication and Security

### API Key Management

API keys for LLM providers are managed securely:

1. Keys can be provided via environment variables (preferred)
   ```
   VAAHAI_LLM_OPENAI_API_KEY=sk-...
   ```

2. Keys can be stored in user configuration
   ```toml
   # ~/.config/vaahai/config.toml
   [llm.openai]
   api_key = "sk-..."
   ```

3. Keys can be provided via command line (not recommended)
   ```
   vaahai review --llm-api-key "sk-..." path/to/file.py
   ```

### Data Privacy

1. Code is only sent to external services when using remote LLM providers
2. No data is persistently stored by default
3. Privacy mode (`--private`) ensures all processing is done locally
4. Clear documentation of data handling practices

## Versioning and Compatibility

### API Versioning

The Python API follows semantic versioning:

- Major version changes indicate breaking API changes
- Minor version changes indicate new features with backward compatibility
- Patch version changes indicate bug fixes and minor improvements

### CLI Compatibility

CLI commands maintain backward compatibility within major versions:

- New options are added in a backward-compatible way
- Deprecated options are marked as such before removal
- Breaking changes are clearly documented in release notes

## Rate Limiting and Quotas

### LLM Provider Rate Limiting

1. Automatic handling of rate limits with exponential backoff
2. Configurable retry behavior
3. Clear error messages for quota exhaustion
4. Token usage tracking and reporting

### Local Resource Management

1. Configurable parallelism for CPU-intensive operations
2. Memory usage limits for large file processing
3. Disk space management for temporary files and history

## Conclusion

This API specification provides a comprehensive reference for developers implementing and integrating with Vaahai. It defines the interfaces, data models, and behaviors that ensure consistent and reliable operation across components and external integrations.
