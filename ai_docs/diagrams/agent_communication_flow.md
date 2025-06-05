# Autogen Agent Communication Flow

This document illustrates the communication patterns and message flow between agents in Microsoft Autogen's architecture. Understanding these patterns is crucial for implementing effective multi-agent systems in VaahAI.

## Basic Agent Communication

```mermaid
sequenceDiagram
    participant User
    participant AssistantAgent
    
    User->>AssistantAgent: TextMessage (Task)
    AssistantAgent->>AssistantAgent: Process with LLM
    AssistantAgent-->>User: TextMessage (Response)
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
    AssistantAgent-->>User: ToolCallSummaryMessage
```

## Multi-Agent Conversation (Group Chat)

```mermaid
sequenceDiagram
    participant User
    participant GroupChatManager
    participant AssistantAgent1
    participant AssistantAgent2
    participant AssistantAgent3
    
    User->>GroupChatManager: TextMessage (Task)
    GroupChatManager->>AssistantAgent1: Forward Message
    AssistantAgent1->>GroupChatManager: TextMessage (Response)
    GroupChatManager->>AssistantAgent2: Forward Messages
    AssistantAgent2->>GroupChatManager: TextMessage (Response)
    GroupChatManager->>AssistantAgent3: Forward Messages
    AssistantAgent3->>GroupChatManager: TextMessage (Response)
    GroupChatManager->>GroupChatManager: Check Termination
    GroupChatManager-->>User: Final Response
```

## Selector Group Chat

```mermaid
sequenceDiagram
    participant User
    participant SelectorAgent
    participant Agent1
    participant Agent2
    participant Agent3
    
    User->>SelectorAgent: TextMessage (Task)
    SelectorAgent->>SelectorAgent: Select Next Speaker
    SelectorAgent->>Agent1: Forward Message
    Agent1->>SelectorAgent: TextMessage (Response)
    SelectorAgent->>SelectorAgent: Select Next Speaker
    SelectorAgent->>Agent2: Forward Messages
    Agent2->>SelectorAgent: TextMessage (Response)
    SelectorAgent->>SelectorAgent: Select Next Speaker
    SelectorAgent->>Agent1: Forward Messages
    Agent1->>SelectorAgent: TextMessage (Response)
    SelectorAgent->>SelectorAgent: Check Termination
    SelectorAgent-->>User: Final Response
```

## Human-in-the-Loop Flow

```mermaid
sequenceDiagram
    participant Human
    participant UserProxyAgent
    participant AssistantAgent
    participant Tool
    
    Human->>UserProxyAgent: TextMessage (Task)
    UserProxyAgent->>AssistantAgent: Forward Message
    AssistantAgent->>AssistantAgent: Process with LLM
    AssistantAgent->>Tool: ToolCallRequestEvent
    Tool->>Tool: Execute Function
    Tool-->>AssistantAgent: ToolCallExecutionEvent
    AssistantAgent-->>UserProxyAgent: TextMessage (Response)
    UserProxyAgent->>Human: Request Feedback
    Human->>UserProxyAgent: TextMessage (Feedback)
    UserProxyAgent->>AssistantAgent: Forward Feedback
    AssistantAgent->>AssistantAgent: Process Feedback
    AssistantAgent-->>UserProxyAgent: TextMessage (Updated Response)
    UserProxyAgent-->>Human: Final Response
```

## Core API Message Routing

```mermaid
sequenceDiagram
    participant Sender
    participant AgentRuntime
    participant ReceiverAgent
    participant MessageHandler
    
    Sender->>AgentRuntime: send_message(message, recipient)
    AgentRuntime->>ReceiverAgent: handle_message(message, ctx)
    ReceiverAgent->>MessageHandler: Route by Message Type
    MessageHandler->>ReceiverAgent: Process Message
    ReceiverAgent-->>AgentRuntime: Response Message
    AgentRuntime-->>Sender: Forward Response
```

## Asynchronous Communication Pattern

```mermaid
sequenceDiagram
    participant User
    participant AgentA
    participant AgentB
    participant AgentC
    
    User->>AgentA: TextMessage (Task)
    activate AgentA
    AgentA->>AgentB: TextMessage (Subtask 1)
    activate AgentB
    AgentA->>AgentC: TextMessage (Subtask 2)
    activate AgentC
    
    AgentB-->>AgentA: TextMessage (Result 1)
    deactivate AgentB
    AgentC-->>AgentA: TextMessage (Result 2)
    deactivate AgentC
    
    AgentA->>AgentA: Combine Results
    AgentA-->>User: TextMessage (Final Result)
    deactivate AgentA
```

## Message Flow in Distributed Runtime

```mermaid
sequenceDiagram
    participant AgentA
    participant WorkerA
    participant HostServicer
    participant WorkerB
    participant AgentB
    
    AgentA->>WorkerA: Local Message
    WorkerA->>HostServicer: Forward Message
    HostServicer->>WorkerB: Route Message
    WorkerB->>AgentB: Deliver Message
    AgentB->>WorkerB: Response
    WorkerB->>HostServicer: Forward Response
    HostServicer->>WorkerA: Route Response
    WorkerA->>AgentA: Deliver Response
```

## Key Communication Patterns

1. **Direct Communication**: One-to-one messaging between agents
2. **Group Chat**: Multiple agents participating in a conversation
3. **Selector-Based**: A moderator agent selects the next speaker
4. **Human-in-the-Loop**: Human feedback integrated into agent workflows
5. **Tool-Based**: Agents using tools to perform actions
6. **Asynchronous**: Agents working on tasks in parallel
7. **Distributed**: Communication across process or machine boundaries

These communication patterns form the foundation of Autogen's flexible architecture, enabling complex multi-agent workflows while maintaining a consistent messaging interface.
