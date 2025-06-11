# AutoGen 0.6.1 Message Handling

## Overview

This document describes how messages are structured and handled in AutoGen 0.6.1, which is used in the VaahAI project. AutoGen 0.6.1 has a significantly different architecture compared to previous versions, particularly in how messages are created and passed between agents.

## Message Types

In AutoGen 0.6.1, messages are structured objects rather than dictionaries. The key message types include:

### Agent-to-Agent Messages

These are subclasses of `BaseChatMessage` and include:

1. **TextMessage**: For basic text communication between agents
   ```python
   from autogen_agentchat.messages import TextMessage
   
   message = TextMessage(content="Hello, world!", source="User")
   ```

2. **UserMessage**: For messages coming from a user to an agent
   ```python
   from autogen_core.messages import UserMessage
   
   message = UserMessage(content="Hello, please help me with this task", role="user")
   ```

3. **MultiModalMessage**: For messages containing text and images
   ```python
   from autogen_agentchat.messages import MultiModalMessage
   from autogen_core import Image as AGImage
   
   message = MultiModalMessage(content=["Describe this image", image_object], source="User")
   ```

### Internal Agent Events

These are subclasses of `BaseAgentEvent` and include:

1. **ToolCallRequestEvent**: Indicates a request to call a tool
2. **ToolCallExecutionEvent**: Contains results of tool calls

## Message Handling in Agents

When sending messages to an agent in AutoGen 0.6.1, you must:

1. Use proper message objects (not dictionaries)
2. Include a cancellation token when calling `on_messages`
3. Handle the response object properly

Example:
```python
from autogen_core.messages import UserMessage
from autogen_core import _cancellation_token

# Create a message
message = UserMessage(content="Your prompt here", role="user")

# Create a cancellation token
cancellation_token = _cancellation_token.CancellationToken()

# Send the message to an agent
response = await agent.on_messages([message], cancellation_token)

# Access the response content
result = response.content
```

## Common Errors and Solutions

1. **Error: `'dict' object has no attribute 'to_model_message'`**
   - Cause: Using a dictionary instead of a proper message object
   - Solution: Use UserMessage or TextMessage objects instead

2. **Error: Missing cancellation token**
   - Cause: Not providing a cancellation token to the on_messages call
   - Solution: Create and pass a CancellationToken object

## Best Practices

1. Always import message classes from the correct modules:
   - `autogen_core.messages` for core message types
   - `autogen_agentchat.messages` for chat-specific message types

2. Always check if imports are successful before using classes

3. Include proper error handling with fallbacks

4. For VaahAI agents, follow this pattern:
   ```python
   try:
       # Import required message classes
       from autogen_core.messages import UserMessage
       from autogen_core import _cancellation_token

       # Create message
       message = UserMessage(content="Prompt", role="user")
       
       # Create cancellation token
       cancellation_token = _cancellation_token.CancellationToken()
       
       # Send to agent
       response = await agent.on_messages([message], cancellation_token)
       
       return response.content
   except Exception as e:
       logger.error(f"Error in message handling: {e}")
       # Fall back to test mode or simpler implementation
   ```
