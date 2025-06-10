#!/usr/bin/env python
"""
Example script demonstrating how to use the Hello World agent.

This script shows how to create and run the Hello World agent
with different configuration options.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from vaahai.agents import AgentFactory


def main():
    """
    Run the Hello World agent with different configurations.
    """
    print("VaahAI Hello World Agent Example")
    print("===============================\n")
    
    # Example 1: Run in test mode (no API key required)
    print("Example 1: Running in test mode")
    config = {
        "name": "HelloWorldAgent",
        "provider": "openai",
        "temperature": 0.7,
        "_test_mode": True
    }
    
    agent = AgentFactory.create_agent("hello_world", config)
    result = agent.run()
    
    print(f"Response: {result.get('response')}")
    print("\n")
    
    # Example 2: Run with API key from environment (if available)
    print("Example 2: Running with API key (if available)")
    if os.environ.get("OPENAI_API_KEY") or os.environ.get("VAAHAI_PROVIDERS_OPENAI_API_KEY"):
        try:
            config = {
                "name": "HelloWorldAgent",
                "provider": "openai",
                "temperature": 0.9,
                "_test_mode": False
            }
            
            agent = AgentFactory.create_agent("hello_world", config)
            result = agent.run()
            
            print(f"Response: {result.get('response')}")
        except Exception as e:
            print(f"Error running with API key: {str(e)}")
            print("Make sure you have set OPENAI_API_KEY or VAAHAI_PROVIDERS_OPENAI_API_KEY")
    else:
        print("Skipping Example 2: No API key found in environment variables")
    
    print("\nExample completed successfully!")


if __name__ == "__main__":
    main()
