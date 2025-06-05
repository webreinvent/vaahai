#!/usr/bin/env python3
"""
Docker-Based Code Execution Agent Example for VaahAI

This example demonstrates how to create an Autogen agent that can execute code
in a secure Docker container environment, which aligns with VaahAI's requirements
for isolated code execution.
"""

import asyncio
import os
import tempfile
import docker
from typing import Dict, Any, List, Optional

# Note: These imports are based on Autogen's structure and would need to be installed
# pip install -U "autogen-agentchat" "autogen-ext[openai]" docker
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient


class DockerExecutionEnvironment:
    """A class to manage Docker-based code execution environments."""
    
    def __init__(self, image_name: str = "python:3.9-slim"):
        """
        Initialize the Docker execution environment.
        
        Args:
            image_name: Docker image to use for code execution
        """
        self.client = docker.from_env()
        self.image_name = image_name
        
        # Ensure the image is available
        try:
            self.client.images.get(image_name)
        except docker.errors.ImageNotFound:
            print(f"Pulling Docker image: {image_name}")
            self.client.images.pull(image_name)
    
    def execute_code(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute code in a Docker container.
        
        Args:
            code: Python code to execute
            timeout: Maximum execution time in seconds
            
        Returns:
            Dictionary containing execution results
        """
        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        try:
            # Create a volume binding to pass the code file to the container
            host_path = os.path.abspath(temp_file_path)
            container_path = "/code/script.py"
            volumes = {host_path: {"bind": container_path, "mode": "ro"}}
            
            # Run the container with limited resources and no network access
            container = self.client.containers.run(
                self.image_name,
                command=f"python {container_path}",
                volumes=volumes,
                detach=True,
                mem_limit="256m",  # Limit memory to 256MB
                cpu_quota=50000,   # Limit CPU to 50% of a core
                network_mode="none",  # Disable network access
                cap_drop=["ALL"],  # Drop all capabilities for security
                security_opt=["no-new-privileges:true"]  # Prevent privilege escalation
            )
            
            # Wait for the container to finish or timeout
            try:
                exit_code = container.wait(timeout=timeout)["StatusCode"]
                logs = container.logs().decode("utf-8")
                
                return {
                    "success": exit_code == 0,
                    "exit_code": exit_code,
                    "output": logs,
                    "error": None if exit_code == 0 else "Execution failed"
                }
            except Exception as e:
                container.kill()
                return {
                    "success": False,
                    "exit_code": -1,
                    "output": "",
                    "error": f"Execution error: {str(e)}"
                }
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            # Ensure the container is removed
            try:
                container.remove(force=True)
            except:
                pass


async def create_code_executor_agent(model_client) -> AssistantAgent:
    """
    Create a code executor agent that can write and run code.
    
    Args:
        model_client: The LLM client to use for the agent
        
    Returns:
        An AssistantAgent configured for code execution
    """
    system_message = """
    You are a code executor agent specialized in writing and running Python code.
    When asked to solve a problem:
    1. Write clear, efficient Python code to solve it
    2. Include comments explaining your approach
    3. Handle edge cases and potential errors
    4. Keep security best practices in mind
    
    Your code will be executed in a secure Docker container with:
    - Limited memory (256MB)
    - Limited CPU (50% of a core)
    - No network access
    - No ability to write to the filesystem outside your temporary environment
    
    Focus on writing code that works correctly within these constraints.
    """
    
    return AssistantAgent(
        name="code_executor",
        system_message=system_message,
        model_client=model_client
    )


async def create_code_reviewer_agent(model_client) -> AssistantAgent:
    """
    Create a code reviewer agent that can analyze code quality.
    
    Args:
        model_client: The LLM client to use for the agent
        
    Returns:
        An AssistantAgent configured for code review
    """
    system_message = """
    You are a code reviewer agent specialized in analyzing Python code.
    When reviewing code:
    1. Check for correctness and whether it solves the stated problem
    2. Identify potential bugs or edge cases not handled
    3. Suggest optimizations for performance or readability
    4. Evaluate security considerations, especially for code running in a Docker container
    
    Provide specific, actionable feedback that would improve the code.
    """
    
    return AssistantAgent(
        name="code_reviewer",
        system_message=system_message,
        model_client=model_client
    )


class DockerCodeExecutionWorkflow:
    """A class to manage the workflow of code execution in Docker."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Docker code execution workflow.
        
        Args:
            api_key: OpenAI API key (optional if set in environment)
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.docker_env = DockerExecutionEnvironment()
    
    async def execute_task(self, task_description: str) -> Dict[str, Any]:
        """
        Execute a task using the code executor and reviewer agents.
        
        Args:
            task_description: Description of the task to execute
            
        Returns:
            Dictionary containing the execution results
        """
        # Initialize the model client
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o",
            api_key=self.api_key
        )
        
        try:
            # Create agents
            code_executor = await create_code_executor_agent(model_client)
            code_reviewer = await create_code_reviewer_agent(model_client)
            user_proxy = UserProxyAgent(
                name="user_proxy",
                human_input_mode="NEVER"  # Don't ask for human input
            )
            
            # Create a group chat
            group_chat = RoundRobinGroupChat(
                agents=[user_proxy, code_executor, code_reviewer],
                max_round=5  # Limit the conversation to 5 rounds
            )
            
            # Start the conversation with the task description
            initial_message = f"""
            Task: {task_description}
            
            Code executor: Please write Python code to solve this task.
            Code reviewer: After the code is written, please review it.
            """
            
            # Run the group chat to generate code
            result = await group_chat.run(initial_message)
            
            # Extract code from the conversation
            # This is a simple extraction method and might need to be improved
            # to handle more complex conversations
            code_blocks = []
            for line in result.split("\n"):
                if "```python" in line:
                    code_blocks.append([])
                elif "```" in line and len(code_blocks) > 0 and len(code_blocks[-1]) > 0:
                    code_blocks[-1] = "\n".join(code_blocks[-1])
                elif len(code_blocks) > 0 and isinstance(code_blocks[-1], list):
                    code_blocks[-1].append(line)
            
            # Use the last code block if available
            code_to_execute = code_blocks[-1] if code_blocks else ""
            
            if not code_to_execute:
                return {
                    "success": False,
                    "error": "No executable code was generated"
                }
            
            # Execute the code in Docker
            execution_result = self.docker_env.execute_code(code_to_execute)
            
            return {
                "success": execution_result["success"],
                "task": task_description,
                "code": code_to_execute,
                "execution_result": execution_result,
                "agent_conversation": result
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
    Example usage of the Docker code execution workflow.
    """
    # Sample task to execute
    task_description = """
    Create a function that calculates the Fibonacci sequence up to n terms.
    Then use this function to calculate and print the first 10 Fibonacci numbers.
    Also calculate and print the sum of these first 10 numbers.
    """
    
    # Replace with your actual API key or set it as an environment variable
    api_key = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
    
    # Create the workflow
    workflow = DockerCodeExecutionWorkflow(api_key)
    
    # Execute the task
    print("Starting Docker-based code execution workflow...")
    result = await workflow.execute_task(task_description)
    
    if result["success"]:
        print("\nTask executed successfully!")
        print("\nCode:")
        print(result["code"])
        print("\nExecution output:")
        print(result["execution_result"]["output"])
    else:
        print(f"\nTask execution failed: {result.get('error', 'Unknown error')}")
        if "execution_result" in result and "output" in result["execution_result"]:
            print("\nExecution output:")
            print(result["execution_result"]["output"])


if __name__ == "__main__":
    asyncio.run(main())
