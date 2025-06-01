"""
Tests for the Vaahai CLI application.

This module contains tests for the CLI application structure and commands.
"""

import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from vaahai.__main__ import app

# Create a CLI runner for testing
runner = CliRunner()

def test_version():
    """Test the --version flag."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Vaahai version:" in result.stdout

def test_help():
    """Test the --help flag."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Vaahai: AI-augmented code review CLI tool" in result.stdout
    
    # Check that all commands are listed
    assert "review" in result.stdout
    assert "analyze" in result.stdout
    assert "config" in result.stdout
    assert "explain" in result.stdout
    assert "document" in result.stdout

def test_review_help():
    """Test the review --help flag."""
    result = runner.invoke(app, ["review", "--help"])
    assert result.exit_code == 0
    assert "Review code with AI assistance" in result.stdout

def test_analyze_help():
    """Test the analyze --help flag."""
    result = runner.invoke(app, ["analyze", "--help"])
    assert result.exit_code == 0
    assert "Run static analysis on code" in result.stdout

def test_config_help():
    """Test the config --help flag."""
    result = runner.invoke(app, ["config", "--help"])
    assert result.exit_code == 0
    assert "Manage configuration" in result.stdout

def test_explain_help():
    """Test the explain --help flag."""
    result = runner.invoke(app, ["explain", "--help"])
    assert result.exit_code == 0
    assert "Generate code explanations" in result.stdout

def test_document_help():
    """Test the document --help flag."""
    result = runner.invoke(app, ["document", "--help"])
    assert result.exit_code == 0
    assert "Generate code documentation" in result.stdout
