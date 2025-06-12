# VaahAI Tool Registry

This document provides an overview of the VaahAI Tool Registry system, which enables dynamic registration, configuration, and execution of code analysis tools.

## Overview

The Tool Registry system provides a flexible framework for creating, registering, and using tools for code analysis and other operations. It follows a similar pattern to the Agent Registry, using decorator-based registration and a factory pattern for tool creation.

## Core Components

### ToolBase

`ToolBase` is an abstract base class that defines the interface for all tools in the VaahAI system. All concrete tool implementations must inherit from this class and implement its abstract methods.

Key features:
- Abstract `execute()` method that must be implemented by subclasses
- Abstract `_validate_config()` method for configuration validation
- Metadata attributes for tool discovery and filtering
- Lifecycle management with initialization and cleanup

```python
from vaahai.tools.base import ToolBase, ToolRegistry

@ToolRegistry.register("my_tool")
class MyTool(ToolBase):
    # Tool metadata
    input_type = "code"
    output_type = "analysis_results"
    version = "0.1.0"
    author = "Your Name"
    tags = ["code_quality", "analysis"]
    requirements = ["some-package>=1.0.0"]
    
    def _validate_config(self) -> None:
        # Validate the tool configuration
        if "some_option" in self.config and not isinstance(self.config["some_option"], bool):
            raise ValueError("some_option must be a boolean")
    
    def execute(self, input_data):
        # Implement the tool's functionality
        return {"result": "analysis complete"}
```

### ToolRegistry

`ToolRegistry` manages the registration and lookup of tool classes. It provides methods for registering tools, retrieving tool classes by type, and filtering tools by various criteria.

Key features:
- Decorator-based registration
- Tool class lookup by type
- Metadata caching for efficient queries
- Filtering by tags, input types, and output types

```python
# Register a tool
@ToolRegistry.register("my_tool")
class MyTool(ToolBase):
    # Tool implementation...

# Check if a tool is registered
is_registered = ToolRegistry.is_registered("my_tool")

# Get a tool class
tool_class = ToolRegistry.get_tool_class("my_tool")

# List all registered tools
tools = ToolRegistry.list_registered_tools()

# Filter tools by tag
code_quality_tools = ToolRegistry.get_tools_by_tag("code_quality")

# Filter tools by input type
code_input_tools = ToolRegistry.get_tools_by_input_type("code")

# Filter tools by output type
analysis_output_tools = ToolRegistry.get_tools_by_output_type("analysis_results")
```

### ToolFactory

`ToolFactory` creates tool instances from configurations. It handles the creation of individual tools as well as tool pipelines.

Key features:
- Tool creation from type and configuration
- Tool creation from configuration files
- Tool pipeline creation
- Tool availability checking
- Tool metadata retrieval

```python
from vaahai.tools.base import ToolFactory

# Create a tool from type and configuration
tool = ToolFactory.create_tool("my_tool", {"option": "value"})

# Create a tool from a configuration file
tool = ToolFactory.create_tool_from_file("path/to/config.yaml")

# Check if a tool is available
is_available = ToolFactory.is_tool_available("my_tool")

# Get tool metadata
metadata = ToolFactory.get_tool_metadata("my_tool")

# Create a tool pipeline
pipeline_config = [
    {"type": "tool1", "option1": "value1"},
    {"type": "tool2", "option2": "value2"}
]
tools = ToolFactory.create_tool_pipeline(pipeline_config)
```

### ToolConfigLoader

`ToolConfigLoader` handles the loading, processing, and validation of tool configurations.

Key features:
- Configuration loading from YAML or JSON files
- Environment variable substitution in configurations
- Configuration validation against schemas
- Default configuration merging

```python
from vaahai.tools.config_loader import ToolConfigLoader

# Load a configuration from a file
config = ToolConfigLoader.load_config_from_file("path/to/config.yaml")

# Process environment variables in a configuration
config = ToolConfigLoader.process_env_vars(config)

# Validate and prepare a configuration
config = ToolConfigLoader.validate_and_prepare_config("my_tool", config)
```

## Tool Pipeline

The `ToolPipeline` class allows multiple tools to be chained together, with the output of one tool being passed as input to the next tool in the pipeline.

```python
from vaahai.tools.utils.pipeline import ToolPipeline

# Create a pipeline from tool instances
pipeline = ToolPipeline([tool1, tool2, tool3])

# Create a pipeline from a configuration
pipeline = ToolPipeline.from_config([
    {"type": "tool1", "option1": "value1"},
    {"type": "tool2", "option2": "value2"}
])

# Execute the pipeline
result = pipeline.execute(input_data)

# Add a tool to the pipeline
pipeline.add_tool(tool4)

# Insert a tool at a specific position
pipeline.insert_tool(1, tool5)

# Remove a tool from the pipeline
removed_tool = pipeline.remove_tool(2)
```

## Tool Schemas

Tool configurations are validated against schemas defined in the `vaahai.tools.schemas` module. Default configurations are provided for different tool types, and validation functions ensure that configurations are valid.

```python
from vaahai.tools.schemas import get_default_config, validate_tool_config

# Get the default configuration for a tool type
default_config = get_default_config("code_linter")

# Validate a configuration
errors = validate_tool_config("code_linter", config)
if errors:
    print(f"Configuration errors: {errors}")
```

## Example Tools

The VaahAI Tool Registry comes with example tool implementations:

### CodeLinterTool

A tool for linting code and identifying potential issues based on configurable rules.

```python
from vaahai.tools.base import ToolFactory

# Create a code linter tool
linter = ToolFactory.create_tool("code_linter", {
    "severity_levels": ["error", "warning"],
    "ignore_patterns": ["# noqa"]
})

# Lint some code
result = linter.execute(code)
```

### StaticAnalyzerTool

A tool for static analysis of code to identify patterns, dependencies, and structure.

```python
from vaahai.tools.base import ToolFactory

# Create a static analyzer tool
analyzer = ToolFactory.create_tool("static_analyzer", {
    "depth": 3,
    "include_patterns": ["*.py", "*.js"],
    "exclude_patterns": ["**/node_modules/**"]
})

# Analyze some code
result = analyzer.execute(code)
```

## Creating Custom Tools

To create a custom tool, follow these steps:

1. Create a new class that inherits from `ToolBase`
2. Register the class with the `ToolRegistry` using the `@ToolRegistry.register` decorator
3. Define metadata attributes for the tool
4. Implement the `_validate_config()` method to validate the tool's configuration
5. Implement the `execute()` method to perform the tool's functionality

```python
from vaahai.tools.base import ToolBase, ToolRegistry

@ToolRegistry.register("custom_tool")
class CustomTool(ToolBase):
    # Tool metadata
    input_type = "custom_input"
    output_type = "custom_output"
    version = "0.1.0"
    author = "Your Name"
    tags = ["custom", "example"]
    requirements = []
    
    def _validate_config(self) -> None:
        # Validate the tool configuration
        if "option" in self.config and not isinstance(self.config["option"], str):
            raise ValueError("option must be a string")
    
    def execute(self, input_data):
        # Implement the tool's functionality
        return {"result": f"Processed {input_data} with option {self.config.get('option', 'default')}"}
```

## Tool Configuration

Tools can be configured using YAML or JSON files. Here's an example configuration file:

```yaml
type: code_linter
enabled: true
timeout: 30
severity_levels:
  - error
  - warning
ignore_patterns:
  - "# noqa"
  - "# pragma: no cover"
```

Environment variables can be used in configuration files using the `${VAR_NAME}` syntax:

```yaml
type: code_linter
enabled: true
timeout: ${LINTER_TIMEOUT:-30}  # Use LINTER_TIMEOUT env var or default to 30
api_key: ${API_KEY}  # Use API_KEY env var (required)
```

## Best Practices

1. **Tool Design**
   - Keep tools focused on a single responsibility
   - Use clear input and output types
   - Document the tool's purpose and configuration options
   - Include appropriate tags for discovery

2. **Configuration**
   - Validate all configuration options
   - Provide sensible defaults
   - Use environment variables for sensitive information
   - Document all configuration options

3. **Error Handling**
   - Validate input data before processing
   - Provide clear error messages
   - Handle exceptions gracefully
   - Return structured error information when possible

4. **Performance**
   - Consider caching results for expensive operations
   - Use streaming for large inputs/outputs when appropriate
   - Implement timeout handling for long-running operations

## Example Usage

See the `examples/tool_registry_example.py` script for a complete example of using the Tool Registry system.
