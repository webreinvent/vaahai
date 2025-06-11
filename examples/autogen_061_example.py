#!/usr/bin/env python
"""
Simple example of AutoGen 0.6.1 agent usage to understand the correct implementation.
This is used to study the message handling in AutoGen 0.6.1 for the VaahAI HelloWorldAgent.
"""

import asyncio
import logging
import os
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("autogen_example")

# Add the project root directory to the Python path to import vaahai modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

async def main():
    """Main function to test AutoGen 0.6.1 agent implementation."""
    try:
        # Import VaahAI config manager
        from vaahai.config.manager import ConfigManager
        
        # Import required AutoGen modules
        import autogen_agentchat
        import autogen_core
        from autogen_agentchat.agents import AssistantAgent
        from autogen_agentchat.messages import TextMessage
        from autogen_core import _cancellation_token
        from autogen_ext.models.openai import OpenAIChatCompletionClient

        logger.info("Successfully imported AutoGen packages")

        # Get API key from VaahAI config
        config_manager = ConfigManager()
        llm_config = config_manager.get("llm", {})
        openai_config = llm_config.get("providers", {}).get("openai", {})
        api_key = openai_config.get("api_key", "")
        
        if not api_key:
            logger.error("OpenAI API key not found in VaahAI config")
            logger.info("You can set it using: vaahai config set llm.providers.openai.api_key YOUR_API_KEY")
            return
            
        logger.info("Found OpenAI API key in VaahAI config")
            
        # Create a model client
        model_client = OpenAIChatCompletionClient(
            model="gpt-3.5-turbo",  # Use default model from AutoGen
            api_key=api_key
        )
        
        logger.info("Created model client")
        
        # Create an assistant agent
        system_message = "You are a helpful assistant named TestAgent. Be brief and friendly."
        agent = AssistantAgent(
            name="TestAgent",
            model_client=model_client,
            system_message=system_message
        )
        
        logger.info(f"Created agent: {agent.name}")
        
        # Create a cancellation token
        cancellation_token = _cancellation_token.CancellationToken()
        
        # Create a message
        message = TextMessage(
            content="Hello! Please introduce yourself briefly.",
            source="user"
        )
        
        logger.info(f"Created message: {message}")
        
        # Send message to agent
        logger.info("Sending message to agent...")
        response = await agent.on_messages([message], cancellation_token)
        
        # Log the response type and attributes
        logger.info(f"Response type: {type(response)}")
        logger.info(f"Response attributes: {dir(response)}")
        
        # Try to access different attributes to understand the response structure
        try:
            if hasattr(response, "content"):
                logger.info(f"Response.content: {response.content}")
            elif hasattr(response, "chat_message") and response.chat_message:
                logger.info(f"Response.chat_message: {response.chat_message}")
                if hasattr(response.chat_message, "content"):
                    logger.info(f"Response.chat_message.content: {response.chat_message.content}")
            elif hasattr(response, "inner_messages") and response.inner_messages:
                logger.info(f"Response.inner_messages length: {len(response.inner_messages)}")
                if response.inner_messages and hasattr(response.inner_messages[0], "content"):
                    logger.info(f"Response.inner_messages[0].content: {response.inner_messages[0].content}")
            elif hasattr(response, "message"):
                logger.info(f"Response.message: {response.message}")
                if hasattr(response.message, "content"):
                    logger.info(f"Response.message.content: {response.message.content}")
            elif hasattr(response, "messages"):
                logger.info(f"Response.messages: {response.messages}")
                if response.messages and hasattr(response.messages[0], "content"):
                    logger.info(f"Response.messages[0].content: {response.messages[0].content}")
            else:
                logger.info("Could not find content in response")
        except Exception as e:
            logger.error(f"Error accessing response attributes: {e}")
        
        # Print the successful result
        logger.info("Completed test of AutoGen 0.6.1 agent")
        
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
