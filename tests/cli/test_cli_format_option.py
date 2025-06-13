"""Tests for the --format option and InquirerPy prompt in the review CLI command."""

import tempfile

import pytest
from typer.testing import CliRunner

from vaahai.cli.main import app

runner = CliRunner(mix_stderr=False)

@pytest.mark.parametrize("fmt", ["rich", "markdown", "html", "interactive"])
def test_format_option(fmt):
    """Ensure --format option is accepted and propagated."""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = runner.invoke(app, ["review", "run", temp_dir, "--format", fmt, "--depth", "quick"], input="\n")
        # Typer exits with code 0 on success
        assert result.exit_code == 0, result.stderr
        assert "Report format:" in result.stdout
        assert fmt in result.stdout
