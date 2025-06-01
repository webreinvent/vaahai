# Vaahai Architecture Documentation for AI Tools

This document provides a detailed architectural overview of the Vaahai AI-augmented code review CLI tool, specifically formatted for AI tools to understand the system structure, component relationships, and implementation patterns.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────┐
│              CLI Layer              │
│  (User Interface & Command Routing) │
└───────────────────┬─────────────────┘
                    │
┌───────────────────▼─────────────────┐
│           Core Layer                │
│  (Orchestration & Coordination)     │
└───┬───────────────────────────┬─────┘
    │                           │
┌───▼───────────────┐   ┌───────▼───────────┐
│  Analysis Layer   │   │     LLM Layer     │
│ (Static Analysis) │   │ (AI Integration)  │
└───────────────────┘   └───────────────────┘
          │                       │
┌─────────▼───────────────────────▼─────────┐
│              Output Layer                 │
│     (Formatting & Presentation)           │
└─────────────────────────────────────────┬─┘
                                          │
┌─────────────────────────────────────────▼─┐
│              Fix Layer                    │
│      (Code Modification & Patching)       │
└─────────────────────────────────────────┬─┘
```

### Component Relationships

1. **CLI Layer** → **Core Layer**: User commands are parsed and routed to appropriate core components
2. **Core Layer** → **Analysis Layer**: Code is sent for static analysis
3. **Core Layer** → **LLM Layer**: Code and analysis results are sent to LLMs
4. **Analysis Layer** → **Output Layer**: Static analysis results are formatted
5. **LLM Layer** → **Output Layer**: LLM responses are parsed and formatted
6. **Output Layer** → **Fix Layer**: Suggested fixes are extracted and prepared for application

## Component Details

### 1. CLI Layer

**Purpose**: Handle user interaction, command parsing, and routing

**Key Components**:
- `cli/main.py`: Entry point and command registration
- `cli/commands/`: Individual command implementations
- `cli/options.py`: Common command options

**Design Patterns**:
- Command Pattern: Each command is implemented as a separate class
- Dependency Injection: Services are injected into commands

**Key Interfaces**:
```python
class Command(ABC):
    @abstractmethod
    def execute(self, context: CommandContext) -> int:
        pass
```

### 2. Core Layer

**Purpose**: Orchestrate the review process and coordinate between components

**Key Components**:
- `core/orchestrator.py`: Main orchestration logic
- `core/config.py`: Configuration management
- `core/scanner.py`: File scanning and processing
- `core/context.py`: Review context management

**Design Patterns**:
- Mediator Pattern: Orchestrator coordinates between components
- Strategy Pattern: Different review strategies based on configuration
- Repository Pattern: Configuration storage and retrieval

**Key Interfaces**:
```python
class Orchestrator:
    def review(self, paths: List[str], options: ReviewOptions) -> ReviewResult:
        pass
        
class ConfigManager:
    def get(self, key: str, default: Any = None) -> Any:
        pass
    def set(self, key: str, value: Any) -> None:
        pass
```

### 3. Analysis Layer

**Purpose**: Perform static analysis on code files

**Key Components**:
- `analyzers/base.py`: Base analyzer interface
- `analyzers/python/`: Python-specific analyzers
- `analyzers/factory.py`: Analyzer factory

**Design Patterns**:
- Strategy Pattern: Different analyzers for different languages
- Factory Pattern: Create appropriate analyzers based on file type
- Adapter Pattern: Uniform interface for different analysis tools

**Key Interfaces**:
```python
class Analyzer(ABC):
    @abstractmethod
    def analyze(self, file_path: str, options: AnalysisOptions) -> AnalysisResult:
        pass
```

### 4. LLM Layer

**Purpose**: Interact with language models for AI-powered review

**Key Components**:
- `llm/base.py`: Base LLM provider interface
- `llm/openai.py`: OpenAI integration
- `llm/ollama.py`: Ollama integration
- `llm/factory.py`: LLM provider factory
- `llm/prompts/`: Prompt templates

**Design Patterns**:
- Strategy Pattern: Different LLM providers
- Template Method Pattern: Common LLM interaction flow
- Factory Pattern: Create appropriate LLM provider

**Key Interfaces**:
```python
class LLMProvider(ABC):
    @abstractmethod
    def review(self, code: str, analysis_results: AnalysisResult, 
               options: LLMOptions) -> LLMResponse:
        pass
```

### 5. Output Layer

**Purpose**: Format and present review results

**Key Components**:
- `formatters/base.py`: Base formatter interface
- `formatters/terminal.py`: Terminal output
- `formatters/markdown.py`: Markdown output
- `formatters/html.py`: HTML output
- `formatters/factory.py`: Formatter factory

**Design Patterns**:
- Strategy Pattern: Different formatters for different output formats
- Visitor Pattern: Format different types of review results
- Factory Pattern: Create appropriate formatter

**Key Interfaces**:
```python
class Formatter(ABC):
    @abstractmethod
    def format(self, review_result: ReviewResult) -> str:
        pass
```

### 6. Fix Layer

**Purpose**: Apply suggested fixes to code

**Key Components**:
- `fixes/applier.py`: Fix application logic
- `fixes/interactive.py`: Interactive fix application
- `fixes/patch.py`: Patch generation

**Design Patterns**:
- Command Pattern: Each fix is a command that can be applied or reverted
- Chain of Responsibility: Process fixes in sequence
- Memento Pattern: Save state before applying fixes

**Key Interfaces**:
```python
class FixApplier:
    def apply(self, file_path: str, fixes: List[Fix], 
              options: FixOptions) -> FixResult:
        pass
```

## Data Flow

### Review Process Data Flow

1. **Input**: User provides file paths and options
2. **Scanning**: Files are scanned and filtered based on patterns
3. **Static Analysis**: Each file is analyzed using appropriate static analyzers
4. **LLM Processing**:
   - Code and analysis results are sent to LLM
   - LLM generates review feedback
   - Response is parsed into structured format
5. **Result Formatting**: Results are formatted according to user preference
6. **Fix Application** (if requested):
   - Fixes are extracted from LLM response
   - User is prompted for each fix (in interactive mode)
   - Approved fixes are applied to files

### Data Structures

**ReviewContext**:
```python
class ReviewContext:
    files: List[FileInfo]
    options: ReviewOptions
    config: ConfigManager
```

**AnalysisResult**:
```python
class Issue:
    code: str
    message: str
    line: int
    column: int
    severity: IssueSeverity
    
class AnalysisResult:
    issues: List[Issue]
    metrics: Dict[str, Any]
    tool_name: str
    file_path: str
```

**LLMResponse**:
```python
class ReviewFeedback:
    summary: str
    strengths: List[str]
    issues: List[ReviewIssue]
    recommendations: List[str]
    
class ReviewIssue:
    description: str
    severity: IssueSeverity
    line: Optional[int]
    code: Optional[str]
    suggested_fix: Optional[str]
```

**ReviewResult**:
```python
class ReviewResult:
    file_path: str
    analysis_results: List[AnalysisResult]
    llm_feedback: Optional[ReviewFeedback]
    fixes: List[Fix]
```

## Implementation Patterns

### 1. Configuration Management

Configuration is managed in a hierarchical structure:
1. Default configuration (hardcoded)
2. Global configuration (~/.config/vaahai/config.toml)
3. Project configuration (.vaahai/config.toml)
4. Command-line options

Each level overrides the previous levels.

### 2. Plugin System

The plugin system follows these principles:
1. Plugins are discovered dynamically
2. Plugins implement specific interfaces
3. Plugins are registered with a registry
4. Plugins are loaded based on configuration

### 3. Error Handling

Error handling follows these patterns:
1. Domain-specific exceptions
2. Error categorization by severity
3. User-friendly error messages
4. Graceful degradation when possible

### 4. Testing Strategy

The testing strategy includes:
1. Unit tests for individual components
2. Integration tests for component interactions
3. End-to-end tests for complete workflows
4. Snapshot tests for output formatting

## Extension Points

The system is designed with the following extension points:

1. **Static Analyzers**: Add new analyzers by implementing the `Analyzer` interface
2. **LLM Providers**: Add new LLM providers by implementing the `LLMProvider` interface
3. **Output Formatters**: Add new formatters by implementing the `Formatter` interface
4. **Commands**: Add new commands by implementing the `Command` interface
5. **Prompt Templates**: Add new prompt templates in the `llm/prompts/` directory

## Performance Considerations

1. **Lazy Loading**: Components are loaded only when needed
2. **Caching**: Results are cached to avoid redundant operations
3. **Parallelization**: Independent operations are parallelized
4. **Resource Management**: Resources are properly managed and released

## Security Considerations

1. **API Key Management**: API keys are stored securely
2. **Code Privacy**: Minimal code exposure to external services
3. **Input Validation**: All inputs are validated
4. **Safe Defaults**: Conservative default settings
