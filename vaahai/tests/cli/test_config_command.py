"""
Tests for VaahAI config command.

This module contains tests to verify that the config command and its subcommands
function correctly.
"""

import pytest
from typer.testing import CliRunner
from vaahai.cli.main import app

runner = CliRunner()


def test_config_init_command():
    """Test that the config init command runs without errors."""
    result = runner.invoke(app, ["config", "init"])
    assert result.exit_code == 0
    assert "Configuration Wizard" in result.stdout
    assert "VaahAI Configuration Wizard" in result.stdout


def test_config_show_command():
    """Test that the config show command runs without errors."""
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "Current Configuration" in result.stdout
    assert "VaahAI Configuration" in result.stdout
