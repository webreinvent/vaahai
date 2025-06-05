"""
VaahAI Agent Usage Example

This example demonstrates how to use the VaahAI agent implementations
to create and interact with different types of agents.
"""

import asyncio
import logging
from typing import Dict, Any

from vaahai.agents.factory import AgentFactory
from vaahai.agents.impl import (
    ConversationalAgent,
    AssistantAgent,
    UserProxyAgent,
    CodeReviewAgent
)


async def main():
    """Main function demonstrating agent usage."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting VaahAI agent example")

    # Create an agent factory
    factory = AgentFactory()
    
    # Create a conversational agent
    conversational_config = {
        "name": "ConversationalBot",
        "max_history_length": 10
    }
    conversational_agent = factory.create_agent("conversational", conversational_config)
    logger.info(f"Created agent: {conversational_agent.get_name()}")
    
    # Create an assistant agent with tools
    assistant_config = {
        "name": "AssistantBot",
        "system_prompt": "You are a helpful assistant that provides concise answers.",
        "tools": [
            {"name": "calculator", "description": "Performs calculations"},
            {"name": "web_search", "description": "Searches the web for information"}
        ]
    }
    assistant_agent = factory.create_agent("assistant", assistant_config)
    logger.info(f"Created agent: {assistant_agent.get_name()}")
    
    # Create a user proxy agent
    user_proxy_config = {
        "name": "UserProxy",
        "human_input_mode": "ALWAYS",
        "auto_reply": False
    }
    user_proxy_agent = factory.create_agent("user_proxy", user_proxy_config)
    logger.info(f"Created agent: {user_proxy_agent.get_name()}")
    
    # Create a specialized code review agent
    code_review_config = {
        "name": "CodeReviewer",
        "domain": "code_quality",
        "expertise": "python",
        "languages": ["python", "javascript"],
        "review_criteria": ["style", "complexity", "security"]
    }
    code_review_agent = factory.create_agent("code_review", code_review_config)
    logger.info(f"Created agent: {code_review_agent.get_name()}")
    
    # Demonstrate message processing
    message = "Hello, can you help me with a Python code review?"
    
    # Process message with different agents
    logger.info(f"Sending message to agents: '{message}'")
    
    response1 = await conversational_agent.process_message(message)
    logger.info(f"Response from {conversational_agent.get_name()}: {response1}")
    
    response2 = await assistant_agent.process_message(message)
    logger.info(f"Response from {assistant_agent.get_name()}: {response2}")
    
    response3 = await code_review_agent.process_message(message)
    logger.info(f"Response from {code_review_agent.get_name()}: {response3}")
    
    # Demonstrate agent capabilities
    logger.info("\nAgent capabilities:")
    logger.info(f"{conversational_agent.get_name()}: {conversational_agent.get_capabilities()}")
    logger.info(f"{assistant_agent.get_name()}: {assistant_agent.get_capabilities()}")
    logger.info(f"{user_proxy_agent.get_name()}: {user_proxy_agent.get_capabilities()}")
    logger.info(f"{code_review_agent.get_name()}: {code_review_agent.get_capabilities()}")
    
    # Demonstrate convenience methods
    logger.info("\nCreating agents using convenience methods:")
    
    assistant = AgentFactory.create_assistant_agent({
        "name": "QuickAssistant",
        "system_prompt": "You are a quick assistant."
    })
    logger.info(f"Created: {assistant.get_name()}")
    
    code_reviewer = AgentFactory.create_code_review_agent({
        "name": "QuickCodeReviewer",
        "domain": "code_quality",
        "expertise": "python"
    })
    logger.info(f"Created: {code_reviewer.get_name()}")


if __name__ == "__main__":
    asyncio.run(main())
