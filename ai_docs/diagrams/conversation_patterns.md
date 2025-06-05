# Autogen Conversation Pattern Diagrams

This document provides visual representations of the various conversation patterns supported by Microsoft Autogen. These diagrams illustrate the message flow and interaction patterns between agents.

## Basic Request-Response Pattern

```mermaid
sequenceDiagram
    participant Agent1
    participant Agent2
    
    Agent1->>Agent2: TextMessage (Request)
    Agent2->>Agent2: Process Request
    Agent2-->>Agent1: TextMessage (Response)
```

## Streaming Response Pattern

```mermaid
sequenceDiagram
    participant Agent1
    participant Agent2
    
    Agent1->>Agent2: TextMessage (Request)
    Agent2->>Agent2: Begin Processing
    Agent2-->>Agent1: TextMessage (Chunk 1)
    Agent2->>Agent2: Continue Processing
    Agent2-->>Agent1: TextMessage (Chunk 2)
    Agent2->>Agent2: Finish Processing
    Agent2-->>Agent1: TextMessage (Final Chunk)
```

## Human-in-the-Loop Approval Flow

```mermaid
sequenceDiagram
    participant Human
    participant AssistantAgent
    participant Tool
    
    Human->>AssistantAgent: TextMessage (Task)
    AssistantAgent->>AssistantAgent: Process Task
    AssistantAgent-->>Human: TextMessage (Proposed Action)
    Human->>AssistantAgent: TextMessage (Approval/Modification)
    AssistantAgent->>Tool: ToolCallRequestEvent
    Tool-->>AssistantAgent: ToolCallExecutionEvent
    AssistantAgent-->>Human: TextMessage (Result)
```

## Round-Robin Group Chat

```mermaid
sequenceDiagram
    participant User
    participant GroupChatManager
    participant Agent1
    participant Agent2
    participant Agent3
    
    User->>GroupChatManager: TextMessage (Task)
    GroupChatManager->>Agent1: Forward Message
    Agent1->>GroupChatManager: TextMessage (Response)
    GroupChatManager->>Agent2: Forward All Messages
    Agent2->>GroupChatManager: TextMessage (Response)
    GroupChatManager->>Agent3: Forward All Messages
    Agent3->>GroupChatManager: TextMessage (Response)
    GroupChatManager->>Agent1: Forward All Messages
    Note over GroupChatManager: Continue until termination condition
    GroupChatManager-->>User: Final Result
```

## Selector-Based Chat

```mermaid
sequenceDiagram
    participant User
    participant SelectorAgent
    participant Agent1
    participant Agent2
    participant Agent3
    
    User->>SelectorAgent: TextMessage (Task)
    SelectorAgent->>SelectorAgent: Select Next Agent
    SelectorAgent->>Agent2: Forward Message
    Agent2->>SelectorAgent: TextMessage (Response)
    SelectorAgent->>SelectorAgent: Select Next Agent
    SelectorAgent->>Agent1: Forward All Messages
    Agent1->>SelectorAgent: TextMessage (Response)
    SelectorAgent->>SelectorAgent: Select Next Agent
    SelectorAgent->>Agent3: Forward All Messages
    Agent3->>SelectorAgent: TextMessage (Response)
    SelectorAgent-->>User: Final Result
```

## Tool Usage Flow

```mermaid
sequenceDiagram
    participant User
    participant AssistantAgent
    participant Tool
    
    User->>AssistantAgent: TextMessage (Task)
    AssistantAgent->>AssistantAgent: Process with LLM
    AssistantAgent->>Tool: ToolCallRequestEvent
    Tool->>Tool: Execute Function
    Tool-->>AssistantAgent: ToolCallExecutionEvent
    AssistantAgent->>AssistantAgent: Process Result
    AssistantAgent-->>User: TextMessage (Response with Tool Result)
```

## Multi-Step Tool Usage

```mermaid
sequenceDiagram
    participant User
    participant AssistantAgent
    participant Tool1
    participant Tool2
    
    User->>AssistantAgent: TextMessage (Task)
    AssistantAgent->>AssistantAgent: Process with LLM
    AssistantAgent->>Tool1: ToolCallRequestEvent
    Tool1-->>AssistantAgent: ToolCallExecutionEvent
    AssistantAgent->>AssistantAgent: Process Intermediate Result
    AssistantAgent->>Tool2: ToolCallRequestEvent
    Tool2-->>AssistantAgent: ToolCallExecutionEvent
    AssistantAgent->>AssistantAgent: Process Final Result
    AssistantAgent-->>User: TextMessage (Response)
```

## Asynchronous Communication

```mermaid
sequenceDiagram
    participant Agent1
    participant MessageQueue
    participant Agent2
    
    Agent1->>MessageQueue: Send Message
    Agent1->>Agent1: Continue Processing
    MessageQueue->>Agent2: Deliver Message (When Available)
    Agent2->>Agent2: Process Message
    Agent2->>MessageQueue: Send Response
    MessageQueue->>Agent1: Deliver Response (When Available)
```

## Distributed Communication

```mermaid
sequenceDiagram
    participant AgentA
    participant WorkerA
    participant HostServicer
    participant WorkerB
    participant AgentB
    
    AgentA->>WorkerA: Local Message
    WorkerA->>HostServicer: Remote Message
    HostServicer->>WorkerB: Forward Message
    WorkerB->>AgentB: Local Message
    AgentB->>WorkerB: Local Response
    WorkerB->>HostServicer: Remote Response
    HostServicer->>WorkerA: Forward Response
    WorkerA->>AgentA: Local Response
```

## Termination Conditions

```mermaid
sequenceDiagram
    participant User
    participant GroupChatManager
    participant Agent1
    participant Agent2
    
    User->>GroupChatManager: TextMessage (Task)
    GroupChatManager->>Agent1: Forward Message
    Agent1->>GroupChatManager: TextMessage (Response)
    GroupChatManager->>Agent2: Forward Messages
    Agent2->>GroupChatManager: TextMessage (Response with "TASK COMPLETE")
    Note over GroupChatManager: Detect Termination Condition
    GroupChatManager-->>User: Final Result
```

## Human Feedback Loop

```mermaid
sequenceDiagram
    participant Human
    participant AssistantAgent
    
    Human->>AssistantAgent: TextMessage (Task)
    AssistantAgent->>AssistantAgent: Process Task
    AssistantAgent-->>Human: TextMessage (Initial Response)
    Human->>AssistantAgent: TextMessage (Feedback)
    AssistantAgent->>AssistantAgent: Incorporate Feedback
    AssistantAgent-->>Human: TextMessage (Improved Response)
    Human->>AssistantAgent: TextMessage (Approval)
```

## Broadcast Communication

```mermaid
sequenceDiagram
    participant Broadcaster
    participant Agent1
    participant Agent2
    participant Agent3
    participant Aggregator
    
    Broadcaster->>Agent1: Broadcast Message
    Broadcaster->>Agent2: Broadcast Message
    Broadcaster->>Agent3: Broadcast Message
    Agent1-->>Aggregator: Response
    Agent2-->>Aggregator: Response
    Agent3-->>Aggregator: Response
    Aggregator->>Aggregator: Combine Responses
```
