# Vaahai AI Integration Guide for AI Tools

This document provides detailed information about the AI integration aspects of the Vaahai AI-augmented code review CLI tool, specifically formatted for AI tools to understand how LLMs are integrated, prompt engineering strategies, and AI-specific implementation details.

## LLM Integration Architecture

### Integration Approach

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Prompt         │     │  LLM            │     │  Response       │
│  Engineering    │────▶│  Interaction    │────▶│  Processing     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        ▲                       ▲                       │
        │                       │                       ▼
┌───────┴───────┐     ┌────────┴────────┐     ┌─────────────────┐
│  Context      │     │  Provider       │     │  Result         │
│  Assembly     │     │  Management     │     │  Integration    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Key Components

1. **Context Assembly**
   - Gathers code, analysis results, and user context
   - Optimizes context for token efficiency
   - Structures information for LLM consumption

2. **Prompt Engineering**
   - Designs effective prompts for specific tasks
   - Manages prompt templates
   - Applies few-shot learning techniques

3. **LLM Interaction**
   - Handles API communication
   - Manages rate limiting and retries
   - Streams responses when appropriate

4. **Provider Management**
   - Abstracts provider-specific details
   - Handles authentication and configuration
   - Supports multiple LLM providers

5. **Response Processing**
   - Parses structured responses
   - Extracts actionable insights
   - Validates and filters results

6. **Result Integration**
   - Combines LLM insights with static analysis
   - Prioritizes and deduplicates findings
   - Formats for human consumption

## Supported LLM Providers

### 1. OpenAI

**Models Supported**:
- GPT-4 (Recommended)
- GPT-3.5-Turbo
- GPT-4-Turbo

**Integration Details**:
- Uses OpenAI Python SDK
- Supports streaming responses
- Configurable temperature and top_p
- Token counting and optimization

**Configuration**:
```toml
[llm.openai]
api_key = "${VAAHAI_OPENAI_API_KEY}"
model = "gpt-4"
temperature = 0.3
max_tokens = 4000
```

### 2. Ollama

**Models Supported**:
- Llama 2
- Mistral
- CodeLlama
- Custom models

**Integration Details**:
- Uses Ollama REST API
- Local model execution
- Reduced latency for quick reviews
- Complete privacy for sensitive code

**Configuration**:
```toml
[llm.ollama]
host = "http://localhost:11434"
model = "codellama"
temperature = 0.3
```

### 3. Anthropic (Planned)

**Models Supported**:
- Claude 3 Opus
- Claude 3 Sonnet
- Claude 3 Haiku

**Integration Details**:
- Will use Anthropic Python SDK
- Optimized for code understanding
- Support for long context windows
- Advanced reasoning capabilities

**Configuration**:
```toml
[llm.anthropic]
api_key = "${VAAHAI_ANTHROPIC_API_KEY}"
model = "claude-3-opus-20240229"
temperature = 0.3
max_tokens = 4000
```

### 4. Plugin System for Custom Providers

**Supported Extensions**:
- Custom LLM providers
- Self-hosted models
- Specialized code models
- Multi-model ensembles

**Integration Details**:
- Plugin interface for new providers
- Configuration management
- Performance benchmarking
- Capability discovery

## Prompt Engineering Strategy

### Prompt Structure

1. **System Context**
   - Tool identity and purpose
   - Expected response format
   - Ethical guidelines
   - Specific instructions

2. **Code Context**
   - File content with line numbers
   - Language and framework information
   - Project structure context
   - Related files (when available)

3. **Analysis Context**
   - Static analysis results
   - Issue descriptions and locations
   - Metrics and statistics
   - Previous review history

4. **Task Instructions**
   - Specific review focus
   - Output format requirements
   - Reasoning requirements
   - Confidence scoring instructions

### Example Prompt Template

```
You are Vaahai, an AI code review assistant. Your task is to review the following {language} code and provide helpful feedback.

## Code to Review:
```{language}
{code}
```

## Static Analysis Results:
{analysis_results}

## Project Context:
{project_context}

## Review Instructions:
Please review this code with a focus on {review_focus}. Provide:
1. A brief summary of the code
2. Key strengths of the implementation
3. Issues found, with each issue including:
   - Description of the problem
   - Severity (critical, high, medium, low, info)
   - Line number(s)
   - Suggested fix (if applicable)
4. General recommendations for improvement

Format your response in JSON as follows:
{
  "summary": "Brief summary of the code",
  "strengths": ["Strength 1", "Strength 2", ...],
  "issues": [
    {
      "description": "Issue description",
      "severity": "high",
      "line": 42,
      "suggested_fix": "Code fix suggestion"
    },
    ...
  ],
  "recommendations": ["Recommendation 1", "Recommendation 2", ...]
}
```

### Prompt Variations

1. **Depth-Based Variations**
   - Quick Review: Focus on critical issues only
   - Standard Review: Balanced analysis
   - Deep Review: Comprehensive analysis

2. **Focus-Based Variations**
   - General: Overall code quality
   - Security: Security vulnerabilities
   - Performance: Performance optimization
   - Style: Code style and conventions

3. **Language-Specific Variations**
   - Python-specific patterns and issues
   - JavaScript/TypeScript-specific guidance
   - Other language-specific considerations

### Few-Shot Learning Examples

Each prompt template includes carefully selected examples to guide the LLM:

```
## Example 1:
[Code with a specific issue]

## Example Analysis:
{
  "summary": "This function calculates factorial recursively",
  "strengths": ["Clear function name", "Handles base case"],
  "issues": [
    {
      "description": "Missing termination condition can cause stack overflow",
      "severity": "critical",
      "line": 3,
      "suggested_fix": "Add if n < 0: raise ValueError(\"Input must be non-negative\")"
    }
  ],
  "recommendations": ["Add input validation", "Consider iterative approach for efficiency"]
}
```

## Response Processing

### Structured Output Parsing

1. **JSON Parsing**
   - Extracts structured data from LLM response
   - Handles malformed JSON with fallback strategies
   - Validates against expected schema

2. **Issue Extraction**
   - Normalizes severity levels
   - Validates line numbers
   - Extracts suggested fixes

3. **Confidence Scoring**
   - Analyzes LLM confidence signals
   - Correlates with static analysis
   - Assigns confidence scores to issues

### Example Processing Logic

```python
def process_llm_response(response: str) -> ReviewFeedback:
    """Process LLM response into structured feedback."""
    try:
        # Attempt to parse JSON response
        data = json.loads(response)
        
        # Validate required fields
        if not all(k in data for k in ["summary", "strengths", "issues", "recommendations"]):
            raise ValueError("Missing required fields in response")
        
        # Process issues
        processed_issues = []
        for issue in data["issues"]:
            # Normalize severity
            severity = normalize_severity(issue.get("severity", "medium"))
            
            # Validate line number
            line = validate_line_number(issue.get("line"))
            
            # Process suggested fix
            suggested_fix = process_suggested_fix(issue.get("suggested_fix", ""))
            
            # Calculate confidence
            confidence = calculate_confidence(issue, severity)
            
            processed_issues.append(ReviewIssue(
                description=issue["description"],
                severity=severity,
                line=line,
                suggested_fix=suggested_fix,
                confidence=confidence
            ))
        
        return ReviewFeedback(
            summary=data["summary"],
            strengths=data["strengths"],
            issues=processed_issues,
            recommendations=data["recommendations"]
        )
    
    except json.JSONDecodeError:
        # Fallback for non-JSON responses
        return process_unstructured_response(response)
```

### Fix Extraction and Validation

1. **Fix Parsing**
   - Extracts code changes from suggestions
   - Identifies affected lines
   - Normalizes code formatting

2. **Fix Validation**
   - Syntax checking
   - Semantic validation when possible
   - Safety assessment

3. **Fix Application Preparation**
   - Generates unified diffs
   - Creates apply/reject options
   - Prepares for interactive application

## Token Optimization Strategies

### Context Optimization

1. **Code Chunking**
   - Splits large files into manageable chunks
   - Preserves critical context across chunks
   - Maintains function and class boundaries

2. **Context Prioritization**
   - Includes most relevant code sections
   - Prioritizes code referenced by static analysis
   - Includes function signatures and docstrings

3. **Information Compression**
   - Removes unnecessary whitespace and comments
   - Summarizes repetitive patterns
   - Condenses static analysis results

### Example Chunking Algorithm

```python
def chunk_code_for_llm(code: str, max_tokens: int) -> List[CodeChunk]:
    """Split code into chunks optimized for LLM processing."""
    # Parse code into AST
    tree = ast.parse(code)
    
    # Extract functions and classes
    nodes = extract_top_level_nodes(tree)
    
    # Estimate token counts
    node_tokens = [(node, estimate_tokens(ast.unparse(node))) for node in nodes]
    
    # Create optimal chunks
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for node, tokens in node_tokens:
        # If single node exceeds token limit, split further
        if tokens > max_tokens:
            sub_chunks = split_large_node(node, max_tokens)
            chunks.extend(sub_chunks)
            continue
            
        # If adding node would exceed limit, start new chunk
        if current_tokens + tokens > max_tokens and current_chunk:
            chunks.append(CodeChunk(nodes=current_chunk))
            current_chunk = []
            current_tokens = 0
            
        # Add node to current chunk
        current_chunk.append(node)
        current_tokens += tokens
    
    # Add final chunk if not empty
    if current_chunk:
        chunks.append(CodeChunk(nodes=current_chunk))
        
    return chunks
```

### Token Usage Monitoring

1. **Token Counting**
   - Estimates token usage before API calls
   - Tracks actual token usage
   - Optimizes for token efficiency

2. **Budget Management**
   - Sets token budgets for different operations
   - Allocates tokens based on task importance
   - Implements adaptive strategies based on results

3. **Caching Strategy**
   - Caches responses for similar inputs
   - Implements efficient cache invalidation
   - Provides cache statistics and management

## AI-Specific Optimizations

### Model-Specific Tuning

1. **Parameter Optimization**
   - Model-specific temperature settings
   - Optimal top_p and frequency penalty
   - Context window utilization

2. **Prompt Engineering**
   - Model-specific prompt formats
   - Instruction optimization
   - Example selection

3. **Response Handling**
   - Model-specific parsing strategies
   - Error handling adaptations
   - Confidence calibration

### Example Model Configuration

```python
MODEL_CONFIGS = {
    "gpt-4": {
        "temperature": 0.3,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "max_tokens": 4000,
        "prompt_template": "templates/gpt4_review.txt",
        "chunk_size": 8000,
        "supports_streaming": True
    },
    "codellama": {
        "temperature": 0.2,
        "top_p": 0.95,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.1,
        "max_tokens": 2000,
        "prompt_template": "templates/codellama_review.txt",
        "chunk_size": 4000,
        "supports_streaming": True
    },
    "claude-3-opus-20240229": {
        "temperature": 0.3,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "max_tokens": 4000,
        "prompt_template": "templates/claude_review.txt",
        "chunk_size": 10000,
        "supports_streaming": True
    }
}
```

## AI-Powered Features

### 1. Code Review

**Purpose**: Analyze code for issues and improvements

**AI Capabilities**:
- Identify logical errors
- Suggest best practices
- Detect security vulnerabilities
- Recommend performance improvements
- Provide educational explanations

**Implementation**:
- Combines static analysis with LLM insights
- Prioritizes issues by severity and confidence
- Provides actionable suggestions
- Includes educational context

### 2. Code Explanation

**Purpose**: Explain code functionality and patterns

**AI Capabilities**:
- Summarize code purpose
- Explain complex algorithms
- Document undocumented code
- Identify design patterns
- Provide learning resources

**Implementation**:
- Analyzes code structure and flow
- Generates natural language explanations
- Identifies key components and relationships
- Provides different detail levels

### 3. Code Comparison

**Purpose**: Compare different versions of code

**AI Capabilities**:
- Identify functional changes
- Assess impact of changes
- Detect potential regressions
- Suggest further improvements
- Summarize change rationale

**Implementation**:
- Analyzes diff between versions
- Focuses on semantic changes
- Provides high-level summary
- Highlights critical differences

### 4. Fix Generation

**Purpose**: Generate fixes for identified issues

**AI Capabilities**:
- Create syntactically correct fixes
- Maintain code style consistency
- Preserve functionality
- Consider edge cases
- Explain fix rationale

**Implementation**:
- Generates specific code changes
- Validates syntax and semantics
- Assesses fix safety
- Provides application options

## Prompt Template Management

### Template Organization

1. **Base Templates**
   - Core templates for common operations
   - Extensible with variables
   - Documented with examples

2. **Specialized Templates**
   - Language-specific templates
   - Task-specific templates
   - Focus-specific templates

3. **Custom Templates**
   - User-defined templates
   - Project-specific templates
   - Team-shared templates

### Template Storage

Templates are stored in the `.claude/commands/` directory with the following structure:

```
.claude/commands/
├── code_review.prompt       # General code review
├── fix_suggestion.prompt    # Fix generation
├── security_audit.prompt    # Security-focused review
├── performance_optimization.prompt  # Performance-focused review
├── custom/                  # Custom templates
│   ├── team_standards.prompt
│   └── project_specific.prompt
└── languages/               # Language-specific templates
    ├── python.prompt
    ├── javascript.prompt
    └── typescript.prompt
```

### Template Rendering

Templates are rendered using a Jinja2-based system:

```python
def render_template(template_name: str, context: Dict[str, Any]) -> str:
    """Render a prompt template with the given context."""
    template_path = find_template_path(template_name)
    
    with open(template_path, "r") as f:
        template_content = f.read()
    
    # Create Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(template_path)),
        undefined=jinja2.StrictUndefined
    )
    
    # Add custom filters
    env.filters["truncate_code"] = truncate_code
    env.filters["format_issues"] = format_issues
    
    # Render template
    template = env.from_string(template_content)
    return template.render(**context)
```

## AI Memory and Context Management

### Context Persistence

1. **Session Context**
   - Maintains context within a session
   - Tracks previous interactions
   - Preserves key insights

2. **Project Context**
   - Stores project-specific knowledge
   - Maintains architectural understanding
   - Preserves coding patterns and standards

3. **User Preferences**
   - Remembers user preferences
   - Adapts to user feedback
   - Personalizes recommendations

### Context Storage

Context is stored in structured formats:

```python
class ProjectContext:
    """Persistent context for a project."""
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.context_file = os.path.join(project_path, ".vaahai", "context.json")
        self.context = self._load_context()
    
    def _load_context(self) -> Dict[str, Any]:
        """Load context from file or initialize new context."""
        if os.path.exists(self.context_file):
            with open(self.context_file, "r") as f:
                return json.load(f)
        return {
            "architecture": {},
            "patterns": {},
            "standards": {},
            "knowledge": {},
            "history": []
        }
    
    def save(self):
        """Save context to file."""
        os.makedirs(os.path.dirname(self.context_file), exist_ok=True)
        with open(self.context_file, "w") as f:
            json.dump(self.context, f, indent=2)
    
    def update_architecture(self, component: str, description: str):
        """Update architectural knowledge."""
        self.context["architecture"][component] = description
        self.save()
    
    def add_pattern(self, pattern_name: str, description: str, example: str):
        """Add a code pattern."""
        self.context["patterns"][pattern_name] = {
            "description": description,
            "example": example
        }
        self.save()
    
    def add_to_history(self, file_path: str, action: str, timestamp: float):
        """Add an entry to history."""
        self.context["history"].append({
            "file_path": file_path,
            "action": action,
            "timestamp": timestamp
        })
        # Limit history size
        if len(self.context["history"]) > 100:
            self.context["history"] = self.context["history"][-100:]
        self.save()
```

### Context Utilization

Context is used to enhance AI interactions:

```python
def create_review_context(
    file_path: str,
    code: str,
    analysis_results: List[AnalysisResult],
    project_context: ProjectContext,
    user_context: Optional[str] = None
) -> Dict[str, Any]:
    """Create context for code review."""
    # Basic context
    context = {
        "file_path": file_path,
        "code": code,
        "language": detect_language(file_path),
        "analysis_results": format_analysis_results(analysis_results),
        "user_context": user_context or ""
    }
    
    # Add project architecture context
    file_rel_path = os.path.relpath(file_path, project_context.project_path)
    component = identify_component(file_rel_path, project_context)
    if component and component in project_context.context["architecture"]:
        context["architecture"] = project_context.context["architecture"][component]
    
    # Add relevant patterns
    context["patterns"] = identify_relevant_patterns(code, project_context)
    
    # Add relevant standards
    context["standards"] = identify_relevant_standards(file_path, project_context)
    
    # Add relevant history
    context["history"] = get_file_history(file_path, project_context)
    
    return context
```

## AI Feedback Loop

### Feedback Collection

1. **Explicit Feedback**
   - User ratings of review quality
   - Fix acceptance/rejection statistics
   - Direct user comments

2. **Implicit Feedback**
   - Fix application patterns
   - Command usage patterns
   - Session duration and engagement

3. **Performance Metrics**
   - False positive/negative rates
   - Fix success rates
   - Response time and quality

### Feedback Utilization

Feedback is used to improve the system:

```python
def process_feedback(
    review_id: str,
    feedback: ReviewFeedback,
    accepted_fixes: List[Fix],
    rejected_fixes: List[Fix],
    user_rating: Optional[int] = None,
    user_comments: Optional[str] = None
) -> None:
    """Process user feedback to improve the system."""
    # Record feedback
    feedback_record = {
        "review_id": review_id,
        "timestamp": time.time(),
        "accepted_fixes": len(accepted_fixes),
        "rejected_fixes": len(rejected_fixes),
        "user_rating": user_rating,
        "user_comments": user_comments
    }
    
    # Analyze fix patterns
    if accepted_fixes or rejected_fixes:
        analyze_fix_patterns(accepted_fixes, rejected_fixes)
    
    # Update prompt effectiveness metrics
    update_prompt_metrics(review_id, feedback, user_rating)
    
    # Store feedback for analysis
    store_feedback(feedback_record)
    
    # Trigger model tuning if enough new data
    check_and_trigger_tuning()
```

### Continuous Improvement

The system uses feedback for continuous improvement:

1. **Prompt Refinement**
   - Adjusts prompts based on effectiveness
   - Tests variations with A/B testing
   - Incorporates successful patterns

2. **Model Selection**
   - Evaluates model performance
   - Selects optimal models for tasks
   - Adjusts parameters based on results

3. **Feature Enhancement**
   - Identifies feature gaps
   - Prioritizes improvements
   - Implements user-requested enhancements

## Security and Privacy Considerations

### Data Handling

1. **Code Privacy**
   - Local LLM options for sensitive code
   - Minimized data transmission
   - Data retention policies

2. **API Key Security**
   - Secure storage of API keys
   - Environment variable usage
   - Key rotation support

3. **Data Minimization**
   - Sends only necessary code
   - Filters sensitive information
   - Provides transparency controls

### Implementation Example

```python
def prepare_code_for_llm(code: str, file_path: str, config: ConfigManager) -> str:
    """Prepare code for sending to LLM with privacy considerations."""
    # Check privacy settings
    privacy_level = config.get("privacy.level", "standard")
    
    # Apply privacy filters
    if privacy_level == "high":
        # Remove comments that might contain sensitive info
        code = remove_comments(code)
        
        # Redact potential secrets
        code = redact_secrets(code)
        
        # Anonymize identifiers if requested
        if config.get("privacy.anonymize_identifiers", False):
            code = anonymize_identifiers(code)
    
    # Log what's being sent (without the actual code)
    logger.info(f"Preparing code from {file_path} for LLM analysis")
    
    return code
```

## Conclusion

This AI integration guide provides a comprehensive overview of how AI capabilities are integrated into the Vaahai code review tool. By following these patterns and best practices, the system can effectively leverage LLMs to provide valuable code insights while maintaining security, performance, and usability.
