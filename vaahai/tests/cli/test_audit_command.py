"""
Tests for VaahAI audit command.

This module contains tests to verify that the audit command and its subcommands
function correctly.
"""

import pytest
import tempfile
from pathlib import Path
from typer.testing import CliRunner
from vaahai.cli.main import app

runner = CliRunner()


def test_audit_run_command_with_directory():
    """Test that the audit run command works with a directory path."""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = runner.invoke(app, ["audit", "run", temp_dir])
        assert result.exit_code == 0
        assert "Security & Compliance Audit" in result.stdout
        assert temp_dir in result.stdout
        assert "Security Checks: Enabled" in result.stdout


def test_audit_run_command_with_options():
    """Test that the audit run command works with various options."""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = runner.invoke(
            app, 
            [
                "audit", 
                "run", 
                temp_dir, 
                "--no-security", 
                "--compliance", 
                "owasp", 
                "--exclude", 
                "node_modules"
            ]
        )
        assert result.exit_code == 0
        assert "Security & Compliance Audit" in result.stdout
        assert "Security Checks: Disabled" in result.stdout
        assert "Compliance Standard: owasp" in result.stdout
        assert "Exclusions: node_modules" in result.stdout
