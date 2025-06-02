# Vaahai API Reference for AI Tools

This document provides a comprehensive API reference for the Vaahai AI-augmented code review CLI tool, specifically formatted for AI tools to understand the interfaces, methods, and data structures used throughout the system.

## Core APIs

### Command Line Interface

#### Entry Point

```python
# vaahai/__main__.py
app = typer.Typer(
    name="vaahai",
    help="AI-augmented code review CLI tool",
    add_completion=False,
)

def main() -> None:
    """Main entry point for the CLI."""
    app()

if __name__ == "__main__":
    main()
```

#### Command Registration

```python
# vaahai/__main__.py
# Register commands directly on the main app
app.callback()(version_callback)
app.command()(review)  # Direct review command that takes a path argument
app.add_typer(analyze_app, name="analyze", help="Run static analysis on code files")
app.add_typer(config_app, name="config", help="Manage configuration")
app.add_typer(explain_app, name="explain", help="Explain code using LLM")
app.add_typer(document_app, name="document", help="Generate documentation for code")
```

#### Command Implementation

```python
# vaahai/__main__.py
def review(
    paths: List[str] = typer.Argument(..., help="Path to file(s) or directory to review"),
    depth: ReviewDepth = typer.Option(ReviewDepth.STANDARD, help="Review depth"),
    focus: ReviewFocus = typer.Option(ReviewFocus.ALL, help="Focus area for review"),
    output_format: OutputFormat = typer.Option(OutputFormat.TERMINAL, help="Output format"),
    include: Optional[List[str]] = typer.Option(None, help="Patterns to include"),
    exclude: Optional[List[str]] = typer.Option(None, help="Patterns to exclude"),
    max_size: Optional[int] = typer.Option(None, help="Maximum file size in KB"),
    verbosity: VerbosityLevel = typer.Option(VerbosityLevel.NORMAL, help="Verbosity level"),
) -> None:
    """Review code files using static analysis and LLM-powered contextual review."""
    # Implementation details...
```

### Configuration Management

#### ConfigManager Interface

```python
# vaahai/core/config.py
class ConfigManager:
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the configuration manager.
        
        Args:
            config_path: Optional path to configuration file. If None, default locations are used.
        """
        # Implementation details...
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: The configuration key (dot-separated for nested keys)
            default: Default value if key is not found
            
        Returns:
            The configuration value or default
        """
        # Implementation details...
    
    def set(self, key: str, value: Any, scope: ConfigScope = ConfigScope.GLOBAL) -> None:
        """Set a configuration value.
        
        Args:
            key: The configuration key (dot-separated for nested keys)
            value: The value to set
            scope: The configuration scope (global or project)
        """
        # Implementation details...
    
    def reset(self, key: Optional[str] = None, scope: ConfigScope = ConfigScope.GLOBAL) -> None:
        """Reset configuration to default values.
        
        Args:
            key: The configuration key to reset, or None to reset all
            scope: The configuration scope (global or project)
        """
        # Implementation details...
    
    def list(self, section: Optional[str] = None) -> Dict[str, Any]:
        """List configuration values.
        
        Args:
            section: Optional section to list, or None for all
            
        Returns:
            Dictionary of configuration values
        """
        # Implementation details...
```

### Orchestration

#### Orchestrator Interface

```python
# vaahai/core/orchestrator.py
class Orchestrator:
    def __init__(self, config_manager: ConfigManager):
        """Initialize the orchestrator.
        
        Args:
            config_manager: Configuration manager instance
        """
        # Implementation details...
    
    def review(self, paths: List[str], options: ReviewOptions) -> List[ReviewResult]:
        """Review code files.
        
        Args:
            paths: List of file or directory paths to review
            options: Review options
            
        Returns:
            List of review results
        """
        # Implementation details...
    
    def analyze(self, paths: List[str], options: AnalysisOptions) -> List[AnalysisResult]:
        """Run static analysis on code files.
        
        Args:
            paths: List of file or directory paths to analyze
            options: Analysis options
            
        Returns:
            List of analysis results
        """
        # Implementation details...
    
    def apply_fixes(self, file_path: str, fixes: List[Fix], options: FixOptions) -> FixResult:
        """Apply fixes to code files.
        
        Args:
            file_path: Path to file to fix
            fixes: List of fixes to apply
            options: Fix application options
            
        Returns:
            Result of fix application
        """
        # Implementation details...
```

## Static Analysis APIs

### Analyzer Interface

```python
# vaahai/analyzers/base.py
class Analyzer(ABC):
    @abstractmethod
    def analyze(self, file_path: str, options: AnalysisOptions) -> AnalysisResult:
        """Analyze a code file.
        
        Args:
            file_path: Path to file to analyze
            options: Analysis options
            
        Returns:
            Analysis result
        """
        pass
    
    @abstractmethod
    def supports_file(self, file_path: str) -> bool:
        """Check if the analyzer supports the given file.
        
        Args:
            file_path: Path to file to check
            
        Returns:
            True if the analyzer supports the file, False otherwise
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the analyzer.
        
        Returns:
            Analyzer name
        """
        pass
```

### Analyzer Factory

```python
# vaahai/analyzers/factory.py
class AnalyzerFactory:
    @staticmethod
    def create_analyzer(analyzer_name: str, config_manager: ConfigManager) -> Analyzer:
        """Create an analyzer instance.
        
        Args:
            analyzer_name: Name of the analyzer to create
            config_manager: Configuration manager instance
            
        Returns:
            Analyzer instance
            
        Raises:
            ValueError: If analyzer is not found
        """
        # Implementation details...
    
    @staticmethod
    def get_analyzers_for_file(file_path: str, config_manager: ConfigManager) -> List[Analyzer]:
        """Get analyzers that support the given file.
        
        Args:
            file_path: Path to file
            config_manager: Configuration manager instance
            
        Returns:
            List of analyzer instances that support the file
        """
        # Implementation details...
```

## LLM Integration APIs

### LLMProvider Interface

```python
# vaahai/llm/base.py
class LLMProvider(ABC):
    @abstractmethod
    def review(
        self, 
        code: str, 
        analysis_results: List[AnalysisResult], 
        options: LLMOptions
    ) -> ReviewFeedback:
        """Review code using LLM.
        
        Args:
            code: Code to review
            analysis_results: Static analysis results
            options: LLM options
            
        Returns:
            Review feedback from LLM
        """
        pass
    
    @abstractmethod
    def explain(
        self, 
        code: str, 
        options: ExplainOptions
    ) -> str:
        """Explain code using LLM.
        
        Args:
            code: Code to explain
            options: Explanation options
            
        Returns:
            Explanation from LLM
        """
        pass
    
    @abstractmethod
    def compare(
        self, 
        old_code: str, 
        new_code: str, 
        options: CompareOptions
    ) -> str:
        """Compare two versions of code using LLM.
        
        Args:
            old_code: Old version of code
            new_code: New version of code
            options: Comparison options
            
        Returns:
            Comparison from LLM
        """
        pass
```

### LLMProvider Factory

```python
# vaahai/llm/factory.py
class LLMProviderFactory:
    @staticmethod
    def create_provider(provider_name: str, config_manager: ConfigManager) -> LLMProvider:
        """Create an LLM provider instance.
        
        Args:
            provider_name: Name of the provider to create
            config_manager: Configuration manager instance
            
        Returns:
            LLM provider instance
            
        Raises:
            ValueError: If provider is not found
        """
        # Implementation details...
```

### Prompt Template Manager

```python
# vaahai/llm/prompts/manager.py
class PromptTemplateManager:
    def __init__(self, config_manager: ConfigManager):
        """Initialize the prompt template manager.
        
        Args:
            config_manager: Configuration manager instance
        """
        # Implementation details...
    
    def get_template(self, template_name: str) -> str:
        """Get a prompt template.
        
        Args:
            template_name: Name of the template to get
            
        Returns:
            Template string
            
        Raises:
            ValueError: If template is not found
        """
        # Implementation details...
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a prompt template with context.
        
        Args:
            template_name: Name of the template to render
            context: Context variables for rendering
            
        Returns:
            Rendered template
            
        Raises:
            ValueError: If template is not found
        """
        # Implementation details...
```

## Output Formatting APIs

### Formatter Interface

```python
# vaahai/formatters/base.py
class Formatter(ABC):
    @abstractmethod
    def format_review_result(self, result: ReviewResult) -> str:
        """Format a review result.
        
        Args:
            result: Review result to format
            
        Returns:
            Formatted result
        """
        pass
    
    @abstractmethod
    def format_analysis_result(self, result: AnalysisResult) -> str:
        """Format an analysis result.
        
        Args:
            result: Analysis result to format
            
        Returns:
            Formatted result
        """
        pass
    
    @abstractmethod
    def format_fix_result(self, result: FixResult) -> str:
        """Format a fix result.
        
        Args:
            result: Fix result to format
            
        Returns:
            Formatted result
        """
        pass
```

### Formatter Factory

```python
# vaahai/formatters/factory.py
class FormatterFactory:
    @staticmethod
    def create_formatter(format_name: str, config_manager: ConfigManager) -> Formatter:
        """Create a formatter instance.
        
        Args:
            format_name: Name of the format to create
            config_manager: Configuration manager instance
            
        Returns:
            Formatter instance
            
        Raises:
            ValueError: If formatter is not found
        """
        # Implementation details...
```

## Fix Application APIs

### FixApplier Interface

```python
# vaahai/fixes/applier.py
class FixApplier:
    def __init__(self, config_manager: ConfigManager):
        """Initialize the fix applier.
        
        Args:
            config_manager: Configuration manager instance
        """
        # Implementation details...
    
    def apply_fixes(
        self, 
        file_path: str, 
        fixes: List[Fix], 
        options: FixOptions
    ) -> FixResult:
        """Apply fixes to a file.
        
        Args:
            file_path: Path to file to fix
            fixes: List of fixes to apply
            options: Fix application options
            
        Returns:
            Result of fix application
        """
        # Implementation details...
    
    def generate_patches(
        self, 
        file_path: str, 
        fixes: List[Fix], 
        options: PatchOptions
    ) -> List[str]:
        """Generate patch files for fixes.
        
        Args:
            file_path: Path to file to fix
            fixes: List of fixes to generate patches for
            options: Patch generation options
            
        Returns:
            List of paths to generated patch files
        """
        # Implementation details...
```

### InteractiveFixApplier Interface

```python
# vaahai/fixes/interactive.py
class InteractiveFixApplier(FixApplier):
    def apply_fixes(
        self, 
        file_path: str, 
        fixes: List[Fix], 
        options: FixOptions
    ) -> FixResult:
        """Apply fixes to a file interactively.
        
        Args:
            file_path: Path to file to fix
            fixes: List of fixes to apply
            options: Fix application options
            
        Returns:
            Result of fix application
        """
        # Implementation details...
```

## Data Structures

### Review Data Structures

```python
# vaahai/models/review.py
class ReviewOptions(BaseModel):
    """Options for code review."""
    depth: ReviewDepth = ReviewDepth.STANDARD
    llm_provider: Optional[str] = None
    model: Optional[str] = None
    analyzers: Optional[List[str]] = None
    ignore: Optional[List[str]] = None
    include_related: bool = False
    context: Optional[str] = None
    apply_fixes: bool = False
    auto_apply_safe: bool = False
    generate_patches: bool = False
    focus: ReviewFocus = ReviewFocus.GENERAL
    diff: bool = False
    ci: bool = False
    exit_code: bool = False
    template: Optional[Path] = None
    output: Optional[Path] = None
    format: OutputFormat = OutputFormat.TERMINAL

class ReviewResult(BaseModel):
    """Result of a code review."""
    file_path: str
    analysis_results: List[AnalysisResult]
    llm_feedback: Optional[ReviewFeedback] = None
    fixes: List[Fix] = []
```

### Analysis Data Structures

```python
# vaahai/models/analysis.py
class IssueSeverity(str, Enum):
    """Severity of an issue."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class Issue(BaseModel):
    """An issue found during analysis."""
    code: str
    message: str
    line: int
    column: int
    severity: IssueSeverity
    file_path: str

class AnalysisOptions(BaseModel):
    """Options for static analysis."""
    analyzers: Optional[List[str]] = None
    ignore: Optional[List[str]] = None
    fix: bool = False
    ci: bool = False
    exit_code: bool = False

class AnalysisResult(BaseModel):
    """Result of static analysis."""
    issues: List[Issue] = []
    metrics: Dict[str, Any] = {}
    tool_name: str
    file_path: str
```

### LLM Data Structures

```python
# vaahai/models/llm.py
class ReviewFeedback(BaseModel):
    """Feedback from LLM review."""
    summary: str
    strengths: List[str] = []
    issues: List[ReviewIssue] = []
    recommendations: List[str] = []

class ReviewIssue(BaseModel):
    """An issue found during LLM review."""
    description: str
    severity: IssueSeverity
    line: Optional[int] = None
    code: Optional[str] = None
    suggested_fix: Optional[str] = None

class LLMOptions(BaseModel):
    """Options for LLM processing."""
    provider: str
    model: str
    temperature: float = 0.3
    max_tokens: Optional[int] = None
    context: Optional[str] = None
    focus: ReviewFocus = ReviewFocus.GENERAL
    template: Optional[str] = None
```

### Fix Data Structures

```python
# vaahai/models/fix.py
class Fix(BaseModel):
    """A fix for an issue."""
    description: str
    file_path: str
    line_start: int
    line_end: int
    original_code: str
    fixed_code: str
    severity: IssueSeverity
    is_safe: bool = False

class FixOptions(BaseModel):
    """Options for fix application."""
    interactive: bool = True
    auto_apply_safe: bool = False
    backup: bool = True

class FixResult(BaseModel):
    """Result of fix application."""
    file_path: str
    applied_fixes: List[Fix] = []
    skipped_fixes: List[Fix] = []
    failed_fixes: List[Tuple[Fix, str]] = []
    backup_path: Optional[str] = None
```

## Enums and Constants

```python
# vaahai/models/enums.py
class ReviewDepth(str, Enum):
    """Depth of code review."""
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"

class ReviewFocus(str, Enum):
    """Focus area for code review."""
    GENERAL = "general"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"

class OutputFormat(str, Enum):
    """Output format for results."""
    TERMINAL = "terminal"
    MARKDOWN = "markdown"
    HTML = "html"

class ConfigScope(str, Enum):
    """Scope of configuration."""
    GLOBAL = "global"
    PROJECT = "project"
    DEFAULT = "default"
```

## Error Handling

```python
# vaahai/exceptions.py
class VaahaiError(Exception):
    """Base exception for all Vaahai errors."""
    pass

class ConfigError(VaahaiError):
    """Error related to configuration."""
    pass

class AnalysisError(VaahaiError):
    """Error related to static analysis."""
    pass

class LLMError(VaahaiError):
    """Error related to LLM processing."""
    pass

class FixError(VaahaiError):
    """Error related to fix application."""
    pass

class InputError(VaahaiError):
    """Error related to user input."""
    pass
```

## Utility Functions

```python
# vaahai/utils/file.py
def is_supported_file(file_path: str, patterns: List[str]) -> bool:
    """Check if a file is supported based on patterns.
    
    Args:
        file_path: Path to file to check
        patterns: List of glob patterns to match
        
    Returns:
        True if the file is supported, False otherwise
    """
    # Implementation details...

def scan_directory(
    directory_path: str, 
    patterns: List[str], 
    recursive: bool = True, 
    max_depth: Optional[int] = None
) -> List[str]:
    """Scan a directory for files matching patterns.
    
    Args:
        directory_path: Path to directory to scan
        patterns: List of glob patterns to match
        recursive: Whether to scan recursively
        max_depth: Maximum recursion depth
        
    Returns:
        List of file paths matching patterns
    """
    # Implementation details...

def read_file(file_path: str) -> str:
    """Read a file.
    
    Args:
        file_path: Path to file to read
        
    Returns:
        File contents
        
    Raises:
        IOError: If file cannot be read
    """
    # Implementation details...

def write_file(file_path: str, content: str, backup: bool = False) -> Optional[str]:
    """Write to a file.
    
    Args:
        file_path: Path to file to write
        content: Content to write
        backup: Whether to create a backup
        
    Returns:
        Path to backup file if backup=True, None otherwise
        
    Raises:
        IOError: If file cannot be written
    """
    # Implementation details...
```

## Plugin System

```python
# vaahai/plugins/registry.py
class PluginRegistry:
    @staticmethod
    def register_plugin(plugin_class: Type[Any], plugin_type: str) -> None:
        """Register a plugin.
        
        Args:
            plugin_class: Plugin class to register
            plugin_type: Type of plugin (analyzer, formatter, etc.)
        """
        # Implementation details...
    
    @staticmethod
    def get_plugins(plugin_type: str) -> List[Type[Any]]:
        """Get registered plugins of a specific type.
        
        Args:
            plugin_type: Type of plugins to get
            
        Returns:
            List of plugin classes
        """
        # Implementation details...
```

## Integration Examples

### Complete Review Workflow

```python
# Example of a complete review workflow
def review_workflow(paths: List[str], options: ReviewOptions) -> None:
    # Initialize components
    config_manager = ConfigManager()
    orchestrator = Orchestrator(config_manager)
    
    # Override config with options
    if options.llm_provider:
        config_manager.set("llm.provider", options.llm_provider, scope=ConfigScope.DEFAULT)
    if options.model:
        config_manager.set("llm.model", options.model, scope=ConfigScope.DEFAULT)
    
    # Perform review
    results = orchestrator.review(paths, options)
    
    # Format results
    formatter_factory = FormatterFactory()
    formatter = formatter_factory.create_formatter(options.format, config_manager)
    formatted_results = [formatter.format_review_result(result) for result in results]
    
    # Output results
    if options.output:
        for i, result in enumerate(formatted_results):
            output_path = options.output
            if len(formatted_results) > 1:
                # Add index for multiple results
                name, ext = os.path.splitext(str(output_path))
                output_path = Path(f"{name}_{i}{ext}")
            with open(output_path, "w") as f:
                f.write(result)
    else:
        for result in formatted_results:
            print(result)
    
    # Apply fixes if requested
    if options.apply_fixes and any(result.fixes for result in results):
        fix_applier = InteractiveFixApplier(config_manager) if not options.ci else FixApplier(config_manager)
        fix_options = FixOptions(
            interactive=not options.ci,
            auto_apply_safe=options.auto_apply_safe,
            backup=True
        )
        
        for result in results:
            if result.fixes:
                fix_result = fix_applier.apply_fixes(result.file_path, result.fixes, fix_options)
                print(formatter.format_fix_result(fix_result))
    
    # Return exit code if requested
    if options.exit_code and any(
        result.analysis_results and any(
            issue.severity in [IssueSeverity.CRITICAL, IssueSeverity.HIGH]
            for ar in result.analysis_results
            for issue in ar.issues
        )
        for result in results
    ):
        sys.exit(5)
