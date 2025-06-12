# Group Chat Manager

The Group Chat Manager is a core component of VaahAI that enables multi-agent collaboration by leveraging Microsoft Autogen's group chat functionality. It provides a wrapper around Autogen's GroupChat classes with additional VaahAI-specific features.

## Overview

The Group Chat Manager allows multiple specialized agents to collaborate on tasks, with proper message routing, termination conditions, and human-in-the-loop integration. It supports different group chat types and human participation modes.

## Features

- Support for multiple group chat patterns (Round Robin, Selector, Broadcast, Custom)
- Configurable termination conditions
- Message filtering capabilities
- Human-in-the-loop integration with different participation modes
- Dynamic agent addition and removal
- Chat history retrieval

## Usage

### Basic Usage

```python
from vaahai.agents.utils.group_chat_manager import VaahAIGroupChatManager, GroupChatType, HumanInputMode
from vaahai.agents.base.agent_factory import AgentFactory

# Create agents
code_reviewer = AgentFactory.create_agent("code_reviewer", {"name": "CodeReviewer"})
security_auditor = AgentFactory.create_agent("security_auditor", {"name": "SecurityAuditor"})
language_detector = AgentFactory.create_agent("language_detector", {"name": "LanguageDetector"})

# Create group chat manager
manager = VaahAIGroupChatManager(
    agents=[code_reviewer, security_auditor, language_detector],
    chat_type=GroupChatType.ROUND_ROBIN,
    human_input_mode=HumanInputMode.TERMINATE
)

# Start a chat
result = await manager.start_chat("Please review this code: def add(a, b): return a + b")

# Get chat history
history = manager.get_chat_history()
```

### Configuration Options

The Group Chat Manager supports various configuration options:

```python
config = {
    "max_rounds": 10,                # Maximum number of conversation rounds
    "allow_repeat_speaker": False,   # Whether to allow the same agent to speak twice in a row
    "send_introductions": True,      # Whether to send agent introductions at the start
    "speaker_selection_method": "auto",  # Method for selecting the next speaker
    
    # Termination configuration
    "termination": {
        "max_messages": 50,          # Maximum number of messages before termination
        "completion_indicators": [   # Phrases that indicate the conversation is complete
            "Task completed",
            "Solution found"
        ],
        "custom_function": None      # Custom termination function
    },
    
    # Message filtering configuration
    "message_filter": {
        "excluded_agents": [],       # Agents whose messages should be filtered out
        "excluded_content": [],      # Content patterns that should be filtered out
        "custom_function": None      # Custom message filter function
    },
    
    # For SelectorGroupChat
    "selector_agent": None,          # Agent responsible for selecting the next speaker
    "selection_function": None,      # Function for selecting the next speaker
    
    # For CustomGroupChat
    "custom_class": None             # Custom group chat class
}
```

### Group Chat Types

The Group Chat Manager supports the following group chat types:

1. **Round Robin**: Agents take turns in a predefined order.
   ```python
   manager = VaahAIGroupChatManager(
       agents=[agent1, agent2, agent3],
       chat_type=GroupChatType.ROUND_ROBIN
   )
   ```

2. **Selector**: A dynamic conversation where agent selection depends on context.
   ```python
   def select_next_agent(group_chat, messages):
       # Logic to select the next agent based on the conversation
       return next_agent
   
   manager = VaahAIGroupChatManager(
       agents=[agent1, agent2, agent3],
       chat_type=GroupChatType.SELECTOR,
       config={"selection_function": select_next_agent}
   )
   ```

3. **Broadcast**: Messages are sent to all agents simultaneously.
   ```python
   manager = VaahAIGroupChatManager(
       agents=[agent1, agent2, agent3],
       chat_type=GroupChatType.BROADCAST
   )
   ```

4. **Custom**: A custom group chat implementation.
   ```python
   manager = VaahAIGroupChatManager(
       agents=[agent1, agent2, agent3],
       chat_type=GroupChatType.CUSTOM,
       config={"custom_class": MyCustomGroupChat}
   )
   ```

### Human Input Modes

The Group Chat Manager supports the following human input modes:

1. **Always**: Always ask for human input.
   ```python
   manager = VaahAIGroupChatManager(
       agents=[agent1, agent2, agent3],
       human_input_mode=HumanInputMode.ALWAYS
   )
   ```

2. **Never**: Never ask for human input.
   ```python
   manager = VaahAIGroupChatManager(
       agents=[agent1, agent2, agent3],
       human_input_mode=HumanInputMode.NEVER
   )
   ```

3. **Terminate**: Ask for human input only for termination decisions.
   ```python
   manager = VaahAIGroupChatManager(
       agents=[agent1, agent2, agent3],
       human_input_mode=HumanInputMode.TERMINATE
   )
   ```

4. **Feedback**: Ask for human input for feedback on agent responses.
   ```python
   manager = VaahAIGroupChatManager(
       agents=[agent1, agent2, agent3],
       human_input_mode=HumanInputMode.FEEDBACK
   )
   ```

## Advanced Usage

### Custom Termination Function

You can provide a custom termination function to determine when to end the conversation:

```python
def custom_termination(messages):
    # End the conversation if a specific condition is met
    if len(messages) > 20:
        return True
    
    # Check for specific content in the last message
    if messages and "final answer" in messages[-1].get("content", "").lower():
        return True
    
    return False

config = {
    "termination": {
        "custom_function": custom_termination
    }
}

manager = VaahAIGroupChatManager(agents=[agent1, agent2], config=config)
```

### Custom Message Filter

You can provide a custom message filter to control which messages are included in the conversation:

```python
def custom_filter(message):
    # Filter out messages containing sensitive information
    if "password" in message.get("content", "").lower():
        return False
    
    # Filter out messages from a specific agent
    if message.get("sender") == "sensitive_agent":
        return False
    
    return True

config = {
    "message_filter": {
        "custom_function": custom_filter
    }
}

manager = VaahAIGroupChatManager(agents=[agent1, agent2], config=config)
```

### Dynamic Agent Management

You can add or remove agents during a conversation:

```python
# Create initial group chat
manager = VaahAIGroupChatManager(agents=[agent1, agent2])

# Start the conversation
await manager.start_chat("Let's solve this problem together.")

# Add a new agent during the conversation
new_agent = AgentFactory.create_agent("expert_agent", {"name": "Expert"})
manager.add_agent(new_agent)

# Remove an agent if no longer needed
manager.remove_agent(agent2)
```

## Integration with VaahAI

The Group Chat Manager is designed to work seamlessly with other VaahAI components:

1. **Agent Factory**: Create specialized agents for different tasks.
2. **Prompt Manager**: Generate system messages for agents.
3. **Configuration System**: Load configuration from TOML files.

Example integration:

```python
from vaahai.agents.base.agent_factory import AgentFactory
from vaahai.agents.utils.group_chat_manager import VaahAIGroupChatManager
from vaahai.cli.utils.config import load_config

# Load configuration
config = load_config()
group_chat_config = config.get("autogen", {}).get("group_chat", {})

# Create agents
agents = []
for agent_config in config.get("agents", []):
    agent = AgentFactory.create_agent(agent_config["type"], agent_config)
    agents.append(agent)

# Create group chat manager
manager = VaahAIGroupChatManager(
    agents=agents,
    config=group_chat_config,
    chat_type=group_chat_config.get("type", "round_robin"),
    human_input_mode=group_chat_config.get("human_input_mode", "terminate")
)

# Start the conversation
result = await manager.start_chat("Let's begin our task.")
```

## Error Handling

The Group Chat Manager includes robust error handling:

1. **Test Mode**: Falls back to test mode if Autogen packages are not available.
2. **Validation**: Validates configuration parameters and provides helpful error messages.
3. **Logging**: Logs warnings and errors for debugging.

## Performance Considerations

When using the Group Chat Manager, consider the following performance tips:

1. **Limit Max Rounds**: Set a reasonable value for `max_rounds` to prevent infinite conversations.
2. **Use Termination Conditions**: Define clear termination conditions to end conversations efficiently.
3. **Filter Messages**: Use message filtering to reduce noise in the conversation.
4. **Choose the Right Chat Type**: Select the appropriate chat type for your use case.
