"""
Tests for the conversation functionality in the VaahAI agent system.
"""

import asyncio
import pytest
from typing import Dict, Any, List

from vaahai.agents.conversation import (
    Conversation, 
    ConversationManager,
    ConversationStatus,
    ConversationFlowType
)
from vaahai.agents.messages import Message
from tests.agents.mock_agents import MockConversationalAgent


@pytest.fixture
def conversation():
    """Create a test conversation."""
    return Conversation(
        conversation_id="test-conversation",
        initiator_id="agent1",
        flow_type=ConversationFlowType.TURN_BASED
    )


@pytest.fixture
def conversation_manager():
    """Create a test conversation manager."""
    return ConversationManager()


@pytest.fixture
def agents():
    """Create test agents."""
    return {
        "agent1": MockConversationalAgent(agent_id="agent1", name="Agent 1"),
        "agent2": MockConversationalAgent(agent_id="agent2", name="Agent 2"),
        "agent3": MockConversationalAgent(agent_id="agent3", name="Agent 3")
    }


def test_conversation_creation():
    """Test that a conversation can be created with the correct properties."""
    conversation = Conversation(
        conversation_id="test-conversation",
        initiator_id="agent1",
        flow_type=ConversationFlowType.TURN_BASED,
        metadata={"topic": "test"}
    )
    
    assert conversation.get_id() == "test-conversation"
    assert "agent1" in conversation.get_participants()
    assert conversation.get_status() == ConversationStatus.CREATED
    assert conversation.get_flow_type() == ConversationFlowType.TURN_BASED
    assert conversation.get_metadata() == {"topic": "test"}
    assert len(conversation.get_message_history()) == 0


def test_conversation_participants(conversation):
    """Test adding and removing participants from a conversation."""
    # Add participants
    conversation.add_participant("agent2")
    conversation.add_participant("agent3")
    
    assert conversation.has_participant("agent1")
    assert conversation.has_participant("agent2")
    assert conversation.has_participant("agent3")
    assert len(conversation.get_participants()) == 3
    
    # Remove a participant
    conversation.remove_participant("agent2")
    
    assert conversation.has_participant("agent1")
    assert not conversation.has_participant("agent2")
    assert conversation.has_participant("agent3")
    assert len(conversation.get_participants()) == 2


def test_conversation_lifecycle(conversation):
    """Test the conversation lifecycle (start, pause, resume, end)."""
    # Initial state
    assert conversation.get_status() == ConversationStatus.CREATED
    
    # Start
    conversation.start()
    assert conversation.get_status() == ConversationStatus.ACTIVE
    
    # Pause
    conversation.pause()
    assert conversation.get_status() == ConversationStatus.PAUSED
    
    # Resume
    conversation.resume()
    assert conversation.get_status() == ConversationStatus.ACTIVE
    
    # End
    conversation.end()
    assert conversation.get_status() == ConversationStatus.ENDED


def test_conversation_messages(conversation):
    """Test adding messages to a conversation."""
    # Start the conversation
    conversation.start()
    
    # Create and add messages
    message1 = Message.create_text_message(
        sender_id="agent1",
        receiver_id="agent2",
        text="Hello, Agent 2!",
        conversation_id=conversation.get_id()
    )
    
    message2 = Message.create_text_message(
        sender_id="agent2",
        receiver_id="agent1",
        text="Hello, Agent 1!",
        conversation_id=conversation.get_id()
    )
    
    conversation.add_message(message1)
    conversation.add_message(message2)
    
    # Check message history
    history = conversation.get_message_history()
    assert len(history) == 2
    assert history[0].get_content()["text"] == "Hello, Agent 2!"
    assert history[1].get_content()["text"] == "Hello, Agent 1!"


def test_turn_based_conversation(conversation):
    """Test turn-based conversation flow."""
    # Add participants
    conversation.add_participant("agent2")
    conversation.add_participant("agent3")
    
    # Start the conversation
    conversation.start()
    
    # Check initial turn
    assert conversation.get_next_turn() == "agent1"
    
    # Add a message from agent1
    message1 = Message.create_text_message(
        sender_id="agent1",
        receiver_id="agent2",
        text="Hello from agent1",
        conversation_id=conversation.get_id()
    )
    conversation.add_message(message1)
    
    # Turn should advance to agent2
    assert conversation.get_next_turn() == "agent2"
    
    # Add a message from agent2
    message2 = Message.create_text_message(
        sender_id="agent2",
        receiver_id="agent3",
        text="Hello from agent2",
        conversation_id=conversation.get_id()
    )
    conversation.add_message(message2)
    
    # Turn should advance to agent3
    assert conversation.get_next_turn() == "agent3"
    
    # Add a message from agent3
    message3 = Message.create_text_message(
        sender_id="agent3",
        receiver_id="agent1",
        text="Hello from agent3",
        conversation_id=conversation.get_id()
    )
    conversation.add_message(message3)
    
    # Turn should cycle back to agent1
    assert conversation.get_next_turn() == "agent1"


def test_conversation_manager_creation(conversation_manager):
    """Test creating conversations with the conversation manager."""
    # Create a conversation
    conversation = conversation_manager.create_conversation(
        initiator_id="agent1",
        flow_type=ConversationFlowType.TURN_BASED,
        participants=["agent2", "agent3"],
        metadata={"topic": "test"}
    )
    
    # Check that the conversation was created correctly
    assert conversation.get_id() is not None
    assert "agent1" in conversation.get_participants()
    assert "agent2" in conversation.get_participants()
    assert "agent3" in conversation.get_participants()
    
    # Check that we can retrieve the conversation
    retrieved = conversation_manager.get_conversation(conversation.get_id())
    assert retrieved is not None
    assert retrieved.get_id() == conversation.get_id()


def test_conversation_manager_agent_conversations(conversation_manager, agents):
    """Test retrieving conversations for a specific agent."""
    # Create conversations with different participants
    conv1 = conversation_manager.create_conversation(
        initiator_id="agent1",
        participants=["agent2"]
    )
    
    conv2 = conversation_manager.create_conversation(
        initiator_id="agent1",
        participants=["agent3"]
    )
    
    conv3 = conversation_manager.create_conversation(
        initiator_id="agent2",
        participants=["agent3"]
    )
    
    # Check agent1's conversations
    agent1_convs = conversation_manager.get_agent_conversations("agent1")
    assert len(agent1_convs) == 2
    assert conv1.get_id() in [c.get_id() for c in agent1_convs]
    assert conv2.get_id() in [c.get_id() for c in agent1_convs]
    
    # Check agent2's conversations
    agent2_convs = conversation_manager.get_agent_conversations("agent2")
    assert len(agent2_convs) == 2
    assert conv1.get_id() in [c.get_id() for c in agent2_convs]
    assert conv3.get_id() in [c.get_id() for c in agent2_convs]
    
    # Check agent3's conversations
    agent3_convs = conversation_manager.get_agent_conversations("agent3")
    assert len(agent3_convs) == 2
    assert conv2.get_id() in [c.get_id() for c in agent3_convs]
    assert conv3.get_id() in [c.get_id() for c in agent3_convs]


def test_conversation_manager_end_conversation(conversation_manager):
    """Test ending a conversation through the manager."""
    # Create a conversation
    conversation = conversation_manager.create_conversation(
        initiator_id="agent1",
        participants=["agent2"]
    )
    
    # End the conversation
    result = conversation_manager.end_conversation(conversation.get_id())
    assert result is True
    
    # Check that the conversation is ended
    retrieved = conversation_manager.get_conversation(conversation.get_id())
    assert retrieved is not None
    assert retrieved.get_status() == ConversationStatus.ENDED
    
    # Try to end a non-existent conversation
    result = conversation_manager.end_conversation("non-existent")
    assert result is False


def test_conversation_manager_participants(conversation_manager):
    """Test adding and removing participants through the manager."""
    # Create a conversation
    conversation = conversation_manager.create_conversation(
        initiator_id="agent1"
    )
    
    # Add a participant
    result = conversation_manager.add_participant(conversation.get_id(), "agent2")
    assert result is True
    
    # Check that the participant was added
    retrieved = conversation_manager.get_conversation(conversation.get_id())
    assert "agent2" in retrieved.get_participants()
    
    # Remove the participant
    result = conversation_manager.remove_participant(conversation.get_id(), "agent2")
    assert result is True
    
    # Check that the participant was removed
    retrieved = conversation_manager.get_conversation(conversation.get_id())
    assert "agent2" not in retrieved.get_participants()
    
    # Try to add/remove participants from a non-existent conversation
    assert conversation_manager.add_participant("non-existent", "agent3") is False
    assert conversation_manager.remove_participant("non-existent", "agent1") is False


def test_conversation_manager_message_routing(conversation_manager):
    """Test routing messages through the conversation manager."""
    # Create a conversation
    conversation = conversation_manager.create_conversation(
        initiator_id="agent1",
        participants=["agent2"]
    )
    conversation_id = conversation.get_id()
    
    # Start the conversation
    conversation.start()
    
    # Create a message
    message = Message.create_text_message(
        sender_id="agent1",
        receiver_id="agent2",
        text="Hello, Agent 2!",
        conversation_id=conversation_id
    )
    
    # Route the message
    result = conversation_manager.route_message(message)
    assert result is True
    
    # Check that the message was added to the conversation
    retrieved = conversation_manager.get_conversation(conversation_id)
    history = retrieved.get_message_history()
    assert len(history) == 1
    assert history[0].get_content()["text"] == "Hello, Agent 2!"
    
    # Try to route a message to a non-existent conversation
    message2 = Message.create_text_message(
        sender_id="agent1",
        receiver_id="agent2",
        text="This won't be routed",
        conversation_id="non-existent"
    )
    result = conversation_manager.route_message(message2)
    assert result is False
    
    # Try to route a message from a non-participant
    message3 = Message.create_text_message(
        sender_id="agent3",
        receiver_id="agent1",
        text="This won't be routed either",
        conversation_id=conversation_id
    )
    result = conversation_manager.route_message(message3)
    assert result is False


@pytest.mark.asyncio
async def test_agent_conversation_integration(agents):
    """Test integration between agents and conversations."""
    # Create a conversation manager
    manager = ConversationManager()
    
    # Create a conversation
    conversation = manager.create_conversation(
        initiator_id="agent1",
        participants=["agent2", "agent3"]
    )
    conversation_id = conversation.get_id()
    
    # Make agents join the conversation
    for agent_id, agent in agents.items():
        agent.join_conversation(conversation_id)
        print(f"Agent {agent_id} joined conversation {conversation_id}")
    
    # Start the conversation
    conversation.start()
    print(f"Conversation {conversation_id} started with status {conversation.get_status()}")
    
    # Create an initial message
    initial_message = Message.create_text_message(
        sender_id="agent1",
        receiver_id="agent2",
        text="Hello from Agent 1",
        conversation_id=conversation_id
    )
    print(f"Created initial message {initial_message.get_id()} from {initial_message.get_sender_id()} to {initial_message.get_receiver_id()}")
    
    # Add the initial message to the conversation
    manager.route_message(initial_message)
    print(f"Routed initial message, conversation now has {len(conversation.get_message_history())} messages")
    
    # Process the message through agent2
    response = await agents["agent2"].process_message(initial_message)
    print(f"Agent2 processed message and returned response {response.get_id()} with conversation_id {response.get_conversation_id()}")
    
    # Check that the response has the correct conversation ID
    assert response.get_conversation_id() == conversation_id
    
    # Route the response back through the conversation
    result = manager.route_message(response)
    print(f"Routed response message, result: {result}")
    print(f"Conversation now has {len(conversation.get_message_history())} messages")
    print(f"Message history: {[msg.get_id() for msg in conversation.get_message_history()]}")
    
    # Check conversation history
    history = conversation.get_message_history()
    assert len(history) == 2
    assert history[0].get_content()["text"] == "Hello from Agent 1"
    assert "received your message" in history[1].get_content()["text"]
