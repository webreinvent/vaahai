# Vaahai: AI-Augmented Code Review CLI Tool

## Overview

Vaahai is a Python-based command-line tool that leverages Microsoft's AutoGen framework and large language models (LLMs) to perform automated, AI-augmented code reviews. The tool integrates static analysis tools with LLM capabilities to provide comprehensive, context-aware code reviews and suggestions for improvement. Vaahai can analyze code across multiple languages and frameworks, aggregate findings, and present them in a user-friendly format. It also offers the option to apply suggested changes directly to the codebase with user confirmation.

## Features

- **AI-Powered Code Reviews**: Utilizes LLMs (OpenAI GPT-4 or local models via Ollama) to provide intelligent code analysis
- **Static Analysis Integration**: Incorporates tools like pylint, flake8, bandit, and language-specific analyzers
- **Multi-Language Support**: Reviews code in Python, PHP, JavaScript, Vue, and other languages
- **Interactive Fixes**: Option to apply suggested changes with confirmation
- **Flexible Output**: Terminal, Markdown, or HTML output formats
- **Configurable**: User-defined settings for LLM selection, review depth, and output preferences
- **Extensible Architecture**: Modular design allows for adding new static analyzers and LLM providers

## Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| Programming Language | Python 3.9+ | Wide adoption, rich ecosystem for AI and CLI tools |
| CLI Framework | Typer | Modern, type-annotated interface with automatic help generation |
| Static Analysis | pylint, flake8, bandit, language-specific tools | Industry-standard tools with comprehensive rule sets |
| AI Orchestration | Microsoft AutoGen | Provides flexible agent-based architecture for LLM interactions |
| LLM Providers | OpenAI API, Ollama | Balance between cloud-based and local deployment options |
| Configuration | TOML | Human-readable, structured format with strong typing |
| Dependency Management | Poetry | Modern dependency management with lock files and virtual environments |
| Output Formatting | Rich, Markdown, Jinja2 | Flexible output options with syntax highlighting |

## CLI Specification

### Command Structure

```
vaahai [OPTIONS] COMMAND [ARGS]...
```

### Global Options

- `--verbose / -v`: Enable verbose output
- `--config PATH`: Path to custom config file
- `--output-format [terminal|markdown|html]`: Output format for results

### Commands

#### Review Command

```
vaahai review [OPTIONS] [PATH]
```

Reviews code at the specified path (file or directory).

**Options:**
- `--language / -l [python|php|js|vue|auto]`: Programming language (auto-detect if not specified)
- `--model / -m [gpt-4|gpt-3.5-turbo|local]`: LLM model to use
- `--depth / -d [quick|standard|thorough]`: Review depth
- `--apply / -a`: Interactively apply suggested changes
- `--output / -o PATH`: Save review to file
- `--include-pattern TEXT`: Files to include (glob pattern)
- `--exclude-pattern TEXT`: Files to exclude (glob pattern)
- `--max-files INTEGER`: Maximum number of files to review

#### Configure Command

```
vaahai config [OPTIONS]
```

Configure Vaahai settings.

**Options:**
- `--set KEY VALUE`: Set configuration value
- `--get KEY`: Get configuration value
- `--list`: List all configuration values
- `--reset`: Reset to default configuration

**Configuration Keys:**
- `openai.api_key`: OpenAI API key
- `ollama.host`: Ollama host address
- `default.model`: Default LLM model
- `default.output_format`: Default output format
- `default.review_depth`: Default review depth

#### Static Analysis Command

```
vaahai analyze [OPTIONS] [PATH]
```

Run only static analysis without LLM review.

**Options:**
- Similar to review command, but without LLM-specific options

## System Architecture & Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  CLI Interface  │────▶│  Code Scanner   │────▶│ Static Analyzers │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│ Change Applier  │◀────│  Review Format  │◀────│  AutoGen Agents │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │                 │
                                                │   LLM Provider  │
                                                │                 │
                                                └─────────────────┘
```

### Process Flow

1. **Input Processing**: CLI parses commands and options
2. **Code Scanning**: Identify files to analyze based on patterns and language
3. **Static Analysis**: Run appropriate static analyzers on code
4. **Context Building**: Aggregate static analysis results and code context
5. **Agent Orchestration**: AutoGen coordinates LLM interactions
6. **LLM Processing**: Send context to LLM for intelligent review
7. **Result Formatting**: Format review results for presentation
8. **Change Application**: Optionally apply suggested changes to files

## File/Module Structure

```
vaahai/
├── __init__.py
├── cli/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── review.py        # Review command implementation
│   │   ├── config.py        # Config command implementation
│   │   └── analyze.py       # Static analysis command
│   └── utils/
│       ├── __init__.py
│       └── output.py        # Output formatting utilities
├── core/
│   ├── __init__.py
│   ├── scanner.py           # Code scanning functionality
│   ├── config.py            # Configuration management
│   └── applier.py           # Change application logic
├── analyzers/
│   ├── __init__.py
│   ├── base.py              # Base analyzer class
│   ├── python/
│   │   ├── __init__.py
│   │   ├── pylint.py
│   │   ├── flake8.py
│   │   └── bandit.py
│   ├── php/
│   │   └── ...
│   ├── js/
│   │   └── ...
│   └── factory.py           # Analyzer factory
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py      # AutoGen orchestration
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── review.py        # Review prompts
│   │   └── fix.py           # Fix prompts
│   └── utils/
│       ├── __init__.py
│       └── context.py       # Context building
├── llm/
│   ├── __init__.py
│   ├── base.py              # Base LLM provider
│   ├── openai.py            # OpenAI implementation
│   └── ollama.py            # Ollama implementation
└── formatters/
    ├── __init__.py
    ├── base.py              # Base formatter
    ├── terminal.py          # Terminal output
    ├── markdown.py          # Markdown output
    └── html.py              # HTML output
```

## Extensibility

Vaahai is designed to be extensible in several key areas:

### Adding New Static Analyzers

1. Create a new analyzer class that inherits from `analyzers.base.BaseAnalyzer`
2. Implement the required methods: `analyze()`, `parse_results()`
3. Register the analyzer in the analyzer factory

```python
from vaahai.analyzers.base import BaseAnalyzer

class NewAnalyzer(BaseAnalyzer):
    def analyze(self, file_path):
        # Implementation
        pass
        
    def parse_results(self, raw_results):
        # Implementation
        pass
```

### Adding New LLM Providers

1. Create a new provider class that inherits from `llm.base.BaseLLMProvider`
2. Implement the required methods: `initialize()`, `generate()`
3. Register the provider in the LLM factory

```python
from vaahai.llm.base import BaseLLMProvider

class NewLLMProvider(BaseLLMProvider):
    def initialize(self):
        # Implementation
        pass
        
    def generate(self, prompt, options=None):
        # Implementation
        pass
```

### Adding New Output Formatters

1. Create a new formatter class that inherits from `formatters.base.BaseFormatter`
2. Implement the required methods: `format_review()`, `save()`
3. Register the formatter in the formatter factory

## Example AI Prompt

Below is an example of the prompt template used for code review:

```
You are an expert code reviewer with deep knowledge of software engineering principles, 
design patterns, and best practices for {language}.

I will provide you with:
1. Code to review
2. Static analysis results
3. Project context

Please provide a comprehensive code review that includes:

1. Overall assessment (1-2 sentences)
2. Key strengths
3. Issues identified, categorized as:
   - Critical: Must be fixed (security, bugs)
   - Important: Should be fixed (performance, maintainability)
   - Minor: Consider fixing (style, readability)
4. Specific recommendations for improvement
5. Code examples for suggested changes

For each issue:
- Reference the specific line number
- Explain why it's an issue
- Provide a clear solution

Static analysis results:
{static_analysis_results}

Code to review:
```{language}
{code}
```

Project context:
{project_context}
```

## Example Output

Here's an example of the review output in Markdown format:

```markdown
# Code Review: user_auth.py

## Overall Assessment
This authentication module has a solid foundation but contains several security vulnerabilities and performance issues that should be addressed.

## Key Strengths
- Well-organized module structure
- Good separation of concerns
- Comprehensive docstrings

## Issues

### Critical
1. **Insecure Password Storage** (Line 45)
   - Passwords are stored using MD5 hash which is cryptographically broken
   - **Fix**: Use argon2 or bcrypt for password hashing
   ```python
   # Before
   password_hash = hashlib.md5(password.encode()).hexdigest()
   
   # After
   import bcrypt
   password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
   ```

2. **SQL Injection Vulnerability** (Line 78)
   - Direct string interpolation in SQL query
   - **Fix**: Use parameterized queries
   ```python
   # Before
   query = f"SELECT * FROM users WHERE username = '{username}'"
   
   # After
   query = "SELECT * FROM users WHERE username = %s"
   cursor.execute(query, (username,))
   ```

### Important
1. **Inefficient Database Queries** (Line 92-105)
   - Multiple separate queries could be combined
   - **Fix**: Use a single query with JOIN
   ```python
   # Before
   user = get_user(user_id)
   permissions = get_permissions(user_id)
   
   # After
   query = """
       SELECT u.*, p.permission_name 
       FROM users u
       JOIN user_permissions up ON u.id = up.user_id
       JOIN permissions p ON up.permission_id = p.id
       WHERE u.id = %s
   ```
```

## Tool Configuration

Vaahai uses a TOML configuration file stored in the user's home directory (`~/.config/vaahai/config.toml`). Here's an example configuration:

```toml
[default]
model = "gpt-4"
output_format = "terminal"
review_depth = "standard"

[openai]
api_key = ""  # Set via config command for security

[ollama]
host = "http://localhost:11434"

[static_analysis]
python = ["pylint", "flake8", "bandit"]
php = ["phpcs", "phpstan"]
js = ["eslint"]
vue = ["eslint"]

[review]
include_patterns = ["*.py", "*.php", "*.js", "*.vue"]
exclude_patterns = ["**/vendor/**", "**/node_modules/**", "**/.git/**"]
max_files = 20

[output]
terminal_color = true
markdown_format = "github"
```

## Development Roadmap

### MVP (Minimum Viable Product)

1. **Phase 1: Core Framework**
   - Set up project structure and CLI framework
   - Create first hello world command
   - Make it publishable using poetry
   - Implement configuration management
   - Create a basic code scanner
   - Build simple LLM integration (OpenAI only)
   - Develop terminal output formatter
   - Support Python files only with pylint integration

2. **Phase 2: Enhanced Analysis**
   - Add multiple static analyzers for Python
   - Implement context building from static analysis
   - Create AutoGen agent orchestration
   - Add Markdown output formatter
   - Implement basic change application

3. **Phase 3: Extensibility**
   - Add support for PHP and JavaScript
   - Implement Ollama integration for local LLMs
   - Create analyzer and LLM provider factories
   - Add HTML output formatter
   - Improve documentation

### Future Enhancements

1. **Language Support Expansion**
   - Add support for more languages (Go, Rust, C#, etc.)
   - Integrate language-specific best practices

2. **Advanced AI Features**
   - Multi-agent conversations for complex reviews
   - Architectural analysis across multiple files
   - Learning from user feedback on suggestions

3. **Integration Features**
   - GitHub/GitLab integration for CI/CD
   - IDE plugins
   - Team collaboration features

## Installation & Usage

### Installation

```bash
# Using pip
pip install vaahai

# Using Poetry
poetry add vaahai

# From source
git clone https://github.com/webreinvent/vaahai.git
cd vaahai
poetry install
```

### Basic Usage

```bash
# Review a single file
vaahai review path/to/file.py

# Review a directory
vaahai review path/to/project/

# Review with specific model
vaahai review path/to/file.py --model gpt-4

# Review and apply changes
vaahai review path/to/file.py --apply

# Configure OpenAI API key
vaahai config --set openai.api_key YOUR_API_KEY
```

## Implementation Snippets

### CLI Entry Point (main.py)

```python
import typer
from typing import Optional
from pathlib import Path
from vaahai.cli.commands import review, config, analyze

app = typer.Typer(help="Vaahai: AI-augmented code review tool")

# Register commands
app.add_typer(review.app, name="review")
app.add_typer(config.app, name="config")
app.add_typer(analyze.app, name="analyze")

@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    config_path: Optional[Path] = typer.Option(
        None, "--config", help="Path to custom config file"
    ),
):
    """
    Vaahai: AI-augmented code review tool powered by AutoGen and LLMs.
    """
    # Initialize application
    pass

if __name__ == "__main__":
    app()
```

### AutoGen Orchestration (orchestrator.py)

```python
import autogen
from typing import Dict, List, Any
from vaahai.llm.base import BaseLLMProvider
from vaahai.agents.prompts.review import REVIEW_PROMPT_TEMPLATE

class ReviewOrchestrator:
    def __init__(self, llm_provider: BaseLLMProvider, config: Dict[str, Any]):
        self.llm_provider = llm_provider
        self.config = config
        self.agents = self._setup_agents()
        
    def _setup_agents(self):
        # Configure AutoGen agents
        reviewer = autogen.AssistantAgent(
            name="code_reviewer",
            llm_config={
                "config_list": [{"model": self.config["model"]}],
                "temperature": 0.2,
            },
            system_message="You are an expert code reviewer specializing in identifying bugs, security issues, and performance problems.",
        )
        
        fixer = autogen.AssistantAgent(
            name="code_fixer",
            llm_config={
                "config_list": [{"model": self.config["model"]}],
                "temperature": 0.2,
            },
            system_message="You are an expert at fixing code issues and implementing best practices.",
        )
        
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
        )
        
        return {
            "reviewer": reviewer,
            "fixer": fixer,
            "user_proxy": user_proxy
        }
        
    def generate_review(self, code: str, static_analysis_results: str, context: str, language: str) -> str:
        # Prepare prompt
        prompt = REVIEW_PROMPT_TEMPLATE.format(
            language=language,
            static_analysis_results=static_analysis_results,
            code=code,
            project_context=context
        )
        
        # Initialize chat
        self.agents["user_proxy"].initiate_chat(
            self.agents["reviewer"],
            message=prompt
        )
        
        # Extract review from chat history
        messages = self.agents["user_proxy"].chat_messages[self.agents["reviewer"].name]
        review_message = messages[-1]["content"]
        
        return review_message
```

### Static Analyzer Base Class (base.py)

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from pathlib import Path

class BaseAnalyzer(ABC):
    """Base class for all static analyzers"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
    @abstractmethod
    def analyze(self, file_path: Path) -> str:
        """
        Run the analyzer on the specified file
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Raw output from the analyzer
        """
        pass
        
    @abstractmethod
    def parse_results(self, raw_results: str) -> List[Dict[str, Any]]:
        """
        Parse the raw analyzer output into structured results
        
        Args:
            raw_results: Raw output from the analyzer
            
        Returns:
            List of issues found by the analyzer
        """
        pass
        
    def format_for_prompt(self, issues: List[Dict[str, Any]]) -> str:
        """
        Format the issues for inclusion in the LLM prompt
        
        Args:
            issues: List of issues found by the analyzer
            
        Returns:
            Formatted string for the LLM prompt
        """
        if not issues:
            return "No issues found."
            
        result = []
        for issue in issues:
            result.append(f"Line {issue['line']}: {issue['message']} ({issue['severity']})")
            
        return "\n".join(result)
```

### Change Applier (applier.py)

```python
import difflib
from typing import Dict, List, Any
from pathlib import Path
import typer

class ChangeApplier:
    """Applies suggested changes to code files"""
    
    def __init__(self, interactive: bool = True):
        self.interactive = interactive
        
    def parse_suggestions(self, review: str) -> List[Dict[str, Any]]:
        """
        Parse code suggestions from the review
        
        Args:
            review: The review text containing suggestions
            
        Returns:
            List of suggested changes
        """
        # Implementation to extract code blocks and their context
        # This is a simplified version - actual implementation would be more robust
        suggestions = []
        lines = review.split("\n")
        current_suggestion = None
        
        for line in lines:
            if "# Before" in line:
                current_suggestion = {"before": [], "after": [], "description": ""}
            elif "# After" in line and current_suggestion:
                current_suggestion["in_after"] = True
            elif line.startswith("```") and current_suggestion:
                if "in_after" in current_suggestion:
                    suggestions.append(current_suggestion)
                    current_suggestion = None
            elif current_suggestion:
                if "in_after" in current_suggestion:
                    current_suggestion["after"].append(line)
                else:
                    current_suggestion["before"].append(line)
                    
        return suggestions
        
    def apply_changes(self, file_path: Path, suggestions: List[Dict[str, Any]]) -> bool:
        """
        Apply suggested changes to a file
        
        Args:
            file_path: Path to the file to modify
            suggestions: List of suggested changes
            
        Returns:
            True if changes were applied, False otherwise
        """
        with open(file_path, "r") as f:
            content = f.read()
            
        modified_content = content
        
        for suggestion in suggestions:
            before = "\n".join(suggestion["before"])
            after = "\n".join(suggestion["after"])
            
            if before in modified_content:
                if self.interactive:
                    # Show diff
                    diff = difflib.unified_diff(
                        before.splitlines(True),
                        after.splitlines(True),
                        n=3
                    )
                    typer.echo("Suggested change:")
                    typer.echo("".join(diff))
                    
                    # Ask for confirmation
                    apply = typer.confirm("Apply this change?")
                    if apply:
                        modified_content = modified_content.replace(before, after)
                else:
                    modified_content = modified_content.replace(before, after)
        
        # Only write if content changed
        if modified_content != content:
            with open(file_path, "w") as f:
                f.write(modified_content)
            return True
            
        return False
```

This comprehensive documentation provides a clear roadmap for developing the Vaahai AI-augmented code review tool, with detailed specifications for its architecture, components, and implementation approach.