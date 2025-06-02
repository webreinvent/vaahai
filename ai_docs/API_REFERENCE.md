# Vaahai API Reference for AI Tools

This document provides detailed API reference information for the Vaahai AI-augmented code review CLI tool, specifically formatted for AI tools to understand the interfaces, functions, classes, and modules.

## Core Modules

### 1. Configuration Manager

{{ ... }}

### 2. Code Scanner

{{ ... }}

### 3. Autogen Multi-Agent System

**Module**: `vaahai.core.agents`

**Description**: Implements a multi-agent system using Microsoft's Autogen framework for sophisticated code review.

**Key Components**:

#### Agent Factory

```python
class AgentFactory:
    """Factory for creating specialized Autogen agents."""
    
    @staticmethod
    def create_language_detector(config: Dict[str, Any]) -> Agent:
        """Create a Language Detector agent."""
        pass
        
    @staticmethod
    def create_framework_detector(config: Dict[str, Any]) -> Agent:
        """Create a Framework/CMS Detector agent."""
        pass
        
    @staticmethod
    def create_standards_analyzer(config: Dict[str, Any]) -> Agent:
        """Create a Standards Analyzer agent."""
        pass
        
    @staticmethod
    def create_security_auditor(config: Dict[str, Any]) -> Agent:
        """Create a Security Auditor agent."""
        pass
        
    @staticmethod
    def create_review_coordinator(config: Dict[str, Any]) -> Agent:
        """Create a Review Coordinator agent."""
        pass
```

#### Group Chat Manager

```python
class ReviewGroupChatManager:
    """Manages the group chat for code review."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the group chat manager with configuration."""
        pass
        
    def setup_agents(self) -> None:
        """Set up all required agents for the review."""
        pass
        
    def initiate_review(self, code_context: Dict[str, Any]) -> Dict[str, Any]:
        """Start the review process with the given code context."""
        pass
        
    def process_results(self, chat_results: Any) -> Dict[str, Any]:
        """Process the results from the group chat."""
        pass
```

#### Agent Configuration

```python
class AgentConfig:
    """Configuration for Autogen agents."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize agent configuration from file or defaults."""
        pass
        
    def get_agent_config(self, agent_type: str) -> Dict[str, Any]:
        """Get configuration for a specific agent type."""
        pass
        
    def get_group_chat_config(self) -> Dict[str, Any]:
        """Get configuration for the group chat."""
        pass
```

#### Review Orchestrator

```python
class ReviewOrchestrator:
    """Orchestrates the entire review process using multiple agents."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the orchestrator with configuration."""
        pass
        
    def review_file(self, file_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Review a single file using the multi-agent system."""
        pass
        
    def review_directory(self, dir_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Review all files in a directory using the multi-agent system."""
        pass
        
    def format_results(self, results: Dict[str, Any], format_type: str) -> str:
        """Format the review results in the specified format."""
        pass
```

### 4. CLI Commands

**Module**: `vaahai.cli.commands`

**Description**: Implements the CLI commands for the Vaahai tool.

**Key Components**:

#### Review Command

```python
@app.command()
def review(
    path: str = typer.Argument(
        ...,
        help="Path to file or directory to review",
    ),
    output_format: OutputFormat = typer.Option(
        OutputFormat.TERMINAL,
        "--format", "-f",
        help="Output format for the review results",
    ),
    output_file: Optional[str] = typer.Option(
        None,
        "--output", "-o",
        help="File to write the review results to",
    ),
    focus: ReviewFocus = typer.Option(
        ReviewFocus.GENERAL,
        "--focus",
        help="Focus area for the review",
    ),
    depth: ReviewDepth = typer.Option(
        ReviewDepth.STANDARD,
        "--depth",
        help="Depth of the review",
    ),
    ignore_patterns: List[str] = typer.Option(
        [],
        "--ignore", "-i",
        help="Patterns to ignore during review",
    ),
    agent_config: Optional[str] = typer.Option(
        None,
        "--agent-config",
        help="Path to agent configuration file",
    ),
):
    """
    Review code using AI-augmented analysis.
    
    This command uses a multi-agent system powered by Autogen to perform
    sophisticated code review on files or directories.
    """
    pass
```

{{ ... }}

## Integration Interfaces

### 1. LLM Provider Interface

{{ ... }}

### 2. Autogen Integration

**Module**: `vaahai.core.agents.autogen_integration`

**Description**: Provides integration with the Autogen framework.

**Key Components**:

#### Autogen Setup

```python
def setup_autogen(config: Dict[str, Any]) -> None:
    """Set up Autogen with the given configuration."""
    pass
```

#### Agent Creation

```python
def create_agent(
    name: str,
    system_message: str,
    llm_config: Dict[str, Any],
    human_input_mode: str = "NEVER",
) -> Agent:
    """Create an Autogen agent with the given parameters."""
    pass
```

#### Group Chat Setup

```python
def setup_group_chat(
    agents: List[Agent],
    config: Dict[str, Any],
) -> GroupChat:
    """Set up a group chat with the given agents and configuration."""
    pass
```

#### Chat Manager

```python
def create_chat_manager(
    group_chat: GroupChat,
    config: Dict[str, Any],
) -> GroupChatManager:
    """Create a group chat manager for the given group chat."""
    pass
```

### 3. Output Formatters

{{ ... }}

## Configuration Schema

### 1. Main Configuration

{{ ... }}

### 2. Agent Configuration

```toml
# Agent configuration schema

[agents]
# Global agent settings
max_rounds = 10
termination_message = "REVIEW_COMPLETE"

[agents.language_detector]
name = "LanguageDetector"
model = "gpt-4"
temperature = 0.2
system_message = """You are a Language Detector Agent specialized in identifying programming languages.
Analyze the code and determine:
1. The primary programming language(s) used
2. Language version indicators if present
3. Any language-specific features or patterns
"""

[agents.framework_detector]
name = "FrameworkDetector"
model = "gpt-4"
temperature = 0.3
system_message = """You are a Framework Detector Agent specialized in identifying frameworks and libraries.
Analyze the code and determine:
1. Frameworks or libraries being used
2. Architectural patterns (MVC, MVVM, etc.)
3. Key dependencies and their relationships
"""

[agents.standards_analyzer]
name = "StandardsAnalyzer"
model = "gpt-4"
temperature = 0.3
system_message = """You are a Standards Analyzer Agent specialized in evaluating adherence to coding standards.
Analyze the code and determine:
1. Adherence to language-specific coding standards
2. Style consistency issues
3. Best practice violations
"""

[agents.security_auditor]
name = "SecurityAuditor"
model = "gpt-4"
temperature = 0.2
system_message = """You are a Security Auditor Agent specialized in identifying security vulnerabilities.
Analyze the code and determine:
1. Security vulnerabilities
2. Common security anti-patterns
3. Security best practice violations
"""

[agents.review_coordinator]
name = "ReviewCoordinator"
model = "gpt-4"
temperature = 0.3
system_message = """You are a Review Coordinator Agent responsible for orchestrating the code review process.
Your tasks include:
1. Dividing code into logical segments
2. Routing specific questions to specialized agents
3. Aggregating findings and generating a comprehensive report
"""

[group_chat]
max_rounds = 10
speaker_selection_method = "auto"
```

{{ ... }}
