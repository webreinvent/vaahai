# Autogen Agent Class Hierarchy

This document provides a detailed view of the class hierarchy in Microsoft Autogen's agent architecture, focusing on inheritance relationships and key components.

## Core API Class Hierarchy

```mermaid
classDiagram
    class Agent {
        <<interface>>
        +AgentId id
        +AgentMetadata metadata
        +handle_message(message, ctx)
    }

    class RoutedAgent {
        <<abstract>>
        +AgentId id
        +AgentMetadata metadata
        +handle_message(message, ctx)
        +register_message_handler(handler)
    }

    Agent <|-- RoutedAgent

    class CustomCoreAgent {
        +handle_my_message_type(message, ctx)
    }

    RoutedAgent <|-- CustomCoreAgent

    class MessageHandler {
        <<decorator>>
        +__call__(func)
    }

    MessageHandler --> RoutedAgent : decorates
```

## AgentChat Class Hierarchy

```mermaid
classDiagram
    class BaseAgent {
        <<abstract>>
        +String name
        +String description
        +run(task) TaskResult
        +run_stream(task) Iterator
        +handle_message(message)
    }

    class AssistantAgent {
        +ModelClient model_client
        +List~Tool~ tools
        +String system_message
        +run(task) TaskResult
    }

    BaseAgent <|-- AssistantAgent

    class UserProxyAgent {
        +Boolean human_input_mode
        +List~Tool~ tools
        +run(task) TaskResult
    }

    BaseAgent <|-- UserProxyAgent

    class RetrieveUserProxyAgent {
        +RetrievalClient retrieval_client
        +run(task) TaskResult
    }

    UserProxyAgent <|-- RetrieveUserProxyAgent

    class TeachableAgent {
        +MemoryClient memory_client
        +run(task) TaskResult
    }

    BaseAgent <|-- TeachableAgent
```

## Runtime Environment Classes

```mermaid
classDiagram
    class AgentRuntime {
        <<interface>>
        +register_agent(agent)
        +send_message(message, recipient)
        +start()
        +stop()
    }

    class SingleThreadedAgentRuntime {
        +Dict agents
        +register_agent(agent)
        +send_message(message, recipient)
    }

    AgentRuntime <|-- SingleThreadedAgentRuntime

    class DistributedAgentRuntime {
        +HostServicer host_servicer
        +List~Worker~ workers
        +register_agent(agent)
        +send_message(message, recipient)
    }

    AgentRuntime <|-- DistributedAgentRuntime
```

## Message Classes

```mermaid
classDiagram
    class BaseChatMessage {
        <<abstract>>
        +String source
        +Dict metadata
        +get_content()
    }

    class TextMessage {
        +String content
    }

    BaseChatMessage <|-- TextMessage

    class MultiModalMessage {
        +List content
    }

    BaseChatMessage <|-- MultiModalMessage

    class BaseAgentEvent {
        <<abstract>>
        +String source
        +Dict metadata
    }

    class ToolCallRequestEvent {
        +List~FunctionCall~ content
    }

    BaseAgentEvent <|-- ToolCallRequestEvent

    class ToolCallExecutionEvent {
        +List~FunctionExecutionResult~ content
    }

    BaseAgentEvent <|-- ToolCallExecutionEvent
```

## Group Chat Classes

```mermaid
classDiagram
    class GroupChat {
        +List~BaseAgent~ agents
        +TerminationCondition termination_condition
        +run(task) TaskResult
    }

    class SelectorGroupChat {
        +List~BaseAgent~ agents
        +BaseAgent selector
        +String selector_prompt
        +run(task) TaskResult
    }

    GroupChat <|-- SelectorGroupChat

    class TerminationCondition {
        <<interface>>
        +should_terminate(messages) Boolean
    }

    class MaxMessageTermination {
        +Integer max_messages
        +should_terminate(messages) Boolean
    }

    TerminationCondition <|-- MaxMessageTermination

    GroupChat --> TerminationCondition : uses
```

## Key Relationships

1. **Agent Inheritance**: All agents inherit from either the `Agent` interface in Core API or the `BaseAgent` class in AgentChat.

2. **Message Handling**: Agents process messages through handler methods, which can be registered using the `@message_handler` decorator in Core API.

3. **Runtime Management**: The agent runtime manages agent lifecycles and facilitates communication between agents.

4. **Group Coordination**: Group chat classes orchestrate conversations between multiple agents, with optional selection logic.

5. **Termination Logic**: Termination conditions determine when a conversation should end based on various criteria.

This class hierarchy demonstrates the extensible nature of Autogen's architecture, allowing for custom agent implementations while maintaining a consistent interface for communication and management.
