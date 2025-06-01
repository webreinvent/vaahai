# Vaahai Business Logic for AI Tools

This document outlines the core business logic, rules, and implementation details of the Vaahai AI-augmented code review CLI tool, specifically formatted for AI tools to understand the underlying principles and decision-making processes.

## Core Business Rules

### Code Review Process

1. **Review Depth Determination**
   - **Quick Review**: Focuses on critical issues only, uses faster analyzers, and limits LLM token usage
   - **Standard Review**: Balanced approach with moderate analysis depth and token usage
   - **Deep Review**: Comprehensive analysis with all available analyzers and maximum context for LLMs

2. **File Selection Logic**
   - Files are selected based on:
     - Explicit paths provided by the user
     - Glob patterns for inclusion/exclusion
     - Git diff for changed files (when `--diff` flag is used)
     - Related files detection (when `--include-related` flag is used)
   - Files are filtered by:
     - Language support (based on file extension)
     - Size limits (configurable, default max 100KB)
     - Exclusion patterns (e.g., `.gitignore` patterns)

3. **Issue Severity Classification**
   - **Critical**: Issues that could lead to security vulnerabilities, crashes, or data loss
   - **High**: Issues that significantly impact code quality, performance, or maintainability
   - **Medium**: Issues that moderately impact code quality or violate best practices
   - **Low**: Minor issues, style violations, or potential improvements
   - **Info**: Informational notes or suggestions

4. **Fix Safety Determination**
   - A fix is considered "safe" if:
     - It only affects whitespace, comments, or documentation
     - It fixes a simple syntax error without changing functionality
     - It addresses a well-understood pattern with a standard solution
     - It has a high confidence score from the LLM (>0.9)
   - A fix is considered "unsafe" if:
     - It changes core logic or functionality
     - It affects multiple files or components
     - It has a low confidence score from the LLM (<0.7)
     - It involves security-sensitive code

## LLM Integration Logic

### Prompt Construction

1. **Context Assembly**
   - **Code Context**: The file being reviewed, with line numbers
   - **Project Context**: Information about the project, language, and frameworks
   - **Analysis Context**: Results from static analyzers
   - **User Context**: Custom context provided by the user
   - **Review Focus**: Specific areas to focus on (security, performance, etc.)

2. **Prompt Template Selection**
   - Templates are selected based on:
     - Review depth (quick, standard, deep)
     - Review focus (general, security, performance, style)
     - File type (Python, JavaScript, etc.)
     - Custom template specified by the user

3. **Token Management**
   - For large files, the code is split into chunks with context preservation
   - Critical sections (e.g., function definitions, class declarations) are prioritized
   - Analysis results are filtered to focus on the most relevant issues
   - Context is compressed by removing redundant information

### Response Processing

1. **Structured Output Parsing**
   - LLM responses are parsed into structured data:
     - Summary of the review
     - Strengths of the code
     - Issues found (with severity, location, and suggested fixes)
     - Recommendations for improvement

2. **Fix Extraction**
   - Fixes are extracted from the LLM response
   - Each fix is validated for:
     - Correct syntax
     - Proper line numbers
     - Compatibility with the codebase
     - Safety (using the safety determination rules)

3. **Confidence Scoring**
   - Each issue and fix is assigned a confidence score
   - Factors affecting confidence:
     - LLM's expressed confidence
     - Alignment with static analysis results
     - Complexity of the issue
     - Specificity of the suggestion

## Static Analysis Integration

### Analyzer Selection

1. **Language-Specific Analyzers**
   - Python: pylint, flake8, bandit, mypy
   - JavaScript: eslint, jshint
   - TypeScript: tslint, typescript-eslint
   - Other languages: language-appropriate analyzers

2. **Analysis Depth Configuration**
   - **Quick**: Basic linting only
   - **Standard**: Linting + simple static analysis
   - **Deep**: Comprehensive static analysis + type checking

3. **Custom Rules Integration**
   - Project-specific rules are loaded from:
     - Configuration files in the project root
     - `.vaahai/analyzers/` directory
     - User's global configuration

### Result Normalization

1. **Issue Standardization**
   - Issues from different analyzers are normalized to a common format:
     - Consistent severity levels
     - Standardized issue codes
     - Normalized line/column references

2. **Deduplication**
   - Similar issues from multiple analyzers are deduplicated
   - Deduplication factors:
     - Line proximity
     - Issue type similarity
     - Message similarity

3. **Prioritization**
   - Issues are prioritized based on:
     - Severity
     - Analyzer confidence
     - Issue type
     - Code location (critical paths are prioritized)

## Output Formatting Logic

### Format Selection

1. **Terminal Output**
   - Interactive mode with color coding
   - Issue grouping by severity
   - Collapsible sections for details
   - Progress indicators for long-running operations

2. **Markdown Output**
   - Structured document with sections
   - Code blocks with syntax highlighting
   - Issue tables with severity indicators
   - Links to relevant documentation

3. **HTML Output**
   - Interactive HTML report
   - Collapsible sections
   - Syntax-highlighted code
   - Inline issue annotations
   - Fix preview functionality

### Content Customization

1. **Verbosity Levels**
   - **Minimal**: Summary and critical issues only
   - **Normal**: Summary, issues, and key recommendations
   - **Detailed**: All information including full context

2. **Focus Filtering**
   - Content can be filtered by:
     - Issue severity
     - Issue type
     - Code section
     - Specific concerns (security, performance, etc.)

## Fix Application Logic

### Interactive Mode

1. **Fix Presentation**
   - Each fix is presented with:
     - Issue description
     - Original code
     - Proposed fix
     - Diff view
     - Safety assessment

2. **User Interaction**
   - User can:
     - Accept the fix
     - Reject the fix
     - Edit the fix
     - Skip to the next fix
     - Apply all safe fixes
     - Quit the process

3. **Application Strategy**
   - Fixes are applied in order of:
     - File dependency (base files first)
     - Line number (bottom to top to preserve line numbers)
     - Safety (safer fixes first)

### Non-Interactive Mode

1. **Automatic Application**
   - Only safe fixes are applied automatically
   - Application is logged for review
   - Backup files are created

2. **Patch Generation**
   - Patches are generated for all fixes
   - Patch files follow git format
   - Patches include metadata about the issues

## Configuration Management

### Configuration Hierarchy

1. **Default Configuration**
   - Built-in defaults for all settings
   - Conservative settings for safety

2. **Global Configuration**
   - User-level settings in `~/.config/vaahai/config.toml`
   - Applies to all projects

3. **Project Configuration**
   - Project-level settings in `.vaahai/config.toml`
   - Overrides global configuration

4. **Command-Line Options**
   - Options provided directly on the command line
   - Highest precedence

### Configuration Validation

1. **Schema Validation**
   - All configuration is validated against a schema
   - Type checking for all values
   - Range validation for numeric values
   - Pattern validation for strings

2. **Dependency Validation**
   - Checks for conflicting settings
   - Validates dependencies between settings
   - Ensures required settings are present

3. **Security Validation**
   - Sensitive settings are identified
   - API keys are validated for format
   - Secure storage options are verified

## Performance Optimization

### Resource Management

1. **Memory Usage**
   - Large files are processed in chunks
   - Results are streamed when possible
   - Temporary data is cleaned up promptly

2. **Concurrency**
   - File analysis is parallelized
   - LLM requests are batched when appropriate
   - CPU-intensive operations use process pools
   - I/O-intensive operations use thread pools

3. **Caching**
   - Analysis results are cached based on file hash
   - LLM responses are cached for similar inputs
   - Cache invalidation on file changes
   - Configurable cache size and location

### Optimization Strategies

1. **Incremental Processing**
   - Only changed files are processed when possible
   - Partial results are saved and reused
   - Differential analysis for git changes

2. **Prioritization**
   - Critical files are processed first
   - High-impact issues are reported first
   - Interactive feedback during long operations

## Security Considerations

### API Key Management

1. **Storage Options**
   - Environment variables (recommended)
   - Configuration file with restricted permissions
   - Secure credential storage (platform-specific)

2. **Usage Patterns**
   - Keys are never logged or displayed
   - Keys are masked in error messages
   - Keys are not included in command history

3. **Scope Limitation**
   - Minimal permissions principle
   - Separate keys for different operations
   - Rotation and expiration policies

### Code Privacy

1. **Data Minimization**
   - Only necessary code is sent to external services
   - Sensitive information is redacted
   - Option to use local LLMs exclusively

2. **Consent and Control**
   - Explicit user confirmation before sending code externally
   - Clear indication of what will be shared
   - Option to review before sending

## Extension and Plugin System

### Plugin Architecture

1. **Plugin Types**
   - Analyzer plugins: Add new static analyzers
   - Formatter plugins: Add new output formats
   - LLM provider plugins: Add new LLM integrations
   - Command plugins: Add new CLI commands

2. **Plugin Discovery**
   - Plugins are discovered from:
     - Built-in plugins directory
     - User's global plugins directory
     - Project-specific plugins directory

3. **Plugin Validation**
   - Interface compliance checking
   - Version compatibility verification
   - Security validation for external plugins

### Customization Points

1. **Prompt Templates**
   - Custom templates in `.claude/commands/` directory
   - Template variables for dynamic content
   - Conditional sections based on context

2. **Analysis Rules**
   - Custom analyzer configurations
   - Project-specific rule sets
   - Rule severity overrides

3. **Output Themes**
   - Custom color schemes for terminal output
   - Custom templates for HTML and Markdown output
   - Branding customization options

## Implementation Details

### File Processing Pipeline

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  File       │     │  Static     │     │  LLM        │     │  Result     │
│  Selection  │────▶│  Analysis   │────▶│  Processing │────▶│  Formatting │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                           │                   │                   │
                           ▼                   ▼                   ▼
                    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
                    │  Analysis   │     │  LLM        │     │  Output     │
                    │  Cache      │     │  Cache      │     │  Cache      │
                    └─────────────┘     └─────────────┘     └─────────────┘
```

1. **File Selection Stage**
   - Input: File paths, glob patterns, git diff
   - Processing: File filtering, related file detection
   - Output: List of files to process

2. **Static Analysis Stage**
   - Input: Files to analyze
   - Processing: Language detection, analyzer selection, analysis execution
   - Output: Normalized analysis results

3. **LLM Processing Stage**
   - Input: Files, analysis results, context
   - Processing: Prompt construction, LLM interaction, response parsing
   - Output: Structured review feedback

4. **Result Formatting Stage**
   - Input: Analysis results, LLM feedback
   - Processing: Format selection, content customization
   - Output: Formatted review results

### Command Execution Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Command    │     │  Option     │     │  Config     │     │  Execution  │
│  Parsing    │────▶│  Validation │────▶│  Loading    │────▶│  Context    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Result     │     │  Fix        │     │  Output     │     │  Command    │
│  Handling   │◀────│  Application│◀────│  Generation │◀────│  Execution  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

1. **Command Parsing Stage**
   - Input: Command-line arguments
   - Processing: Argument parsing, command identification
   - Output: Parsed command and options

2. **Option Validation Stage**
   - Input: Parsed options
   - Processing: Type checking, range validation, dependency validation
   - Output: Validated options

3. **Config Loading Stage**
   - Input: Command context, validated options
   - Processing: Configuration hierarchy resolution
   - Output: Merged configuration

4. **Execution Context Stage**
   - Input: Command, options, configuration
   - Processing: Context preparation, dependency injection
   - Output: Execution context

5. **Command Execution Stage**
   - Input: Execution context
   - Processing: Command-specific logic
   - Output: Command results

6. **Output Generation Stage**
   - Input: Command results
   - Processing: Formatting, filtering
   - Output: Formatted output

7. **Fix Application Stage**
   - Input: Command results, fix options
   - Processing: Fix validation, application
   - Output: Fix results

8. **Result Handling Stage**
   - Input: Command results, fix results
   - Processing: Exit code determination, result storage
   - Output: Final command outcome

### Data Flow Between Components

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  CLI Layer  │     │  Core Layer │     │  Analysis   │
│             │◀───▶│             │◀───▶│  Layer      │
└─────────────┘     └─────────────┘     └─────────────┘
                          ▲ ▲
                          │ │
                    ┌─────┘ └─────┐
                    │             │
              ┌─────▼────┐   ┌────▼─────┐
              │  LLM     │   │  Output  │
              │  Layer   │   │  Layer   │
              └──────────┘   └──────────┘
```

1. **CLI Layer → Core Layer**
   - Command options
   - User input
   - Execution context

2. **Core Layer → Analysis Layer**
   - Files to analyze
   - Analysis options
   - Analyzer selection

3. **Analysis Layer → Core Layer**
   - Analysis results
   - Issue details
   - Metrics

4. **Core Layer → LLM Layer**
   - Code to review
   - Analysis context
   - Prompt configuration

5. **LLM Layer → Core Layer**
   - Review feedback
   - Suggested fixes
   - Confidence scores

6. **Core Layer → Output Layer**
   - Combined results
   - Output format
   - Customization options

7. **Output Layer → CLI Layer**
   - Formatted output
   - Interactive elements
   - Exit codes

## Key Algorithms

### Related File Detection

```python
def find_related_files(file_path, project_files, max_files=5):
    """Find files related to the given file."""
    # Implementation details...
    # 1. Parse imports and references
    # 2. Calculate file similarity scores
    # 3. Select top related files
    # 4. Return sorted by relevance
```

### Issue Deduplication

```python
def deduplicate_issues(issues):
    """Deduplicate similar issues from different analyzers."""
    # Implementation details...
    # 1. Group issues by line proximity
    # 2. Calculate similarity scores
    # 3. Merge similar issues
    # 4. Return deduplicated issues
```

### Fix Safety Analysis

```python
def analyze_fix_safety(original_code, fixed_code, context):
    """Analyze the safety of a suggested fix."""
    # Implementation details...
    # 1. Calculate diff between original and fixed code
    # 2. Analyze scope of changes
    # 3. Check for risky patterns
    # 4. Return safety score and reasoning
```

### Token Management

```python
def optimize_tokens(code, analysis_results, max_tokens):
    """Optimize token usage for LLM context."""
    # Implementation details...
    # 1. Calculate token usage
    # 2. Prioritize critical sections
    # 3. Compress or truncate as needed
    # 4. Return optimized content
```

## Error Handling and Recovery

### Error Categorization

1. **User Errors**
   - Invalid command syntax
   - Missing required arguments
   - Invalid configuration
   - Unsupported file types

2. **System Errors**
   - File access issues
   - Network connectivity problems
   - Insufficient resources
   - External service failures

3. **Logic Errors**
   - Unexpected data formats
   - Plugin compatibility issues
   - Algorithm failures
   - State inconsistencies

### Recovery Strategies

1. **Graceful Degradation**
   - Fall back to simpler analyzers if advanced ones fail
   - Use cached results if fresh analysis fails
   - Skip problematic files and continue with others
   - Reduce feature set when resources are constrained

2. **Retry Mechanisms**
   - Exponential backoff for external service calls
   - Alternative endpoints for API failures
   - Chunking of large requests
   - Circuit breakers for persistent failures

3. **User Guidance**
   - Clear error messages with actionable advice
   - Suggestions for configuration fixes
   - Links to troubleshooting documentation
   - Interactive recovery options

## Logging and Telemetry

### Logging Levels

1. **ERROR**: Critical failures that prevent operation
2. **WARNING**: Issues that affect functionality but allow continued operation
3. **INFO**: Important operational events
4. **DEBUG**: Detailed information for troubleshooting
5. **TRACE**: Very detailed internal state for development

### Telemetry Categories

1. **Usage Metrics**
   - Commands executed
   - Options selected
   - Files processed
   - Features used

2. **Performance Metrics**
   - Execution time
   - Memory usage
   - Token consumption
   - Cache hit rates

3. **Error Metrics**
   - Error frequencies
   - Recovery success rates
   - User-reported issues
   - Unexpected behaviors

### Privacy Controls

1. **Data Collection Policies**
   - Explicit opt-in for telemetry
   - Anonymous aggregation by default
   - Local-only logging option
   - Data retention limits

2. **Sensitive Data Protection**
   - Code content is never included in telemetry
   - File paths are hashed
   - Personal identifiers are removed
   - Configuration values are redacted
