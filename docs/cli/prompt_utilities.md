# VaahAI CLI Prompt Utilities

This document describes the interactive prompt utilities available in the VaahAI CLI, powered by InquirerPy.

## Overview

The VaahAI CLI provides a set of interactive prompt utilities that make it easy to collect user input in a consistent and user-friendly way. These utilities are built on top of the InquirerPy library and are styled to match the VaahAI CLI's Rich-based output.

All prompt utilities handle non-interactive environments gracefully by using default values or raising appropriate errors when required input cannot be collected.

## Basic Usage

```python
from vaahai.cli.utils.prompts import text_prompt, confirm_prompt, select_prompt

# Simple text input
name = text_prompt("What is your name?", default="User")

# Confirmation
if confirm_prompt("Do you want to continue?", default=True):
    # User confirmed
    pass

# Selection from a list
color = select_prompt("Choose a color", ["Red", "Green", "Blue"])
```

## Available Prompt Types

### Text Input

```python
from vaahai.cli.utils.prompts import text_prompt

name = text_prompt(
    message="What is your name?",
    default="User",
    validate=True,  # Ensures input is not empty
    transformer=lambda x: x.upper(),  # Optional transformation
    instruction="Enter your full name"  # Optional longer instruction
)
```

### Password Input

```python
from vaahai.cli.utils.prompts import password_prompt

password = password_prompt(
    message="Enter your password",
    validate=True,  # Ensures input is not empty
    instruction="Password will not be displayed as you type"
)
```

### Confirmation

```python
from vaahai.cli.utils.prompts import confirm_prompt

result = confirm_prompt(
    message="Do you want to continue?",
    default=True,  # Default to Yes
    instruction="Press Y for Yes or N for No"
)
```

### Single Selection

```python
from vaahai.cli.utils.prompts import select_prompt

color = select_prompt(
    message="Choose a color",
    choices=["Red", "Green", "Blue", "Yellow"],
    default="Blue",
    instruction="Use arrow keys to navigate"
)
```

### Multiple Selection

```python
from vaahai.cli.utils.prompts import multiselect_prompt

languages = multiselect_prompt(
    message="Select programming languages",
    choices=["Python", "JavaScript", "Go", "Rust"],
    min_selections=1,  # Require at least one selection
    max_selections=3,  # Allow at most three selections
    default=["Python"],  # Pre-select Python
    instruction="Use space to select, enter to confirm"
)
```

### Fuzzy Search Selection

```python
from vaahai.cli.utils.prompts import fuzzy_prompt

country = fuzzy_prompt(
    message="Select your country",
    choices=["United States", "Canada", "United Kingdom", "..."],
    default="United States",
    instruction="Type to search",
    max_height=10  # Limit the height of the selection list
)
```

### Number Input

```python
from vaahai.cli.utils.prompts import number_prompt

age = number_prompt(
    message="Enter your age",
    default=25,
    min_allowed=18,
    max_allowed=100,
    float_allowed=False,  # Only allow integers
    instruction="Must be between 18 and 100"
)
```

### File/Directory Path Selection

```python
from vaahai.cli.utils.prompts import path_prompt

file_path = path_prompt(
    message="Select a file",
    default="/home/user/documents",
    only_files=True,  # Only allow files, not directories
    instruction="Must be an existing file"
)

dir_path = path_prompt(
    message="Select a directory",
    default="/home/user",
    only_directories=True,  # Only allow directories, not files
    instruction="Must be an existing directory"
)
```

### Multi-line Text Editor

```python
from vaahai.cli.utils.prompts import editor_prompt

content = editor_prompt(
    message="Write a description",
    default="Initial content",
    file_extension=".md",  # For syntax highlighting
    instruction="Your default editor will open"
)
```

## Advanced Usage

### Custom Choice Objects

```python
from vaahai.cli.utils.prompts import select_prompt, create_choice

choices = [
    create_choice("Option A", value="a"),
    create_choice("Option B", value="b"),
    create_choice("Option C (disabled)", value="c", disabled=True),
    create_choice("Option D (pre-selected)", value="d", enabled=True)
]

result = select_prompt("Select an option", choices)
```

### Non-Interactive Mode Handling

All prompt utilities check if the current environment is a TTY (interactive terminal) before prompting. In non-interactive environments:

1. If a default value is provided, it will be used and a message will be printed
2. If no default is available and input is required, a RuntimeError will be raised

```python
# In a non-interactive environment (e.g., CI/CD pipeline):
name = text_prompt("What is your name?", default="CI User")
# Will print: "What is your name?: Using default value: CI User"
# And return: "CI User"

# Without a default:
try:
    password = password_prompt("Enter password:")
except RuntimeError as e:
    # Will raise: "Cannot prompt for password in non-interactive mode: Enter password"
    pass
```

## Styling

The prompt utilities use a consistent style that matches the VaahAI CLI's Rich-based output. The style is defined in `VAAHAI_PROMPT_STYLE` and uses the same color scheme as the Rich theme.

## Demo

To see all prompt types in action, run:

```bash
vaahai dev prompt-showcase
```

This will run a showcase of all available prompt types with examples and explanations.

## Integration with Rich

The prompt utilities are designed to work seamlessly with the Rich-based console output utilities. For example:

```python
from vaahai.cli.utils.console import print_header, print_key_value
from vaahai.cli.utils.prompts import text_prompt

print_header("User Information")
name = text_prompt("What is your name?")
print_key_value("Name", name)
```
