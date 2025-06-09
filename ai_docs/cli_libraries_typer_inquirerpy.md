# Typer and InquirerPy: VaahAI CLI Libraries

This document provides a comprehensive overview of the two key libraries used in the VaahAI CLI implementation: Typer and InquirerPy.

## Typer: Modern CLI Framework

Typer is a Python library for building command-line interfaces (CLIs) that's built on top of Click. It leverages Python's type hints to create intuitive, type-safe CLI applications.

### Key Features

1. **Type-Based Parameter Definition**: Uses Python type annotations to define and validate CLI parameters
2. **Rich Help Text Generation**: Automatically generates help text from docstrings
3. **Command Hierarchies**: Supports nested command groups for organizing complex CLIs
4. **Callback Pattern**: Uses decorators and callbacks for command execution flow
5. **Rich Integration**: Works well with Rich for beautiful terminal output
6. **Completion Support**: Provides shell completion for commands and options

### Basic Usage

```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    print(f"Hello {name}")

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

if __name__ == "__main__":
    app()
```

### Command Groups

Typer allows organizing commands into hierarchical groups:

```python
main_app = typer.Typer()
sub_app = typer.Typer()

main_app.add_typer(sub_app, name="sub")

# Register commands to the main app
@main_app.command()
def main_command():
    """Main command."""
    print("Running main command")

# Register commands to the sub app
@sub_app.command()
def sub_command():
    """Sub command."""
    print("Running sub command")
```

### Callback Pattern

```python
@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """Runs when no subcommand is specified."""
    if ctx.invoked_subcommand is None:
        print("No subcommand was specified")
```

### VaahAI Implementation

In VaahAI, Typer is used to:

1. Create the main CLI application structure with command groups:
   - `core_app`: Essential VaahAI commands
   - `project_app`: Project analysis commands
   - `dev_app`: Development and testing commands

2. Register individual commands like `config`, `helloworld`, `review`, `audit`, and `version`

3. Define command parameters with type hints for automatic validation

4. Generate help text and usage information automatically

5. Handle command callbacks for proper execution flow

## InquirerPy: Interactive Prompts

InquirerPy is a Python port of Inquirer.js that provides interactive command-line prompts. It's a re-implementation of PyInquirer with bug fixes and additional features.

### Key Features

1. **Multiple Prompt Types**: Input, selection, confirmation, checkbox, etc.
2. **Two Syntax Options**: Classic (PyInquirer-compatible) and Alternate (more flexible)
3. **Customizable Styling**: Supports custom themes and styling
4. **Validation**: Built-in validation for user inputs
5. **Rich Integration**: Works well with Rich for styled output

### Classic Syntax

```python
from InquirerPy import prompt

questions = [
    {"type": "input", "message": "What's your name:", "name": "name"},
    {
        "type": "list",
        "message": "What's your favourite programming language:",
        "choices": ["Go", "Python", "Rust", "JavaScript"],
    },
    {"type": "confirm", "message": "Confirm?"},
]
result = prompt(questions)
name = result["name"]
fav_lang = result[1]
confirm = result[2]
```

### Alternate Syntax (Recommended)

```python
from InquirerPy import inquirer

name = inquirer.text(message="What's your name:").execute()
fav_lang = inquirer.select(
    message="What's your favourite programming language:",
    choices=["Go", "Python", "Rust", "JavaScript"],
).execute()
confirm = inquirer.confirm(message="Confirm?").execute()
```

### Available Prompt Types

1. **Text Input**: `inquirer.text()` - For free-form text input
2. **Password**: `inquirer.secret()` - For password input (masked)
3. **Selection**: `inquirer.select()` - For selecting from a list of options
4. **Checkbox**: `inquirer.checkbox()` - For selecting multiple items from a list
5. **Confirmation**: `inquirer.confirm()` - For yes/no questions
6. **Number**: `inquirer.number()` - For numeric input with validation
7. **Path**: `inquirer.filepath()` - For file/directory path input with validation
8. **Fuzzy**: `inquirer.fuzzy()` - For fuzzy search selection

### VaahAI Implementation

In VaahAI, InquirerPy is used to:

1. Create interactive configuration prompts in `vaahai config init`
2. Provide user-friendly selection interfaces for various options
3. Validate user input with custom validation rules
4. Create rich, interactive experiences in the CLI
5. Demonstrate prompt capabilities in the `prompt_showcase` command

## Integration in VaahAI

The VaahAI CLI combines Typer and InquirerPy to create a powerful and user-friendly command-line interface:

1. **Command Structure**: Typer provides the overall command structure, argument parsing, and help text generation
2. **User Interaction**: InquirerPy handles interactive user input with rich prompts
3. **Rich Output**: Both libraries integrate with Rich for beautiful terminal output
4. **Validation**: Both libraries provide validation for their respective domains (command arguments and interactive inputs)

### Best Practices

1. **Use Type Hints**: Always use Python type hints with Typer for automatic validation
2. **Provide Docstrings**: Add detailed docstrings to commands for automatic help text generation
3. **Use Command Groups**: Organize related commands into logical groups
4. **Prefer Alternate Syntax**: Use InquirerPy's alternate syntax for better IDE support and flexibility
5. **Handle Non-TTY Environments**: Always check if running in a TTY environment before using interactive prompts
6. **Provide Default Values**: Always provide sensible defaults for non-interactive mode

### Example: Command with Interactive Prompt

```python
import typer
from InquirerPy import inquirer
from vaahai.cli.utils.console import console
from vaahai.cli.utils.prompts import is_tty

app = typer.Typer()

@app.command()
def setup(name: str = None):
    """Set up a new project."""
    if name is None and is_tty():
        name = inquirer.text(
            message="Enter project name:",
            validate=lambda x: len(x) > 0,
        ).execute()
    elif name is None:
        console.print("[red]Error: Project name is required in non-interactive mode[/red]")
        raise typer.Exit(1)

    console.print(f"[green]Setting up project: {name}[/green]")
```

## Troubleshooting Common Issues

### Command Not Found

If a command is not showing up in the CLI help:
1. Ensure the command is properly registered with `app.add_typer()` or `@app.command()`
2. Check that the module containing the command is properly imported
3. Verify that the command name doesn't contain hyphens (use underscores instead)
4. Try reinstalling the package with `poetry install`

### Interactive Prompts Not Working

If interactive prompts are not working:
1. Check if running in a TTY environment with `is_tty()`
2. Provide fallback behavior for non-TTY environments
3. Ensure InquirerPy is properly installed
4. Check for version compatibility issues

### Command Registration Issues

If commands are not being properly registered:
1. Ensure the command module is imported in the parent module
2. Check that the command is added to the parent app with `add_typer()`
3. Verify that the command name follows Python identifier rules
4. Check for circular imports or import errors
