# Vaahai API Reference

## Core Modules

### Configuration Module

```python
from vaahai.config import ConfigManager

# Get configuration instance
config = ConfigManager()

# Get configuration value
api_key = config.get("openai.api_key")

# Set configuration value
config.set("openai.api_key", "your-api-key")

# Save configuration
config.save()

# Validate configuration
is_valid, errors = config.validate()
```

### Agent Factory

```python
from vaahai.agents import AgentFactory

# Create an agent
language_detector = AgentFactory.create("language_detector", config=config)

# Run agent
result = language_detector.run(file_path="/path/to/file.py")
```

### Command Handlers

```python
from vaahai.commands import ReviewCommand

# Create command handler
review_cmd = ReviewCommand(config=config)

# Execute command
result = review_cmd.execute(
    path="/path/to/code",
    output_format="markdown",
    depth="standard"
)
```

## Agent APIs

### Base Agent

All agents inherit from the `VaahaiAgent` base class which provides common functionality:

```python
from vaahai.agents.base import VaahaiAgent

class CustomAgent(VaahaiAgent):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        
    def run(self, *args, **kwargs):
        # Agent-specific implementation
        pass
```

### Language Detector Agent

```python
from vaahai.agents import LanguageDetectorAgent

# Create agent
detector = LanguageDetectorAgent(config=config)

# Detect language for a file
result = detector.detect_file("/path/to/file.py")
# Returns: {"language": "python", "version": "3.8+", "confidence": 0.95}

# Detect languages in a directory
results = detector.detect_directory("/path/to/project")
# Returns: {"files": [...], "summary": {"python": 60%, "javascript": 30%, "other": 10%}}
```

### Framework Detector Agent

```python
from vaahai.agents import FrameworkDetectorAgent

# Create agent
detector = FrameworkDetectorAgent(config=config)

# Detect frameworks
result = detector.detect("/path/to/project")
# Returns: {"frameworks": ["django", "react"], "confidence": 0.9}
```

### Reviewer Agent

```python
from vaahai.agents import ReviewerAgent

# Create agent
reviewer = ReviewerAgent(config=config)

# Review code
result = reviewer.review(
    path="/path/to/code",
    focus="quality",  # or "security", "performance", "all"
    depth="standard"  # or "deep", "quick"
)
```

### Auditor Agent

```python
from vaahai.agents import AuditorAgent

# Create agent
auditor = AuditorAgent(config=config)

# Audit code
result = auditor.audit(
    path="/path/to/code",
    focus=["security", "compliance"],
    standards=["pci-dss", "owasp-top-10"]
)
```

### Reporter Agent

```python
from vaahai.agents import ReporterAgent

# Create agent
reporter = ReporterAgent(config=config)

# Generate report
report = reporter.generate(
    data=review_results,
    format="markdown"  # or "html", "terminal"
)
```

### Applier Agent

```python
from vaahai.agents import ApplierAgent

# Create agent
applier = ApplierAgent(config=config)

# Apply changes
result = applier.apply(
    changes=suggested_changes,
    path="/path/to/file.py",
    interactive=True  # Ask for confirmation before each change
)
```

## Autogen Integration

### Creating Autogen Agents

```python
from vaahai.agents.autogen import create_assistant_agent, create_user_proxy_agent

# Create an assistant agent
assistant = create_assistant_agent(
    name="code_reviewer",
    system_message="You are a code review expert...",
    llm_config=config.get("llm")
)

# Create a user proxy agent
user_proxy = create_user_proxy_agent(
    name="user_proxy",
    human_input_mode="NEVER"
)
```

### Setting Up Group Chat

```python
from vaahai.agents.autogen import create_group_chat

# Create a group chat with multiple agents
group_chat = create_group_chat(
    agents=[language_detector, framework_detector, reviewer, reporter],
    messages=[],
    max_round=10
)

# Create a group chat manager
manager = create_group_chat_manager(group_chat=group_chat)

# Initiate the chat
manager.initiate_chat(
    message="Review the code in /path/to/project"
)
```

## Utility Functions

```python
from vaahai.utils import file_utils, output_utils

# Check if a file is binary
is_binary = file_utils.is_binary_file("/path/to/file")

# Get file extension
ext = file_utils.get_extension("/path/to/file.py")  # Returns: "py"

# Format output as table
table = output_utils.as_table(data, headers=["File", "Language", "Issues"])

# Format output as markdown
md = output_utils.as_markdown(data)
```

## CLI Integration

```python
import typer
from vaahai.commands import ReviewCommand

app = typer.Typer()

@app.command()
def review(
    path: str = typer.Argument(..., help="Path to file or directory to review"),
    output: str = typer.Option("terminal", help="Output format")
):
    """Review code for quality and best practices."""
    cmd = ReviewCommand()
    result = cmd.execute(path=path, output_format=output)
    typer.echo(result)
```
