# Conversation Flow in VaahAI

This document describes the conversation flow system in VaahAI, which enables agents to participate in structured conversations with each other.

## Overview

The conversation flow system provides a way for agents to engage in multi-agent conversations with different flow patterns. It consists of the following key components:

1. **Conversation**: Represents a conversation between agents, with participants, message history, and state.
2. **ConversationManager**: Manages multiple conversations, participant mappings, and message routing.
3. **Agent Conversation Support**: Extensions to the BaseAgent class to support participation in conversations.

## Conversation Structure

A conversation in VaahAI has the following properties:

- **ID**: A unique identifier for the conversation.
- **Participants**: A set of agent IDs participating in the conversation.
- **Status**: The current state of the conversation (created, active, paused, ended).
- **Flow Type**: The pattern of message flow in the conversation (turn-based, broadcast, directed).
- **Metadata**: Additional information about the conversation.
- **Message History**: A chronological record of messages in the conversation.

## Conversation Lifecycle

Conversations follow a defined lifecycle:

1. **Creation**: A conversation is created with an initiator and optional additional participants.
2. **Start**: The conversation is started, allowing messages to flow between participants.
3. **Active Phase**: Messages are exchanged according to the conversation's flow type.
4. **Pause/Resume**: A conversation can be paused and later resumed if needed.
5. **End**: The conversation is ended, preventing further message exchange.

## Conversation Flow Types

VaahAI supports different conversation flow patterns:

### Turn-Based Flow

In turn-based conversations, participants take turns sending messages in a predefined order. The conversation tracks whose turn it is, and only that participant can send a message.

```
Agent A -> Agent B -> Agent C -> Agent A -> ...
```

### Broadcast Flow

In broadcast conversations, messages from any participant are sent to all other participants.

```
Agent A -> [Agent B, Agent C, Agent D]
Agent B -> [Agent A, Agent C, Agent D]
```

### Directed Flow

In directed conversations, participants can send messages to specific other participants.

```
Agent A -> Agent B
Agent C -> Agent D
```

## Agent Conversation Participation

Agents can participate in multiple conversations simultaneously. The BaseAgent class provides methods for:

- **Joining a conversation**: `agent.join_conversation(conversation_id)`
- **Leaving a conversation**: `agent.leave_conversation(conversation_id)`
- **Checking participation**: `agent.is_in_conversation(conversation_id)`
- **Getting all conversations**: `agent.get_conversations()`

## Message Routing

The ConversationManager handles routing messages between agents in conversations:

1. When a message is sent, it includes a conversation ID.
2. The ConversationManager routes the message to the appropriate conversation.
3. The conversation adds the message to its history and determines the next steps based on its flow type.
4. For turn-based conversations, the turn advances to the next participant.

## Integration with Message System

The conversation system integrates with the existing message system:

- Messages include a `conversation_id` field to associate them with a conversation.
- The BaseAgent's `process_message` method checks if the message belongs to a conversation the agent is participating in.
- Responses automatically include the conversation ID of the original message.

## Example Usage

Here's an example of creating and using a conversation:

```python
# Create a conversation manager
manager = ConversationManager()

# Create a conversation with three participants
conversation = manager.create_conversation(
    initiator_id="agent1",
    participants=["agent2", "agent3"],
    flow_type=ConversationFlowType.TURN_BASED
)

# Make agents join the conversation
agent1.join_conversation(conversation.get_id())
agent2.join_conversation(conversation.get_id())
agent3.join_conversation(conversation.get_id())

# Start the conversation
conversation.start()

# Agent1 sends a message
message = Message.create_text_message(
    sender_id="agent1",
    receiver_id="agent2",
    text="Hello, Agent 2!",
    conversation_id=conversation.get_id()
)

# Route the message through the conversation manager
manager.route_message(message)

# The conversation now has the message in its history
# and the turn has advanced to agent2
```

## Testing

The conversation system includes comprehensive tests in `tests/agents/test_conversations.py` covering:

- Conversation creation and lifecycle management
- Participant management
- Message history tracking
- Turn-based conversation flow
- Conversation manager functionality
- Integration with agents

## Future Extensions

Planned extensions to the conversation system include:

1. **Conversation Templates**: Predefined conversation structures for common interaction patterns.
2. **Conversation Persistence**: Saving and loading conversations from storage.
3. **Conversation Analysis**: Tools for analyzing conversation patterns and outcomes.
4. **Advanced Flow Types**: Additional conversation flow patterns such as hierarchical and conditional flows.
