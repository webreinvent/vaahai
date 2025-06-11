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
    async def slow_run():
        await asyncio.sleep(0.01)  # Simulate delay
        return {"status": "success", "response": "Hello from VaahAI!"}
    mock_agent.run.side_effect = slow_run
    mock_create_agent.return_value = mock_agent

    # Run the CLI command
    result = runner.invoke(helloworld_app, [])

    # Check that the spinner context manager was entered
    assert mock_spinner.called
    # Check output
    assert "Hello World agent response generated successfully!" in result.output
    assert "Hello from VaahAI!" in result.output
