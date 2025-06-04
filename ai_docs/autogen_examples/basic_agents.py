#!/usr/bin/env python3
"""
Basic Autogen Agents Example for VaahAI

This example demonstrates how to create and use basic Autogen agents
that could be integrated into the VaahAI project.
"""

import asyncio
from typing import Dict, Any, List

# Note: These imports are based on Autogen's structure and would need to be installed
# pip install -U "autogen-agentchat" "autogen-ext[openai]"
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def create_code_reviewer_agent(model_client) -> AssistantAgent:
    """
    Create a code reviewer agent that can analyze code quality.
    
    Args:
        model_client: The LLM client to use for the agent
        
    Returns:
        An AssistantAgent configured for code review
    """
    system_message = """
    You are a code reviewer agent specialized in identifying code quality issues.
    Analyze the provided code for:
    1. Potential bugs
    2. Performance issues
    3. Readability concerns
    4. Best practice violations
    
    Provide specific, actionable feedback with examples of how to improve the code.
    """
    
    return AssistantAgent(
        name="code_reviewer",
        system_message=system_message,
        model_client=model_client
    )


async def create_security_auditor_agent(model_client) -> AssistantAgent:
    """
    Create a security auditor agent that can identify security vulnerabilities.
    
    Args:
        model_client: The LLM client to use for the agent
        
    Returns:
        An AssistantAgent configured for security auditing
    """
    system_message = """
    You are a security auditor agent specialized in identifying security vulnerabilities.
    Analyze the provided code for:
    1. Injection vulnerabilities
    2. Authentication issues
    3. Data exposure risks
    4. Security misconfigurations
    5. Use of components with known vulnerabilities
    
    Provide specific, actionable feedback with examples of how to fix security issues.
    """
    
    return AssistantAgent(
        name="security_auditor",
        system_message=system_message,
        model_client=model_client
    )


async def create_reporter_agent(model_client) -> AssistantAgent:
    """
    Create a reporter agent that can summarize findings from other agents.
    
    Args:
        model_client: The LLM client to use for the agent
        
    Returns:
        An AssistantAgent configured for reporting
    """
    system_message = """
    You are a reporter agent specialized in summarizing and formatting findings.
    Your job is to:
    1. Collect findings from the code reviewer and security auditor
    2. Organize them by priority and category
    3. Format them in a clear, actionable report
    4. Highlight the most critical issues that should be addressed first
    
    Present your report in markdown format with appropriate sections and formatting.
    """
    
    return AssistantAgent(
        name="reporter",
        system_message=system_message,
        model_client=model_client
    )


async def analyze_code_with_agents(code: str, api_key: str) -> Dict[str, Any]:
    """
    Analyze code using a team of specialized agents.
    
    Args:
        code: The code to analyze
        api_key: OpenAI API key
        
    Returns:
        A dictionary containing the analysis results
    """
    # Initialize the model client with OpenAI
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=api_key
    )
    
    try:
        # Create specialized agents
        code_reviewer = await create_code_reviewer_agent(model_client)
        security_auditor = await create_security_auditor_agent(model_client)
        reporter = await create_reporter_agent(model_client)
        user_proxy = UserProxyAgent("user_proxy")
        
        # Create a group chat with all agents
        group_chat = RoundRobinGroupChat(
            agents=[user_proxy, code_reviewer, security_auditor, reporter],
            max_round=10  # Limit the conversation to 10 rounds
        )
        
        # Start the conversation with the code to analyze
        task = f"""
        Please analyze the following code:
        
        ```
        {code}
        ```
        
        Code reviewer: Please identify code quality issues.
        Security auditor: Please identify security vulnerabilities.
        Reporter: Please summarize the findings in a well-formatted report.
        """
        
        # Run the group chat
        result = await group_chat.run(task)
        
        return {
            "success": True,
            "report": result,
            "agents_used": ["code_reviewer", "security_auditor", "reporter"]
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        # Clean up resources
        await model_client.close()


async def main():
    """
    Example usage of the code analysis functionality.
    """
    # Sample code to analyze
    sample_code = """
    def get_user_data(user_id):
        # Connect to database
        conn = connect_to_db()
        
        # Fetch user data - SECURITY ISSUE: SQL Injection vulnerability
        query = "SELECT * FROM users WHERE id = " + user_id
        result = conn.execute(query)
        
        # PERFORMANCE ISSUE: Not closing database connection
        return result.fetchone()
    
    def calculate_total(items):
        # CODE QUALITY ISSUE: Inefficient calculation
        total = 0
        for i in range(len(items)):
            total = total + items[i]['price']
        return total
    """
    
    # Replace with your actual API key
    api_key = "YOUR_OPENAI_API_KEY"
    
    # Run the analysis
    print("Starting code analysis with Autogen agents...")
    results = await analyze_code_with_agents(sample_code, api_key)
    
    if results["success"]:
        print("\nAnalysis completed successfully!")
        print("\nReport:")
        print(results["report"])
    else:
        print(f"\nAnalysis failed: {results['error']}")


if __name__ == "__main__":
    asyncio.run(main())
