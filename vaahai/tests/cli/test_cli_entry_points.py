"""
Tests for VaahAI CLI entry points.

This module contains tests to verify that all CLI commands are properly registered
and accessible through the main entry point.
"""

import pytest
from typer.testing import CliRunner
from vaahai.cli.main import app

runner = CliRunner()


def test_main_help():
    """Test that the main CLI help command works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "vaahai" in result.stdout
    assert "Commands" in result.stdout


def test_helloworld_command():
    """Test that the helloworld command is registered and accessible."""
    result = runner.invoke(app, ["helloworld", "--help"])
    assert result.exit_code == 0
    assert "helloworld" in result.stdout


def test_config_command():
    """Test that the config command is registered and accessible."""
    result = runner.invoke(app, ["config", "--help"])
    assert result.exit_code == 0
    assert "config" in result.stdout


def test_review_command():
    """Test that the review command is registered and accessible."""
    result = runner.invoke(app, ["review", "--help"])
    assert result.exit_code == 0
    assert "review" in result.stdout


def test_audit_command():
    """Test that the audit command is registered and accessible."""
    result = runner.invoke(app, ["audit", "--help"])
    assert result.exit_code == 0
    assert "audit" in result.stdout


def test_version_command():
    """Test that the version command is registered and accessible."""
    result = runner.invoke(app, ["version", "--help"])
    assert result.exit_code == 0
    assert "version" in result.stdout
