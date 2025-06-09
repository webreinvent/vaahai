# Autogen Message Types

This document provides visual representations of the various message types used in Microsoft Autogen's framework. Understanding these message types is essential for implementing effective agent communication in VaahAI.

## Core Message Type Hierarchy

```mermaid
classDiagram
    class Message {
        +content: Any
        +role: str
        +metadata: Dict
        +id: str
        +parent_id: Optional[str]
        +timestamp: datetime
        +to_dict() Dict
        +from_dict(dict) Message
    }

    class TextMessage {
        +content: str
        +to_text() str
    }

    class MultiModalMessage {
        +content: List[ContentItem]
        +to_text() str
    }

    class ContentItem {
        +type: str
        +data: Any
    }

    class TextContentItem {
        +type: "text"
        +data: str
    }

    class ImageContentItem {
        +type: "image"
        +data: bytes
        +mime_type: str
    }

    class ToolCallRequestEvent {
        +tool_name: str
        +parameters: Dict
        +request_id: str
    }

    class ToolCallExecutionEvent {
        +tool_name: str
        +result: Any
        +request_id: str
        +success: bool
        +error: Optional[str]
    }

    class ToolCallSummaryMessage {
        +tool_name: str
        +summary: str
        +request_id: str
    }

    Message <|-- TextMessage
    Message <|-- MultiModalMessage
    Message <|-- ToolCallRequestEvent
    Message <|-- ToolCallExecutionEvent
    Message <|-- ToolCallSummaryMessage

    MultiModalMessage *-- ContentItem
    ContentItem <|-- TextContentItem
    ContentItem <|-- ImageContentItem
```

## Message Roles and Context

```mermaid
classDiagram
    class MessageRole {
        ASSISTANT
        USER
        SYSTEM
        TOOL
        FUNCTION
    }

    class ConversationContext {
        +messages: List[Message]
        +add_message(message)
        +get_messages() List[Message]
        +get_messages_by_role(role) List[Message]
        +clear()
    }

    class MessageThread {
        +root_message: Message
        +replies: List[Message]
        +add_reply(message)
        +get_thread() List[Message]
    }

    ConversationContext *-- Message
    MessageThread *-- Message
```

## Message Flow in Agent Communication

```mermaid
flowchart TD
    A[Agent A] -->|Creates| B[TextMessage]
    B -->|Sent to| C[Agent B]
    C -->|Processes| B
    C -->|Creates| D[TextMessage Response]
    D -->|Sent to| A

    A -->|Creates| E[ToolCallRequestEvent]
    E -->|Sent to| F[Tool]
    F -->|Executes| F
    F -->|Creates| G[ToolCallExecutionEvent]
    G -->|Sent to| A
    A -->|Creates| H[ToolCallSummaryMessage]
    H -->|Sent to| C
```

## MultiModal Message Structure

```mermaid
flowchart TD
    A[MultiModalMessage] -->|Contains| B[Text Content]
    A -->|Contains| C[Image Content]
    A -->|Contains| D[Other Media Content]

    B -->|Rendered as| E[Text in Conversation]
    C -->|Rendered as| F[Image in Conversation]
    D -->|Rendered as| G[Media in Conversation]
```

## Message Metadata Structure

```mermaid
classDiagram
    class MessageMetadata {
        +sender_id: str
        +recipient_id: str
        +timestamp: datetime
        +conversation_id: str
        +custom_data: Dict
    }

    class Message {
        +content: Any
        +role: str
        +metadata: MessageMetadata
        +id: str
        +parent_id: Optional[str]
    }

    Message *-- MessageMetadata
```

## Message Serialization and Transport

```mermaid
flowchart TD
    A[Message Object] -->|Serialization| B[JSON Representation]
    B -->|Network Transport| C[Remote System]
    C -->|Deserialization| D[Reconstructed Message]

    E[MultiModalMessage] -->|Special Serialization| F[JSON + Binary Data]
    F -->|Network Transport| G[Remote System]
    G -->|Special Deserialization| H[Reconstructed MultiModalMessage]
```

## Message Processing Pipeline

```mermaid
flowchart LR
    A[Raw Input] -->|Parsing| B[Message Object]
    B -->|Validation| C[Validated Message]
    C -->|Routing| D[Target Agent]
    D -->|Processing| E[Response Generation]
    E -->|Formatting| F[Response Message]
    F -->|Delivery| G[Recipient]
```

## Tool Message Flow

```mermaid
sequenceDiagram
    participant Agent
    participant ToolManager
    participant Tool

    Agent->>ToolManager: ToolCallRequestEvent
    ToolManager->>ToolManager: Validate Request
    ToolManager->>Tool: Execute Tool
    Tool->>Tool: Process Request
    Tool-->>ToolManager: Return Result
    ToolManager-->>Agent: ToolCallExecutionEvent
    Agent->>Agent: Process Result
    Agent->>Agent: Generate Summary
    Agent-->>Agent: ToolCallSummaryMessage
```
