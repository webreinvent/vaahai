"""
InquirerPy prompt showcase for VaahAI CLI.

This module demonstrates the InquirerPy prompt capabilities of the VaahAI CLI.
It serves as both a test and an example of how to use the prompt utilities.
"""

import typer
import time
from pathlib import Path
from typing import Optional, List

from vaahai.cli.utils.console import (
    console,
    print_header,
    print_section,
    print_success,
    print_info,
    print_code,
    print_key_value,
    format_highlight,
)

from vaahai.cli.utils.prompts import (
    text_prompt,
    password_prompt,
    confirm_prompt,
    select_prompt,
    multiselect_prompt,
    path_prompt,
    editor_prompt,
    fuzzy_prompt,
    number_prompt,
    create_choice,
)

prompt_showcase_app = typer.Typer(help="Demonstrate InquirerPy prompt capabilities")


@prompt_showcase_app.callback()
def callback(ctx: typer.Context):
    """Showcase InquirerPy prompt capabilities."""
    if ctx.invoked_subcommand is None:
        run_showcase()


def run_showcase():
    """Run the InquirerPy prompt showcase."""
    print_header("InquirerPy Prompt Showcase", "Demonstrating interactive prompt capabilities")
    
    # Basic text input
    print_section("Text Input")
    print_info("Simple text input with default value and validation")
    name = text_prompt(
        message="What is your name?",
        default="User",
        validate=True,
        instruction="Enter your name (cannot be empty)"
    )
    print_key_value("You entered", name)
    
    # Password input
    print_section("Password Input")
    print_info("Password input with masked characters")
    password = password_prompt(
        message="Enter a password",
        validate=True,
        instruction="Password will not be displayed as you type"
    )
    print_key_value("Password length", str(len(password)))
    
    # Confirmation
    print_section("Confirmation")
    print_info("Yes/No confirmation prompt")
    confirmed = confirm_prompt(
        message="Do you like interactive prompts?",
        default=True,
        instruction="Press Y for Yes or N for No"
    )
    print_key_value("Your response", "Yes" if confirmed else "No")
    
    # Selection
    print_section("Selection")
    print_info("Select one option from a list")
    color_choices = ["Red", "Green", "Blue", "Yellow", "Purple"]
    color = select_prompt(
        message="Select your favorite color",
        choices=color_choices,
        default="Blue",
        instruction="Use arrow keys to navigate"
    )
    print_key_value("You selected", color)
    
    # Advanced selection with Choice objects
    print_section("Advanced Selection")
    print_info("Selection with custom Choice objects")
    framework_choices = [
        create_choice("React", value="react", disabled=False),
        create_choice("Vue", value="vue", disabled=False),
        create_choice("Angular", value="angular", disabled=False),
        create_choice("Svelte", value="svelte", disabled=False),
        create_choice("Legacy Framework", value="legacy", disabled=True),
    ]
    framework = select_prompt(
        message="Select a frontend framework",
        choices=framework_choices,
        instruction="Disabled options cannot be selected"
    )
    print_key_value("You selected", framework)
    
    # Multi-selection
    print_section("Multi-selection")
    print_info("Select multiple options from a list")
    language_choices = ["Python", "JavaScript", "TypeScript", "Go", "Rust", "Java"]
    languages = multiselect_prompt(
        message="Select programming languages you know",
        choices=language_choices,
        min_selections=1,
        max_selections=3,
        instruction="Use space to select, enter to confirm (min: 1, max: 3)"
    )
    print_key_value("You selected", ", ".join(languages))
    
    # Fuzzy search
    print_section("Fuzzy Search")
    print_info("Type to search through a large list of options")
    country_choices = [
        "United States", "Canada", "United Kingdom", "Australia", 
        "Germany", "France", "Japan", "China", "India", "Brazil",
        "Mexico", "South Africa", "Russia", "Italy", "Spain"
    ]
    country = fuzzy_prompt(
        message="Select your country",
        choices=country_choices,
        instruction="Type to search"
    )
    print_key_value("You selected", country)
    
    # Number input
    print_section("Number Input")
    print_info("Enter a numeric value with constraints")
    age = number_prompt(
        message="Enter your age",
        default=25,
        min_allowed=18,
        max_allowed=100,
        instruction="Must be between 18 and 100"
    )
    print_key_value("You entered", str(age))
    
    # Path selection
    print_section("Path Selection")
    print_info("Select a file path with validation")
    file_path = path_prompt(
        message="Select a file",
        default=str(Path.home()),
        only_files=True,
        instruction="Must be an existing file"
    )
    print_key_value("Selected file", file_path)
    
    # Editor
    if confirm_prompt("Would you like to try the editor prompt?", default=False):
        print_section("Editor")
        print_info("Opens your default editor for multi-line text input")
        content = editor_prompt(
            message="Write a short note",
            default="Hello,\n\nThis is a test note.\n\nRegards,\nUser",
            file_extension=".md",
            instruction="Your default editor will open"
        )
        print_code(content, language="markdown")
    
    # Summary
    print_section("Summary")
    print_success("You've completed the InquirerPy prompt showcase!")
    print_info("These prompt utilities can be used throughout the VaahAI CLI to create interactive and user-friendly experiences.")
    print_info(f"Check out the {format_highlight('vaahai.cli.utils.prompts')} module for more details.")


@prompt_showcase_app.command()
def all():
    """Run all prompt showcase examples."""
    showcase_all()


@prompt_showcase_app.command()
def basic():
    """Demonstrate basic prompt types."""
    showcase_basic()


@prompt_showcase_app.command()
def selection():
    """Demonstrate selection prompt types."""
    showcase_selection()


def showcase_all():
    """Run all prompt showcase examples."""
    run_showcase()


def showcase_basic():
    """Demonstrate basic prompt types."""
    print_header("Basic Prompt Types", "Text, Password, and Confirmation")
    
    name = text_prompt("What is your name?", default="User")
    print_key_value("Name", name)
    
    if confirm_prompt("Would you like to try a password prompt?", default=False):
        password = password_prompt("Enter a test password")
        print_key_value("Password length", str(len(password)))
    
    print_success("Basic prompt showcase completed!")


def showcase_selection():
    """Demonstrate selection prompt types."""
    print_header("Selection Prompt Types", "Single, Multiple, and Fuzzy Selection")
    
    # Single selection
    options = ["Option A", "Option B", "Option C", "Option D"]
    selected = select_prompt("Select an option", options)
    print_key_value("Selected", selected)
    
    # Multiple selection
    selected_multiple = multiselect_prompt(
        "Select multiple options",
        options,
        min_selections=1
    )
    print_key_value("Selected", ", ".join(selected_multiple))
    
    # Fuzzy selection
    items = [f"Item {i}" for i in range(1, 21)]
    fuzzy_selected = fuzzy_prompt("Search for an item", items)
    print_key_value("Selected", fuzzy_selected)
    
    print_success("Selection prompt showcase completed!")


if __name__ == "__main__":
    prompt_showcase_app()
