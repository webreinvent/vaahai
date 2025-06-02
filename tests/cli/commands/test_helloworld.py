"""
Tests for the Hello World CLI command.
"""

import pytest
from typer.testing import CliRunner
from vaahai.cli.commands.helloworld import app as helloworld_app

runner = CliRunner()


def test_helloworld_command_default_message():
    """Test that the helloworld command works with default message."""
    result = runner.invoke(helloworld_app)
    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout


def test_helloworld_command_custom_message():
    """Test that the helloworld command works with custom message."""
    result = runner.invoke(helloworld_app, ["--message", "Custom CLI message"])
    assert result.exit_code == 0
    assert "Custom CLI message" in result.stdout


def test_helloworld_command_short_option():
    """Test that the helloworld command works with short option."""
    result = runner.invoke(helloworld_app, ["-m", "Short option message"])
    assert result.exit_code == 0
    assert "Short option message" in result.stdout
