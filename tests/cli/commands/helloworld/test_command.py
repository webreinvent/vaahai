import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
import asyncio

from vaahai.cli.commands.helloworld.command import helloworld_app

@pytest.fixture
def runner():
    return CliRunner()

@patch("vaahai.cli.commands.helloworld.command.AgentFactory.create_agent")
@patch("vaahai.cli.commands.helloworld.command.progress_spinner")
def test_helloworld_loader_shows_spinner(mock_spinner, mock_create_agent, runner):
    # Mock the agent and its run method
    mock_agent = MagicMock()
    async def slow_run(location=None):
        await asyncio.sleep(0.01)  # Simulate delay
        return {"status": "success", "response": f"Hello from VaahAI! Location: {location}"}
    mock_agent.run.side_effect = slow_run
    mock_create_agent.return_value = mock_agent

    # Run the CLI command
    result = runner.invoke(helloworld_app, [])

    # Check that the spinner context manager was entered
    assert mock_spinner.called
    # Check output
    assert "Hello World agent response generated successfully!" in result.output
    assert "Hello from VaahAI! Location:" in result.output

@patch("vaahai.cli.commands.helloworld.command.AgentFactory.create_agent")
@patch("vaahai.cli.commands.helloworld.command.progress_spinner")
@patch("vaahai.cli.commands.helloworld.command.detect_user_location")
def test_helloworld_location_personalization(mock_detect_location, mock_spinner, mock_create_agent, runner):
    # Force a specific location
    mock_detect_location.return_value = "IN"
    mock_agent = MagicMock()
    async def run(location=None):
        return {"status": "success", "response": f"Namaste! Here's a joke for India. Location: {location}"}
    mock_agent.run.side_effect = run
    mock_create_agent.return_value = mock_agent

    result = runner.invoke(helloworld_app, [])
    assert mock_spinner.called
    assert "Namaste! Here's a joke for India" in result.output
    assert "Location: IN" in result.output
