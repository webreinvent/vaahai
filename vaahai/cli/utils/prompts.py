"""
Interactive prompt utilities for VaahAI CLI.

This module provides utility functions for creating consistent interactive
prompts using InquirerPy across all CLI commands.
"""

from typing import List, Dict, Any, Optional, Union, Callable
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator, EmptyInputValidator


def text_prompt(
    message: str,
    default: Optional[str] = None,
    validate: bool = False,
    transformer: Optional[Callable[[str], str]] = None,
) -> str:
    """
    Display a text input prompt.
    
    Args:
        message: The prompt message to display
        default: Optional default value
        validate: Whether to validate that input is not empty
        transformer: Optional function to transform the input
        
    Returns:
        The user's input as a string
    """
    validator = EmptyInputValidator() if validate else None
    return inquirer.text(
        message=message,
        default=default,
        validate=validator,
        transformer=transformer,
    ).execute()


def password_prompt(
    message: str,
    validate: bool = False,
) -> str:
    """
    Display a password input prompt (input is masked).
    
    Args:
        message: The prompt message to display
        validate: Whether to validate that input is not empty
        
    Returns:
        The user's input as a string
    """
    validator = EmptyInputValidator() if validate else None
    return inquirer.secret(
        message=message,
        validate=validator,
    ).execute()


def confirm_prompt(
    message: str,
    default: bool = False,
) -> bool:
    """
    Display a yes/no confirmation prompt.
    
    Args:
        message: The prompt message to display
        default: Default value (True for Yes, False for No)
        
    Returns:
        Boolean representing the user's choice
    """
    return inquirer.confirm(
        message=message,
        default=default,
    ).execute()


def select_prompt(
    message: str,
    choices: List[Union[str, Choice]],
    default: Optional[str] = None,
) -> str:
    """
    Display a selection prompt with a list of choices.
    
    Args:
        message: The prompt message to display
        choices: List of choices (strings or Choice objects)
        default: Optional default choice
        
    Returns:
        The selected choice
    """
    return inquirer.select(
        message=message,
        choices=choices,
        default=default,
    ).execute()


def multiselect_prompt(
    message: str,
    choices: List[Union[str, Choice]],
    min_selections: int = 0,
    max_selections: Optional[int] = None,
) -> List[str]:
    """
    Display a multi-selection prompt allowing multiple choices.
    
    Args:
        message: The prompt message to display
        choices: List of choices (strings or Choice objects)
        min_selections: Minimum number of selections required
        max_selections: Maximum number of selections allowed
        
    Returns:
        List of selected choices
    """
    return inquirer.checkbox(
        message=message,
        choices=choices,
        min_selections=min_selections,
        max_selections=max_selections,
    ).execute()


def path_prompt(
    message: str,
    default: Optional[str] = None,
    only_directories: bool = False,
    only_files: bool = False,
) -> str:
    """
    Display a prompt for file or directory path input with validation.
    
    Args:
        message: The prompt message to display
        default: Optional default path
        only_directories: Whether to only accept directories
        only_files: Whether to only accept files
        
    Returns:
        The validated path as a string
    """
    validator = PathValidator(
        is_dir=only_directories,
        is_file=only_files,
    )
    return inquirer.filepath(
        message=message,
        default=default,
        validate=validator,
    ).execute()


def editor_prompt(
    message: str,
    default: str = "",
    file_extension: str = ".txt",
) -> str:
    """
    Open an editor for multi-line text input.
    
    Args:
        message: The prompt message to display
        default: Optional default text
        file_extension: File extension for syntax highlighting
        
    Returns:
        The text entered in the editor
    """
    return inquirer.editor(
        message=message,
        default=default,
        file_extension=file_extension,
    ).execute()
