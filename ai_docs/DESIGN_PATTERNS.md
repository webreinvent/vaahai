# Vaahai Design Patterns for AI Tools

This document outlines the key design patterns used in the Vaahai AI-augmented code review CLI tool, specifically formatted for AI tools to understand the architectural decisions, patterns, and implementation approaches.

## Core Design Patterns

### 1. Command Pattern

**Usage in Vaahai**: The CLI commands are implemented using the Command pattern, where each command is encapsulated as an object.

**Implementation**:
```python
class Command(ABC):
    @abstractmethod
    def execute(self, context: CommandContext) -> int:
        """Execute the command.
        
        Args:
            context: Command execution context
            
        Returns:
            Exit code
        """
        pass
```

**Examples**:
- `ReviewCommand`: Executes the code review workflow
- `AnalyzeCommand`: Executes the static analysis workflow
- `ConfigCommand`: Manages configuration settings
- `FixCommand`: Applies fixes to code

**Benefits**:
- Decouples command invocation from implementation
- Allows for command composition and sequencing
- Simplifies adding new commands

### 2. Factory Pattern

**Usage in Vaahai**: Factories are used to create instances of analyzers, LLM providers, and formatters based on configuration.

**Implementation**:
```python
class AnalyzerFactory:
    @staticmethod
    def create_analyzer(analyzer_name: str, config_manager: ConfigManager) -> Analyzer:
        """Create an analyzer instance."""
        # Implementation details...
```

**Examples**:
- `AnalyzerFactory`: Creates appropriate static analyzers
- `LLMProviderFactory`: Creates LLM provider instances
- `FormatterFactory`: Creates output formatters

**Benefits**:
- Centralizes instance creation logic
- Allows for runtime selection of implementations
- Simplifies adding new implementations

### 3. Strategy Pattern

**Usage in Vaahai**: Different strategies are used for static analysis, LLM integration, and output formatting.

**Implementation**:
```python
class Analyzer(ABC):
    @abstractmethod
    def analyze(self, file_path: str, options: AnalysisOptions) -> AnalysisResult:
        """Analyze a code file."""
        pass
```

**Examples**:
- `PylintAnalyzer`, `Flake8Analyzer`, `BanditAnalyzer`: Different analysis strategies
- `OpenAIProvider`, `OllamaProvider`: Different LLM integration strategies
- `TerminalFormatter`, `MarkdownFormatter`, `HTMLFormatter`: Different output formatting strategies

**Benefits**:
- Allows for interchangeable algorithms
- Encapsulates algorithm-specific logic
- Enables runtime selection of strategies

### 4. Adapter Pattern

**Usage in Vaahai**: Adapters are used to provide a uniform interface to different static analysis tools and LLM providers.

**Implementation**:
```python
class PylintAdapter(Analyzer):
    def analyze(self, file_path: str, options: AnalysisOptions) -> AnalysisResult:
        """Adapt Pylint output to the Analyzer interface."""
        # Implementation details...
```

**Examples**:
- `PylintAdapter`: Adapts Pylint to the Analyzer interface
- `OpenAIAdapter`: Adapts OpenAI API to the LLMProvider interface
- `OllamaAdapter`: Adapts Ollama API to the LLMProvider interface

**Benefits**:
- Provides a consistent interface to diverse tools
- Isolates integration details
- Simplifies adding support for new tools

### 5. Template Method Pattern

**Usage in Vaahai**: Template methods define the skeleton of algorithms, with specific steps implemented by subclasses.

**Implementation**:
```python
class BaseAnalyzer(Analyzer):
    def analyze(self, file_path: str, options: AnalysisOptions) -> AnalysisResult:
        """Template method for analysis workflow."""
        self.prepare(file_path, options)
        raw_result = self.run_analysis(file_path, options)
        return self.process_result(raw_result, file_path)
    
    @abstractmethod
    def run_analysis(self, file_path: str, options: AnalysisOptions) -> Any:
        """Run the actual analysis tool."""
        pass
    
    def prepare(self, file_path: str, options: AnalysisOptions) -> None:
        """Prepare for analysis (optional hook)."""
        pass
    
    @abstractmethod
    def process_result(self, raw_result: Any, file_path: str) -> AnalysisResult:
        """Process the raw analysis result."""
        pass
```

**Examples**:
- `BaseAnalyzer`: Template for analysis workflow
- `BaseLLMProvider`: Template for LLM interaction workflow
- `BaseFormatter`: Template for output formatting workflow

**Benefits**:
- Defines common algorithm structure
- Allows customization of specific steps
- Promotes code reuse

### 6. Observer Pattern

**Usage in Vaahai**: Observers are used for progress reporting and event handling during long-running operations.

**Implementation**:
```python
class ProgressObserver(ABC):
    @abstractmethod
    def on_progress(self, current: int, total: int, message: str) -> None:
        """Handle progress update."""
        pass
    
    @abstractmethod
    def on_complete(self, result: Any) -> None:
        """Handle operation completion."""
        pass
    
    @abstractmethod
    def on_error(self, error: Exception) -> None:
        """Handle operation error."""
        pass
```

**Examples**:
- `TerminalProgressObserver`: Displays progress in the terminal
- `LoggingProgressObserver`: Logs progress events
- `CIProgressObserver`: Handles progress in CI environments

**Benefits**:
- Decouples progress reporting from core logic
- Allows multiple observers for different outputs
- Simplifies adding new progress reporting mechanisms

### 7. Chain of Responsibility Pattern

**Usage in Vaahai**: Chains are used for processing files, applying fixes, and handling configuration.

**Implementation**:
```python
class FixHandler(ABC):
    def __init__(self, next_handler: Optional["FixHandler"] = None):
        self.next_handler = next_handler
    
    def handle(self, fix: Fix, file_path: str, options: FixOptions) -> FixResult:
        """Handle a fix or pass to the next handler."""
        if self.can_handle(fix, options):
            return self.process_fix(fix, file_path, options)
        elif self.next_handler:
            return self.next_handler.handle(fix, file_path, options)
        else:
            return FixResult(file_path=file_path, skipped_fixes=[fix])
    
    @abstractmethod
    def can_handle(self, fix: Fix, options: FixOptions) -> bool:
        """Check if this handler can handle the fix."""
        pass
    
    @abstractmethod
    def process_fix(self, fix: Fix, file_path: str, options: FixOptions) -> FixResult:
        """Process the fix."""
        pass
```

**Examples**:
- `SafeFixHandler`: Handles safe fixes
- `InteractiveFixHandler`: Handles fixes requiring user confirmation
- `ConfigurationChain`: Processes configuration from different sources

**Benefits**:
- Decouples request handling from processing
- Allows dynamic handler chains
- Simplifies adding new handlers

### 8. Composite Pattern

**Usage in Vaahai**: Composites are used for handling multiple files, combining analysis results, and organizing configuration.

**Implementation**:
```python
class CompositeAnalyzer(Analyzer):
    def __init__(self, analyzers: List[Analyzer]):
        self.analyzers = analyzers
    
    def analyze(self, file_path: str, options: AnalysisOptions) -> List[AnalysisResult]:
        """Run multiple analyzers and combine results."""
        results = []
        for analyzer in self.analyzers:
            if analyzer.supports_file(file_path):
                results.append(analyzer.analyze(file_path, options))
        return results
```

**Examples**:
- `CompositeAnalyzer`: Combines multiple analyzers
- `CompositeFormatter`: Combines multiple formatters
- `ConfigurationNode`: Represents hierarchical configuration

**Benefits**:
- Treats individual and composite objects uniformly
- Simplifies client code
- Enables hierarchical structures

### 9. Decorator Pattern

**Usage in Vaahai**: Decorators are used to add functionality to analyzers, formatters, and commands.

**Implementation**:
```python
class CachingAnalyzer(Analyzer):
    def __init__(self, analyzer: Analyzer, cache_manager: CacheManager):
        self.analyzer = analyzer
        self.cache_manager = cache_manager
    
    def analyze(self, file_path: str, options: AnalysisOptions) -> AnalysisResult:
        """Add caching to an analyzer."""
        cache_key = self._get_cache_key(file_path, options)
        cached_result = self.cache_manager.get(cache_key)
        if cached_result:
            return cached_result
        
        result = self.analyzer.analyze(file_path, options)
        self.cache_manager.set(cache_key, result)
        return result
    
    def _get_cache_key(self, file_path: str, options: AnalysisOptions) -> str:
        """Generate a cache key."""
        # Implementation details...
```

**Examples**:
- `CachingAnalyzer`: Adds caching to analyzers
- `LoggingCommand`: Adds logging to commands
- `TimingDecorator`: Adds performance timing

**Benefits**:
- Adds functionality without modifying original classes
- Allows dynamic composition of behaviors
- Promotes the open/closed principle

### 10. Repository Pattern

**Usage in Vaahai**: Repositories are used for configuration storage, caching, and result persistence.

**Implementation**:
```python
class ConfigRepository(ABC):
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a configuration value."""
        pass
    
    @abstractmethod
    def list(self, prefix: str = "") -> Dict[str, Any]:
        """List configuration values with a prefix."""
        pass
```

**Examples**:
- `TOMLConfigRepository`: Stores configuration in TOML files
- `CacheRepository`: Manages cached results
- `ReviewResultRepository`: Stores review results

**Benefits**:
- Abstracts data storage details
- Centralizes data access logic
- Simplifies testing with mock repositories

## Application-Specific Patterns

### 1. Pipeline Pattern

**Usage in Vaahai**: The review process is implemented as a pipeline of operations.

**Implementation**:
```python
class ReviewPipeline:
    def __init__(self, stages: List[ReviewStage]):
        self.stages = stages
    
    def process(self, context: ReviewContext) -> ReviewResult:
        """Process a review through all pipeline stages."""
        for stage in self.stages:
            context = stage.process(context)
        return context.result
```

**Examples**:
- `FileLoadingStage`: Loads file contents
- `StaticAnalysisStage`: Runs static analysis
- `LLMProcessingStage`: Processes code with LLM
- `ResultFormattingStage`: Formats results

**Benefits**:
- Breaks complex process into manageable stages
- Allows reordering and reconfiguration of stages
- Simplifies adding new stages

### 2. Plugin Pattern

**Usage in Vaahai**: Plugins are used to extend functionality with custom analyzers, formatters, and commands.

**Implementation**:
```python
class Plugin(ABC):
    @abstractmethod
    def initialize(self, registry: PluginRegistry) -> None:
        """Initialize the plugin and register components."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the plugin name."""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Get the plugin version."""
        pass
```

**Examples**:
- `CustomAnalyzerPlugin`: Adds custom analyzers
- `CustomFormatterPlugin`: Adds custom formatters
- `CustomCommandPlugin`: Adds custom commands

**Benefits**:
- Allows third-party extensions
- Maintains separation between core and extensions
- Enables dynamic loading of functionality

### 3. Context Object Pattern

**Usage in Vaahai**: Context objects are used to pass data between components and track state.

**Implementation**:
```python
class ReviewContext:
    def __init__(self, file_path: str, options: ReviewOptions):
        self.file_path = file_path
        self.options = options
        self.file_content: Optional[str] = None
        self.analysis_results: List[AnalysisResult] = []
        self.llm_feedback: Optional[ReviewFeedback] = None
        self.fixes: List[Fix] = []
        self.result: Optional[ReviewResult] = None
```

**Examples**:
- `ReviewContext`: Context for review process
- `AnalysisContext`: Context for analysis process
- `CommandContext`: Context for command execution

**Benefits**:
- Simplifies parameter passing
- Maintains state across operations
- Provides a single point of access to shared data

### 4. Configuration Hierarchy Pattern

**Usage in Vaahai**: Configuration is organized in a hierarchical structure with multiple layers.

**Implementation**:
```python
class ConfigurationManager:
    def __init__(self):
        self.layers = [
            DefaultConfigLayer(),
            GlobalConfigLayer(),
            ProjectConfigLayer(),
            CommandLineConfigLayer()
        ]
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value from the appropriate layer."""
        for layer in reversed(self.layers):
            value = layer.get(key)
            if value is not None:
                return value
        return default
```

**Examples**:
- `DefaultConfigLayer`: Built-in defaults
- `GlobalConfigLayer`: User-level settings
- `ProjectConfigLayer`: Project-level settings
- `CommandLineConfigLayer`: Command-line options

**Benefits**:
- Provides flexible configuration override
- Separates configuration sources
- Enables context-specific settings

### 5. Result Aggregation Pattern

**Usage in Vaahai**: Results from multiple sources are aggregated into a unified view.

**Implementation**:
```python
class ResultAggregator:
    def aggregate(
        self, 
        file_path: str, 
        analysis_results: List[AnalysisResult], 
        llm_feedback: Optional[ReviewFeedback]
    ) -> ReviewResult:
        """Aggregate results from different sources."""
        # Implementation details...
```

**Examples**:
- `ReviewResultAggregator`: Combines static analysis and LLM results
- `IssueAggregator`: Combines issues from different analyzers
- `FixAggregator`: Combines fixes from different sources

**Benefits**:
- Provides a unified view of results
- Handles conflicts and duplicates
- Simplifies result presentation

## Implementation Techniques

### 1. Dependency Injection

**Usage in Vaahai**: Dependencies are injected into components rather than created internally.

**Implementation**:
```python
class Orchestrator:
    def __init__(
        self, 
        config_manager: ConfigManager,
        analyzer_factory: AnalyzerFactory,
        llm_provider_factory: LLMProviderFactory,
        formatter_factory: FormatterFactory
    ):
        self.config_manager = config_manager
        self.analyzer_factory = analyzer_factory
        self.llm_provider_factory = llm_provider_factory
        self.formatter_factory = formatter_factory
```

**Benefits**:
- Decouples component creation from usage
- Simplifies testing with mock dependencies
- Enables flexible component configuration

### 2. Configuration as Code

**Usage in Vaahai**: Configuration is represented as structured code objects.

**Implementation**:
```python
class ReviewConfiguration(BaseModel):
    depth: ReviewDepth = ReviewDepth.STANDARD
    llm_provider: str = "openai"
    model: str = "gpt-4"
    analyzers: List[str] = ["pylint", "flake8", "bandit"]
    # Additional configuration...
```

**Benefits**:
- Provides type safety for configuration
- Enables validation and default values
- Simplifies configuration handling

### 3. Error Handling Strategy

**Usage in Vaahai**: Errors are categorized and handled according to severity and context.

**Implementation**:
```python
try:
    result = analyzer.analyze(file_path, options)
except AnalysisError as e:
    if options.fail_fast:
        raise
    logger.warning(f"Analysis failed: {e}")
    result = AnalysisResult(
        issues=[],
        metrics={},
        tool_name=analyzer.get_name(),
        file_path=file_path
    )
```

**Benefits**:
- Provides consistent error handling
- Enables graceful degradation
- Improves user experience

### 4. Lazy Loading

**Usage in Vaahai**: Components are loaded only when needed to improve performance.

**Implementation**:
```python
class LazyAnalyzerFactory:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.analyzers: Dict[str, Analyzer] = {}
    
    def get_analyzer(self, analyzer_name: str) -> Analyzer:
        """Get or create an analyzer instance."""
        if analyzer_name not in self.analyzers:
            self.analyzers[analyzer_name] = self._create_analyzer(analyzer_name)
        return self.analyzers[analyzer_name]
    
    def _create_analyzer(self, analyzer_name: str) -> Analyzer:
        """Create an analyzer instance."""
        # Implementation details...
```

**Benefits**:
- Reduces startup time
- Minimizes resource usage
- Improves overall performance

### 5. Extension Points

**Usage in Vaahai**: The system defines clear extension points for customization.

**Implementation**:
```python
# Extension point for analyzers
@analyzer_registry.register("custom")
class CustomAnalyzer(Analyzer):
    # Implementation details...

# Extension point for formatters
@formatter_registry.register("custom")
class CustomFormatter(Formatter):
    # Implementation details...
```

**Benefits**:
- Enables third-party extensions
- Maintains system integrity
- Simplifies customization

## Anti-Patterns to Avoid

### 1. God Objects

**Description**: Avoid creating large, monolithic classes that handle too many responsibilities.

**Prevention**:
- Use the Single Responsibility Principle
- Break large classes into smaller, focused components
- Use composition over inheritance

### 2. Hardcoded Dependencies

**Description**: Avoid hardcoding dependencies within components.

**Prevention**:
- Use dependency injection
- Use factories for component creation
- Use configuration for dependency selection

### 3. Leaky Abstractions

**Description**: Avoid abstractions that expose implementation details.

**Prevention**:
- Design clean interfaces
- Hide implementation details
- Use proper encapsulation

### 4. Premature Optimization

**Description**: Avoid optimizing before measuring performance.

**Prevention**:
- Focus on clean, maintainable code first
- Measure performance to identify bottlenecks
- Optimize only where necessary

### 5. Reinventing the Wheel

**Description**: Avoid reimplementing functionality that exists in libraries.

**Prevention**:
- Use established libraries for common functionality
- Focus on core business logic
- Contribute to existing libraries instead of forking
