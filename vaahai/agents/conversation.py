"""
VaahAI Conversation Management

This module provides classes for managing conversations between agents in the VaahAI system.
It includes conversation structure, conversation flow patterns, and conversation management.
"""

import logging
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional, Set, Union, Callable

from .interfaces import IAgent, IConversation, IConversationManager
from .messages import Message

logger = logging.getLogger(__name__)


class ConversationStatus(Enum):
    """Enum representing the status of a conversation."""
    CREATED = "created"
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"


class ConversationFlowType(Enum):
    """Enum representing the type of conversation flow."""
    TURN_BASED = "turn_based"
    BROADCAST = "broadcast"
    DIRECTED = "directed"


class Conversation(IConversation):
    """
    Represents a conversation between agents.
    
    A conversation contains information about participants, messages, and state.
    It provides methods for managing the conversation lifecycle and participant interactions.
    """
    
    def __init__(
        self,
        conversation_id: Optional[str] = None,
        initiator_id: Optional[str] = None,
        flow_type: ConversationFlowType = ConversationFlowType.TURN_BASED,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new conversation.
        
        Args:
            conversation_id: Unique identifier for this conversation. If not provided, a UUID will be generated.
            initiator_id: ID of the agent that initiated the conversation.
            flow_type: The type of conversation flow to use.
            metadata: Additional metadata for the conversation.
        """
        self._id = conversation_id or str(uuid.uuid4())
        self._initiator_id = initiator_id
        self._flow_type = flow_type
        self._metadata = metadata or {}
        self._participants: Set[str] = set()
        self._status = ConversationStatus.CREATED
        self._created_at = datetime.now().isoformat()
        self._updated_at = self._created_at
        self._ended_at: Optional[str] = None
        self._message_history: List[Message] = []
        self._turn_order: List[str] = []
        self._current_turn_index = 0
        
        # Add initiator to participants if provided
        if initiator_id:
            self._participants.add(initiator_id)
            self._turn_order.append(initiator_id)
    
    def get_id(self) -> str:
        """
        Get the unique identifier for this conversation.
        
        Returns:
            Conversation identifier string
        """
        return self._id
    
    def get_status(self) -> ConversationStatus:
        """
        Get the current status of the conversation.
        
        Returns:
            Current conversation status
        """
        return self._status
    
    def get_flow_type(self) -> ConversationFlowType:
        """
        Get the flow type of the conversation.
        
        Returns:
            Conversation flow type
        """
        return self._flow_type
    
    def get_participants(self) -> Set[str]:
        """
        Get the set of participant IDs in this conversation.
        
        Returns:
            Set of participant IDs
        """
        return self._participants.copy()
    
    def get_message_history(self) -> List[Message]:
        """
        Get the message history for this conversation.
        
        Returns:
            List of messages in the conversation
        """
        return self._message_history.copy()
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get the metadata for this conversation.
        
        Returns:
            Dictionary of metadata
        """
        return self._metadata.copy()
    
    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set a metadata value for this conversation.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self._metadata[key] = value
        self._updated_at = datetime.now().isoformat()
    
    def add_participant(self, participant_id: str) -> None:
        """
        Add a participant to the conversation.
        
        Args:
            participant_id: ID of the participant to add
        """
        if participant_id not in self._participants:
            self._participants.add(participant_id)
            
            # Add to turn order if using turn-based flow
            if self._flow_type == ConversationFlowType.TURN_BASED:
                self._turn_order.append(participant_id)
                
            self._updated_at = datetime.now().isoformat()
            logger.info(f"Added participant {participant_id} to conversation {self._id}")
    
    def remove_participant(self, participant_id: str) -> None:
        """
        Remove a participant from the conversation.
        
        Args:
            participant_id: ID of the participant to remove
        """
        if participant_id in self._participants:
            self._participants.remove(participant_id)
            
            # Remove from turn order if using turn-based flow
            if self._flow_type == ConversationFlowType.TURN_BASED and participant_id in self._turn_order:
                self._turn_order.remove(participant_id)
                # Adjust current turn index if necessary
                if self._current_turn_index >= len(self._turn_order):
                    self._current_turn_index = 0 if self._turn_order else -1
                    
            self._updated_at = datetime.now().isoformat()
            logger.info(f"Removed participant {participant_id} from conversation {self._id}")
    
    def has_participant(self, participant_id: str) -> bool:
        """
        Check if a participant is in the conversation.
        
        Args:
            participant_id: ID of the participant to check
            
        Returns:
            True if the participant is in the conversation, False otherwise
        """
        return participant_id in self._participants
    
    def start(self) -> None:
        """
        Start the conversation.
        """
        if self._status == ConversationStatus.CREATED:
            self._status = ConversationStatus.ACTIVE
            self._updated_at = datetime.now().isoformat()
            logger.info(f"Started conversation {self._id}")
        else:
            logger.warning(f"Cannot start conversation {self._id} with status {self._status}")
    
    def pause(self) -> None:
        """
        Pause the conversation.
        """
        if self._status == ConversationStatus.ACTIVE:
            self._status = ConversationStatus.PAUSED
            self._updated_at = datetime.now().isoformat()
            logger.info(f"Paused conversation {self._id}")
        else:
            logger.warning(f"Cannot pause conversation {self._id} with status {self._status}")
    
    def resume(self) -> None:
        """
        Resume the conversation.
        """
        if self._status == ConversationStatus.PAUSED:
            self._status = ConversationStatus.ACTIVE
            self._updated_at = datetime.now().isoformat()
            logger.info(f"Resumed conversation {self._id}")
        else:
            logger.warning(f"Cannot resume conversation {self._id} with status {self._status}")
    
    def end(self) -> None:
        """
        End the conversation.
        """
        if self._status != ConversationStatus.ENDED:
            self._status = ConversationStatus.ENDED
            self._updated_at = datetime.now().isoformat()
            self._ended_at = self._updated_at
            logger.info(f"Ended conversation {self._id}")
        else:
            logger.warning(f"Conversation {self._id} is already ended")
    
    def add_message(self, message: Message) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            message: The message to add
        """
        if self._status != ConversationStatus.ENDED:
            # Set conversation ID on the message if not already set
            if not message.get_conversation_id():
                message.set_conversation_id(self._id)
                
            self._message_history.append(message)
            self._updated_at = datetime.now().isoformat()
            
            # Update turn if using turn-based flow
            if self._flow_type == ConversationFlowType.TURN_BASED:
                self._advance_turn()
        else:
            logger.warning(f"Cannot add message to ended conversation {self._id}")
    
    def get_next_turn(self) -> Optional[str]:
        """
        Get the ID of the participant whose turn is next.
        
        Returns:
            Participant ID, or None if no participants or not using turn-based flow
        """
        if self._flow_type != ConversationFlowType.TURN_BASED or not self._turn_order:
            return None
            
        return self._turn_order[self._current_turn_index]
    
    def _advance_turn(self) -> None:
        """
        Advance to the next turn in turn-based flow.
        """
        if self._flow_type == ConversationFlowType.TURN_BASED and self._turn_order:
            self._current_turn_index = (self._current_turn_index + 1) % len(self._turn_order)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the conversation to a dictionary.
        
        Returns:
            Dictionary representation of the conversation
        """
        return {
            "id": self._id,
            "initiator_id": self._initiator_id,
            "flow_type": self._flow_type.value,
            "status": self._status.value,
            "participants": list(self._participants),
            "created_at": self._created_at,
            "updated_at": self._updated_at,
            "ended_at": self._ended_at,
            "metadata": self._metadata,
            "message_count": len(self._message_history)
        }


class ConversationManager(IConversationManager):
    """
    Manages conversations between agents.
    
    The conversation manager is responsible for creating, retrieving, and ending
    conversations, as well as routing messages to the appropriate conversation.
    """
    
    def __init__(self):
        """
        Initialize a new conversation manager.
        """
        self._conversations: Dict[str, Conversation] = {}
        self._agent_conversations: Dict[str, Set[str]] = {}
    
    def create_conversation(
        self,
        initiator_id: str,
        flow_type: ConversationFlowType = ConversationFlowType.TURN_BASED,
        participants: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        conversation_id: Optional[str] = None
    ) -> Conversation:
        """
        Create a new conversation.
        
        Args:
            initiator_id: ID of the agent initiating the conversation
            flow_type: Type of conversation flow to use
            participants: List of participant IDs to add to the conversation
            metadata: Additional metadata for the conversation
            conversation_id: Optional ID for the conversation
            
        Returns:
            The created conversation
        """
        conversation = Conversation(
            conversation_id=conversation_id,
            initiator_id=initiator_id,
            flow_type=flow_type,
            metadata=metadata
        )
        
        # Add initiator to participants
        self._add_agent_to_conversation(initiator_id, conversation.get_id())
        
        # Add additional participants
        if participants:
            for participant_id in participants:
                if participant_id != initiator_id:
                    conversation.add_participant(participant_id)
                    self._add_agent_to_conversation(participant_id, conversation.get_id())
        
        # Store the conversation
        self._conversations[conversation.get_id()] = conversation
        
        logger.info(f"Created conversation {conversation.get_id()} with initiator {initiator_id}")
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """
        Get a conversation by ID.
        
        Args:
            conversation_id: ID of the conversation to get
            
        Returns:
            The conversation, or None if not found
        """
        return self._conversations.get(conversation_id)
    
    def get_agent_conversations(self, agent_id: str) -> List[Conversation]:
        """
        Get all conversations that an agent is participating in.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            List of conversations the agent is participating in
        """
        conversation_ids = self._agent_conversations.get(agent_id, set())
        return [self._conversations[cid] for cid in conversation_ids if cid in self._conversations]
    
    def end_conversation(self, conversation_id: str) -> bool:
        """
        End a conversation.
        
        Args:
            conversation_id: ID of the conversation to end
            
        Returns:
            True if the conversation was ended, False if not found
        """
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.end()
            logger.info(f"Ended conversation {conversation_id}")
            return True
        return False
    
    def add_participant(self, conversation_id: str, participant_id: str) -> bool:
        """
        Add a participant to a conversation.
        
        Args:
            conversation_id: ID of the conversation
            participant_id: ID of the participant to add
            
        Returns:
            True if the participant was added, False if the conversation was not found
        """
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.add_participant(participant_id)
            self._add_agent_to_conversation(participant_id, conversation_id)
            return True
        return False
    
    def remove_participant(self, conversation_id: str, participant_id: str) -> bool:
        """
        Remove a participant from a conversation.
        
        Args:
            conversation_id: ID of the conversation
            participant_id: ID of the participant to remove
            
        Returns:
            True if the participant was removed, False if the conversation was not found
        """
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.remove_participant(participant_id)
            self._remove_agent_from_conversation(participant_id, conversation_id)
            return True
        return False
    
    def route_message(self, message: Message) -> bool:
        """
        Route a message to the appropriate conversation.
        
        Args:
            message: The message to route
            
        Returns:
            True if the message was routed successfully, False otherwise
        """
        conversation_id = message.get_conversation_id()
        if not conversation_id:
            logger.warning(f"Cannot route message without conversation ID: {message.get_id()}")
            return False
            
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found for message {message.get_id()}")
            return False
            
        sender_id = message.get_sender_id()
        if not conversation.has_participant(sender_id):
            logger.warning(f"Sender {sender_id} is not a participant in conversation {conversation_id}")
            return False
            
        logger.info(f"Adding message {message.get_id()} from {sender_id} to conversation {conversation_id}")
        conversation.add_message(message)
        logger.info(f"Conversation {conversation_id} now has {len(conversation.get_message_history())} messages")
        return True
    
    def get_all_conversations(self) -> List[Conversation]:
        """
        Get all conversations.
        
        Returns:
            List of all conversations
        """
        return list(self._conversations.values())
    
    def get_active_conversations(self) -> List[Conversation]:
        """
        Get all active conversations.
        
        Returns:
            List of active conversations
        """
        return [c for c in self._conversations.values() if c.get_status() == ConversationStatus.ACTIVE]
    
    def _add_agent_to_conversation(self, agent_id: str, conversation_id: str) -> None:
        """
        Add an agent to the agent-conversation mapping.
        
        Args:
            agent_id: ID of the agent
            conversation_id: ID of the conversation
        """
        if agent_id not in self._agent_conversations:
            self._agent_conversations[agent_id] = set()
        self._agent_conversations[agent_id].add(conversation_id)
    
    def _remove_agent_from_conversation(self, agent_id: str, conversation_id: str) -> None:
        """
        Remove an agent from the agent-conversation mapping.
        
        Args:
            agent_id: ID of the agent
            conversation_id: ID of the conversation
        """
        if agent_id in self._agent_conversations:
            self._agent_conversations[agent_id].discard(conversation_id)
            if not self._agent_conversations[agent_id]:
                del self._agent_conversations[agent_id]
