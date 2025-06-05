#!/usr/bin/env python3
"""
Multi-Provider Agent Collaboration Example for VaahAI

This example demonstrates how to create a team of agents using different LLM providers
(OpenAI, Anthropic, and local models via Ollama) working together on a code analysis task.
"""

import asyncio
import os
from typing import Dict, Any, List, Optional

# Note: These imports are based on Autogen's structure and would need to be installed
# pip install -U "autogen-agentchat" "autogen-ext[openai,anthropic,ollama]"
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient


class LLMClientFactory:
    """Factory class to create LLM clients for different providers."""
    
    @staticmethod
    async def create_client(provider: str, model_name: str, api_key: Optional[str] = None):
        """
        Create an LLM client for the specified provider.
        
        Args:
            provider: The LLM provider (openai, anthropic, ollama)
            model_name: The model name to use
            api_key: API key for the provider (if required)
            
        Returns:
            An LLM client for the specified provider
        """
        if provider.lower() == "openai":
            return OpenAIChatCompletionClient(
                model=model_name,
                api_key=api_key or os.environ.get("OPENAI_API_KEY")
            )
        elif provider.lower() == "anthropic":
            return AnthropicChatCompletionClient(
                model=model_name,
                api_key=api_key or os.environ.get("ANTHROPIC_API_KEY")
            )
        elif provider.lower() == "ollama":
            # Ollama is typically run locally, so no API key is needed
            return OllamaChatCompletionClient(
                model=model_name,
                base_url="http://localhost:11434"  # Default Ollama URL
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")


class AgentFactory:
    """Factory class to create specialized agents."""
    
    @staticmethod
    async def create_language_detector_agent(model_client) -> AssistantAgent:
        """Create an agent specialized in detecting programming languages."""
        system_message = """
        You are a language detection agent specialized in identifying programming languages.
        Analyze the provided code and determine:
        1. The primary programming language used
        2. Any additional languages or markup present
        3. The version of the language if identifiable
        4. Common frameworks or libraries being used
        
        Provide a concise analysis with high confidence.
        """
        
        return AssistantAgent(
            name="language_detector",
            system_message=system_message,
            model_client=model_client
        )
    
    @staticmethod
    async def create_code_reviewer_agent(model_client) -> AssistantAgent:
        """Create an agent specialized in code review."""
        system_message = """
        You are a code reviewer agent specialized in identifying code quality issues.
        Analyze the provided code for:
        1. Potential bugs and logical errors
        2. Performance optimization opportunities
        3. Readability and maintainability issues
        4. Best practice violations
        5. Code structure and organization
        
        Provide specific, actionable feedback with examples of how to improve the code.
        """
        
        return AssistantAgent(
            name="code_reviewer",
            system_message=system_message,
            model_client=model_client
        )
    
    @staticmethod
    async def create_security_auditor_agent(model_client) -> AssistantAgent:
        """Create an agent specialized in security auditing."""
        system_message = """
        You are a security auditor agent specialized in identifying security vulnerabilities.
        Analyze the provided code for:
        1. Injection vulnerabilities (SQL, NoSQL, command, etc.)
        2. Authentication and authorization issues
        3. Data exposure risks and sensitive information leaks
        4. Security misconfigurations
        5. Use of components with known vulnerabilities
        6. Insecure cryptographic storage or transmission
        7. Insufficient logging and monitoring
        
        Provide specific, actionable feedback with examples of how to fix security issues.
        Rate each vulnerability by severity (Critical, High, Medium, Low).
        """
        
        return AssistantAgent(
            name="security_auditor",
            system_message=system_message,
            model_client=model_client
        )
    
    @staticmethod
    async def create_reporter_agent(model_client) -> AssistantAgent:
        """Create an agent specialized in reporting findings."""
        system_message = """
        You are a reporter agent specialized in summarizing and formatting findings.
        Your job is to:
        1. Collect findings from all other agents
        2. Organize them by priority and category
        3. Format them in a clear, actionable report
        4. Highlight the most critical issues that should be addressed first
        5. Provide a summary of overall code health
        
        Present your report in markdown format with appropriate sections, tables, and formatting.
        Include a summary at the top and detailed findings below.
        """
        
        return AssistantAgent(
            name="reporter",
            system_message=system_message,
            model_client=model_client
        )


async def analyze_code_with_multi_provider_agents(
    code: str,
    openai_api_key: Optional[str] = None,
    anthropic_api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze code using agents powered by different LLM providers.
    
    Args:
        code: The code to analyze
        openai_api_key: OpenAI API key (optional if set in environment)
        anthropic_api_key: Anthropic API key (optional if set in environment)
        
    Returns:
        A dictionary containing the analysis results
    """
    # Create LLM clients for different providers
    openai_client = await LLMClientFactory.create_client("openai", "gpt-4o", openai_api_key)
    anthropic_client = await LLMClientFactory.create_client("anthropic", "claude-3-opus-20240229", anthropic_api_key)
    ollama_client = await LLMClientFactory.create_client("ollama", "codellama")
    
    try:
        # Create specialized agents with different providers
        language_detector = await AgentFactory.create_language_detector_agent(ollama_client)
        code_reviewer = await AgentFactory.create_code_reviewer_agent(openai_client)
        security_auditor = await AgentFactory.create_security_auditor_agent(anthropic_client)
        reporter = await AgentFactory.create_reporter_agent(openai_client)
        user_proxy = UserProxyAgent("user_proxy")
        
        # Create a group chat with all agents
        group_chat = RoundRobinGroupChat(
            agents=[user_proxy, language_detector, code_reviewer, security_auditor, reporter],
            max_round=15  # Limit the conversation to 15 rounds
        )
        
        # Start the conversation with the code to analyze
        task = f"""
        Please analyze the following code:
        
        ```
        {code}
        ```
        
        Language detector: Please identify the programming language and frameworks used.
        Code reviewer: Please identify code quality issues.
        Security auditor: Please identify security vulnerabilities.
        Reporter: Please summarize the findings in a comprehensive report.
        """
        
        # Run the group chat
        result = await group_chat.run(task)
        
        return {
            "success": True,
            "report": result,
            "agents_used": ["language_detector", "code_reviewer", "security_auditor", "reporter"],
            "providers_used": ["openai", "anthropic", "ollama"]
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        # Clean up resources
        await openai_client.close()
        await anthropic_client.close()
        await ollama_client.close()


class CodeSampleRepository:
    """Repository of code samples for testing."""
    
    @staticmethod
    def get_python_sample() -> str:
        """Get a Python code sample with intentional issues."""
        return """
        import os
        import sqlite3
        
        def connect_to_database():
            # SECURITY ISSUE: Hardcoded credentials
            db_path = "users.db"
            return sqlite3.connect(db_path)
        
        def get_user_data(user_id):
            conn = connect_to_database()
            
            # SECURITY ISSUE: SQL Injection vulnerability
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
        
        def authenticate_user(username, password):
            # SECURITY ISSUE: Plaintext password comparison
            conn = connect_to_database()
            query = "SELECT password FROM users WHERE username = ?"
            result = conn.execute(query, (username,)).fetchone()
            conn.close()
            
            if result and result[0] == password:
                # SECURITY ISSUE: No session management
                return True
            return False
        
        def execute_command(command):
            # SECURITY ISSUE: Command injection vulnerability
            os.system(command)
            
        def main():
            user_id = input("Enter user ID: ")
            user_data = get_user_data(user_id)
            print(f"User data: {user_data}")
            
            command = input("Enter command to execute: ")
            execute_command(command)
        
        if __name__ == "__main__":
            main()
        """
    
    @staticmethod
    def get_javascript_sample() -> str:
        """Get a JavaScript code sample with intentional issues."""
        return """
        const express = require('express');
        const mysql = require('mysql');
        const app = express();
        
        // SECURITY ISSUE: Hardcoded credentials
        const db = mysql.createConnection({
            host: 'localhost',
            user: 'root',
            password: 'password123',
            database: 'userdb'
        });
        
        db.connect((err) => {
            if (err) {
                console.error('Database connection failed: ' + err.stack);
                return;
            }
            console.log('Connected to database');
        });
        
        app.use(express.json());
        
        // SECURITY ISSUE: No input validation
        app.get('/user/:id', (req, res) => {
            const userId = req.params.id;
            
            // SECURITY ISSUE: SQL Injection vulnerability
            const query = `SELECT * FROM users WHERE id = ${userId}`;
            
            db.query(query, (err, results) => {
                if (err) {
                    console.error(err);
                    return res.status(500).send('Database error');
                }
                
                // SECURITY ISSUE: Information disclosure
                return res.json(results[0]);
            });
        });
        
        // CODE QUALITY ISSUE: Callback hell
        app.post('/order', (req, res) => {
            const { userId, items } = req.body;
            
            db.query('SELECT * FROM users WHERE id = ?', [userId], (err, users) => {
                if (err) return res.status(500).send('Error');
                
                const user = users[0];
                db.query('INSERT INTO orders (user_id) VALUES (?)', [user.id], (err, result) => {
                    if (err) return res.status(500).send('Error');
                    
                    const orderId = result.insertId;
                    let itemsProcessed = 0;
                    
                    // PERFORMANCE ISSUE: Inefficient database operations
                    items.forEach(item => {
                        db.query('INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)', 
                            [orderId, item.id, item.quantity], (err) => {
                                if (err) return res.status(500).send('Error');
                                
                                itemsProcessed++;
                                if (itemsProcessed === items.length) {
                                    res.json({ success: true, orderId });
                                }
                            });
                    });
                });
            });
        });
        
        // SECURITY ISSUE: Insecure cookie
        app.post('/login', (req, res) => {
            const { username, password } = req.body;
            
            db.query('SELECT * FROM users WHERE username = ? AND password = ?', 
                [username, password], (err, results) => {
                    if (err) return res.status(500).send('Error');
                    
                    if (results.length > 0) {
                        // SECURITY ISSUE: Setting insecure cookie
                        res.cookie('user_id', results[0].id, { httpOnly: false });
                        res.json({ success: true });
                    } else {
                        res.status(401).json({ success: false });
                    }
                });
        });
        
        const PORT = 3000;
        app.listen(PORT, () => {
            console.log(`Server running on port ${PORT}`);
        });
        """


async def main():
    """
    Example usage of the multi-provider code analysis functionality.
    """
    # Get sample code to analyze
    code_repo = CodeSampleRepository()
    sample_code = code_repo.get_python_sample()
    
    # Replace with your actual API keys or set them as environment variables
    openai_api_key = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY")
    
    # Run the analysis
    print("Starting code analysis with multi-provider Autogen agents...")
    results = await analyze_code_with_multi_provider_agents(
        sample_code,
        openai_api_key,
        anthropic_api_key
    )
    
    if results["success"]:
        print("\nAnalysis completed successfully!")
        print("\nReport:")
        print(results["report"])
    else:
        print(f"\nAnalysis failed: {results['error']}")


if __name__ == "__main__":
    asyncio.run(main())
