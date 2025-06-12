#!/usr/bin/env python3
"""
Example demonstrating the use of VaahAI's Group Chat Manager.

This example shows how to create specialized agents and orchestrate them
in a group chat to collaboratively solve a task.
"""

import asyncio
import logging
from typing import Dict, Any, List

from vaahai.agents.base.agent_factory import AgentFactory
from vaahai.agents.utils.group_chat_manager import VaahAIGroupChatManager, GroupChatType, HumanInputMode

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def run_code_review_chat(code_snippet: str) -> Dict[str, Any]:
    """
    Run a code review chat with specialized agents.
    
    Args:
        code_snippet: The code to review.
        
    Returns:
        Dictionary containing the result and messages from the conversation.
    """
    # Create specialized agents for code review
    try:
        logger.info("Creating specialized agents for code review...")
        
        # Create a language detection agent
        language_detector = AgentFactory.create_agent("language_detector", {
            "name": "LanguageDetector",
            "system_message": "You are a programming language detection specialist. Your role is to identify the programming language, framework, and version used in code snippets.",
            "_test_mode": True  # For example purposes
        })
        
        # Create a code review agent
        code_reviewer = AgentFactory.create_agent("code_reviewer", {
            "name": "CodeReviewer",
            "system_message": "You are a code review specialist. Your role is to review code for bugs, performance issues, and best practices.",
            "_test_mode": True  # For example purposes
        })
        
        # Create a security audit agent
        security_auditor = AgentFactory.create_agent("security_auditor", {
            "name": "SecurityAuditor",
            "system_message": "You are a security audit specialist. Your role is to identify security vulnerabilities and suggest fixes.",
            "_test_mode": True  # For example purposes
        })
        
        # Create a report generation agent
        report_generator = AgentFactory.create_agent("report_generator", {
            "name": "ReportGenerator",
            "system_message": "You are a report generation specialist. Your role is to summarize findings and create a final report.",
            "_test_mode": True  # For example purposes
        })
        
        # Configure the group chat
        config = {
            "max_rounds": 10,
            "allow_repeat_speaker": False,
            "send_introductions": True,
            "termination": {
                "max_messages": 20,
                "completion_indicators": [
                    "Final Report:",
                    "Review Complete"
                ]
            },
            "_test_mode": True  # For example purposes
        }
        
        # Create the group chat manager
        logger.info("Creating group chat manager...")
        manager = VaahAIGroupChatManager(
            agents=[language_detector, code_reviewer, security_auditor, report_generator],
            config=config,
            chat_type=GroupChatType.ROUND_ROBIN,
            human_input_mode=HumanInputMode.NEVER
        )
        
        # Start the chat
        logger.info("Starting code review chat...")
        initial_message = f"Please review the following code:\n\n```\n{code_snippet}\n```"
        result = await manager.start_chat(initial_message)
        
        # Get the chat history
        history = manager.get_chat_history()
        
        logger.info("Code review completed.")
        return result
        
    except Exception as e:
        logger.error(f"Error running code review chat: {str(e)}")
        raise


async def run_custom_selector_chat(question: str) -> Dict[str, Any]:
    """
    Run a chat with a custom selector function.
    
    Args:
        question: The question to answer.
        
    Returns:
        Dictionary containing the result and messages from the conversation.
    """
    try:
        logger.info("Creating specialized agents for question answering...")
        
        # Create specialized agents
        math_expert = AgentFactory.create_agent("math_expert", {
            "name": "MathExpert",
            "system_message": "You are a mathematics expert. Your role is to solve mathematical problems.",
            "_test_mode": True  # For example purposes
        })
        
        coding_expert = AgentFactory.create_agent("coding_expert", {
            "name": "CodingExpert",
            "system_message": "You are a coding expert. Your role is to write and explain code.",
            "_test_mode": True  # For example purposes
        })
        
        history_expert = AgentFactory.create_agent("history_expert", {
            "name": "HistoryExpert",
            "system_message": "You are a history expert. Your role is to provide historical context and facts.",
            "_test_mode": True  # For example purposes
        })
        
        coordinator = AgentFactory.create_agent("coordinator", {
            "name": "Coordinator",
            "system_message": "You are a coordinator. Your role is to direct questions to the appropriate expert and summarize their responses.",
            "_test_mode": True  # For example purposes
        })
        
        # Define a custom selector function
        def select_next_agent(group_chat, messages):
            """
            Select the next agent based on the message content.
            
            Args:
                group_chat: The group chat instance.
                messages: List of messages in the conversation.
                
            Returns:
                The next agent to speak.
            """
            if not messages:
                # Start with the coordinator
                return next(agent for agent in group_chat.agents if agent.name == "Coordinator")
            
            last_message = messages[-1]["content"].lower()
            
            # Let the coordinator select the next expert
            if messages[-1]["sender"] == "Coordinator":
                if "math" in last_message or "calculation" in last_message:
                    return next(agent for agent in group_chat.agents if agent.name == "MathExpert")
                elif "code" in last_message or "programming" in last_message:
                    return next(agent for agent in group_chat.agents if agent.name == "CodingExpert")
                elif "history" in last_message or "past" in last_message:
                    return next(agent for agent in group_chat.agents if agent.name == "HistoryExpert")
            
            # After an expert speaks, return to the coordinator
            return next(agent for agent in group_chat.agents if agent.name == "Coordinator")
        
        # Configure the group chat
        config = {
            "max_rounds": 10,
            "allow_repeat_speaker": False,
            "send_introductions": True,
            "selection_function": select_next_agent,
            "termination": {
                "max_messages": 20,
                "completion_indicators": [
                    "Final Answer:",
                    "Question Answered"
                ]
            },
            "_test_mode": True  # For example purposes
        }
        
        # Create the group chat manager
        logger.info("Creating group chat manager with custom selector...")
        manager = VaahAIGroupChatManager(
            agents=[coordinator, math_expert, coding_expert, history_expert],
            config=config,
            chat_type=GroupChatType.SELECTOR,
            human_input_mode=HumanInputMode.NEVER
        )
        
        # Start the chat
        logger.info("Starting question answering chat...")
        initial_message = f"Please answer the following question: {question}"
        result = await manager.start_chat(initial_message)
        
        logger.info("Question answering completed.")
        return result
        
    except Exception as e:
        logger.error(f"Error running custom selector chat: {str(e)}")
        raise


async def main():
    """Run the example."""
    print("VaahAI Group Chat Manager Example")
    print("=================================")
    
    # Example 1: Code Review Chat
    print("\n1. Running Code Review Chat Example...")
    code_snippet = """
def calculate_factorial(n):
    if n < 0:
        return None
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
    """
    
    result = await run_code_review_chat(code_snippet)
    print("\nCode Review Result:")
    if result["messages"]:
        for message in result["messages"]:
            print(f"\n[{message.get('sender', 'Unknown')}]")
            print(message.get('content', ''))
    
    # Example 2: Custom Selector Chat
    print("\n\n2. Running Custom Selector Chat Example...")
    question = "What is the Fibonacci sequence and can you provide a Python function to calculate it?"
    
    result = await run_custom_selector_chat(question)
    print("\nQuestion Answering Result:")
    if result["messages"]:
        for message in result["messages"]:
            print(f"\n[{message.get('sender', 'Unknown')}]")
            print(message.get('content', ''))


if __name__ == "__main__":
    asyncio.run(main())
