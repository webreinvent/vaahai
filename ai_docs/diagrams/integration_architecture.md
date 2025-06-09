# Autogen Integration Architecture

This document contains architecture diagrams illustrating how Microsoft Autogen components will integrate with VaahAI. These diagrams provide a visual representation of the integration approach, component relationships, and data flows.

## Table of Contents
1. [High-Level Integration Architecture](#high-level-integration-architecture)
2. [Agent Integration Layer](#agent-integration-layer)
3. [Group Chat Integration](#group-chat-integration)
4. [Message Flow Architecture](#message-flow-architecture)
5. [Tool Integration Architecture](#tool-integration-architecture)
6. [Configuration Integration](#configuration-integration)
7. [Extension Points](#extension-points)

## High-Level Integration Architecture

This diagram shows the high-level architecture of VaahAI with Autogen integration, illustrating the major components and their relationships.

```mermaid
flowchart TB
    subgraph VaahAI["VaahAI Framework"]
        CLI["CLI Interface"]
        Config["Configuration Manager"]
        LLMProviders["LLM Provider Interface"]
        AgentFactory["Agent Factory"]

        subgraph AgentArch["Agent Architecture"]
            BaseAgent["Base Agent Interface"]
            SpecializedAgents["Specialized Agents"]
        end

        subgraph ConvManagement["Conversation Management"]
            ConvManager["Conversation Manager"]
            ConvHistory["Conversation History"]
        end

        subgraph ToolIntegration["Tool Integration"]
            ToolRegistry["Tool Registry"]
            ToolExecution["Tool Execution Engine"]
        end
    end

    subgraph AutogenCore["Autogen Core"]
        AutogenAgents["Autogen Agents"]
        AutogenMessages["Message System"]
        AutogenGroupChat["Group Chat"]
    end

    CLI --> Config
    Config --> LLMProviders
    Config --> AgentFactory
    LLMProviders --> AgentFactory
    AgentFactory --> BaseAgent
    BaseAgent --> SpecializedAgents
    BaseAgent --> ConvManager
    ConvManager --> ConvHistory
    BaseAgent --> ToolRegistry
    ToolRegistry --> ToolExecution

    %% Integration points
    BaseAgent -.-> AutogenAgents
    ConvManager -.-> AutogenGroupChat
    ConvHistory -.-> AutogenMessages
    ToolRegistry -.-> AutogenMessages

    classDef vaahai fill:#f9f,stroke:#333,stroke-width:2px
    classDef autogen fill:#bbf,stroke:#333,stroke-width:2px
    classDef integration fill:#bfb,stroke:#333,stroke-width:2px

    class VaahAI,CLI,Config,LLMProviders,AgentFactory,AgentArch,ConvManagement,ToolIntegration,BaseAgent,SpecializedAgents,ConvManager,ConvHistory,ToolRegistry,ToolExecution vaahai
    class AutogenCore,AutogenAgents,AutogenMessages,AutogenGroupChat autogen
```

## Agent Integration Layer

This diagram illustrates how VaahAI's agent architecture integrates with Autogen's agent system.

```mermaid
classDiagram
    class IAgent {
        <<interface>>
        +initialize()
        +process_message()
        +generate_response()
        +handle_tool_calls()
    }

    class BaseAgent {
        +name: str
        +system_message: str
        +model_config: dict
        +initialize()
        +process_message()
        +generate_response()
        +handle_tool_calls()
    }

    class AutogenAgentAdapter {
        +autogen_agent: AutogenAgent
        +initialize()
        +process_message()
        +generate_response()
        +handle_tool_calls()
        -adapt_message_to_autogen()
        -adapt_autogen_response()
    }

    class AutogenAgent {
        +name: str
        +system_message: str
        +llm_config: dict
        +register_reply()
        +generate_reply()
        +receive()
        +send()
    }

    class AssistantAgent {
        +generate_reply()
    }

    class UserProxyAgent {
        +human_input_mode: str
        +get_human_input()
    }

    class VaahAIAssistantAgent {
        +specialized_capabilities: dict
        +process_specialized_tasks()
    }

    class VaahAIUserProxyAgent {
        +input_mode: str
        +get_user_input()
    }

    IAgent <|.. BaseAgent
    BaseAgent <|-- AutogenAgentAdapter
    AutogenAgentAdapter o-- AutogenAgent
    AutogenAgent <|-- AssistantAgent
    AutogenAgent <|-- UserProxyAgent
    AutogenAgentAdapter <|-- VaahAIAssistantAgent
    AutogenAgentAdapter <|-- VaahAIUserProxyAgent

    note for AutogenAgentAdapter "Adapter pattern to integrate\nAutogen agents with VaahAI"
```

## Group Chat Integration

This diagram shows how VaahAI's conversation management integrates with Autogen's group chat functionality.

```mermaid
classDiagram
    class IConversationManager {
        <<interface>>
        +initialize_conversation()
        +add_participant()
        +remove_participant()
        +send_message()
        +get_history()
        +terminate_conversation()
    }

    class BaseConversationManager {
        +conversation_id: str
        +participants: list
        +history: list
        +initialize_conversation()
        +add_participant()
        +remove_participant()
        +send_message()
        +get_history()
        +terminate_conversation()
    }

    class AutogenGroupChatAdapter {
        +group_chat: AutogenGroupChat
        +initialize_conversation()
        +add_participant()
        +remove_participant()
        +send_message()
        +get_history()
        +terminate_conversation()
        -adapt_message_to_autogen()
        -adapt_autogen_response()
    }

    class AutogenGroupChat {
        +agents: list
        +messages: list
        +selector: function
        +run()
        +select_speaker()
        +append_message()
        +terminate()
    }

    class RoundRobinGroupChat {
        +select_speaker()
    }

    class SelectorGroupChat {
        +selector_agent: Agent
        +select_speaker()
    }

    class VaahAIRoundRobinChat {
        +custom_termination: function
        +check_termination()
    }

    class VaahAISelectorChat {
        +custom_selector: function
        +select_next_speaker()
    }

    IConversationManager <|.. BaseConversationManager
    BaseConversationManager <|-- AutogenGroupChatAdapter
    AutogenGroupChatAdapter o-- AutogenGroupChat
    AutogenGroupChat <|-- RoundRobinGroupChat
    AutogenGroupChat <|-- SelectorGroupChat
    AutogenGroupChatAdapter <|-- VaahAIRoundRobinChat
    AutogenGroupChatAdapter <|-- VaahAISelectorChat

    note for AutogenGroupChatAdapter "Adapter pattern to integrate\nAutogen group chats with VaahAI"
```

## Message Flow Architecture

This diagram illustrates the flow of messages between VaahAI and Autogen components.

```mermaid
sequenceDiagram
    participant User
    participant VaahAI_CLI
    participant VaahAI_ConvManager
    participant Autogen_GroupChat
    participant Autogen_Agent1
    participant Autogen_Agent2
    participant Autogen_ToolExecution

    User->>VaahAI_CLI: Input message
    VaahAI_CLI->>VaahAI_ConvManager: Process message
    VaahAI_ConvManager->>Autogen_GroupChat: Adapt and forward message

    Autogen_GroupChat->>Autogen_GroupChat: Select next speaker
    Autogen_GroupChat->>Autogen_Agent1: Forward message
    Autogen_Agent1->>Autogen_GroupChat: Generate response

    alt Tool Call Detected
        Autogen_GroupChat->>Autogen_ToolExecution: Execute tool
        Autogen_ToolExecution->>Autogen_GroupChat: Tool result
    end

    Autogen_GroupChat->>Autogen_GroupChat: Select next speaker
    Autogen_GroupChat->>Autogen_Agent2: Forward message history
    Autogen_Agent2->>Autogen_GroupChat: Generate response

    Autogen_GroupChat->>VaahAI_ConvManager: Return conversation result
    VaahAI_ConvManager->>VaahAI_CLI: Format and display result
    VaahAI_CLI->>User: Display output
```

## Tool Integration Architecture

This diagram shows how VaahAI's tool system integrates with Autogen's tool calling capabilities.

```mermaid
flowchart TB
    subgraph VaahAI["VaahAI Tool System"]
        ToolRegistry["Tool Registry"]
        ToolExecutor["Tool Executor"]
        ToolResults["Tool Results Handler"]
    end

    subgraph Autogen["Autogen Tool System"]
        AgentToolCalls["Agent Tool Calls"]
        ToolMessages["Tool Messages"]
        ToolCallbacks["Tool Callbacks"]
    end

    subgraph Tools["Available Tools"]
        CodeExecution["Code Execution"]
        WebSearch["Web Search"]
        DataAnalysis["Data Analysis"]
        FileOperations["File Operations"]
    end

    ToolRegistry -->|"Register"| Tools
    AgentToolCalls -->|"Request"| ToolMessages
    ToolMessages -->|"Dispatch"| ToolCallbacks
    ToolCallbacks -->|"Execute via"| ToolExecutor
    ToolExecutor -->|"Execute"| Tools
    Tools -->|"Return results"| ToolResults
    ToolResults -->|"Format"| ToolMessages

    %% Integration points
    ToolRegistry -.->|"Sync"| ToolCallbacks
    ToolExecutor -.->|"Adapt"| ToolCallbacks
    ToolResults -.->|"Adapt"| ToolMessages

    classDef vaahai fill:#f9f,stroke:#333,stroke-width:2px
    classDef autogen fill:#bbf,stroke:#333,stroke-width:2px
    classDef tools fill:#fbb,stroke:#333,stroke-width:2px

    class VaahAI,ToolRegistry,ToolExecutor,ToolResults vaahai
    class Autogen,AgentToolCalls,ToolMessages,ToolCallbacks autogen
    class Tools,CodeExecution,WebSearch,DataAnalysis,FileOperations tools
```

## Configuration Integration

This diagram illustrates how VaahAI's configuration system integrates with Autogen's configuration requirements.

```mermaid
classDiagram
    class VaahAIConfig {
        +load_config()
        +validate_config()
        +get_config_value()
        +set_config_value()
    }

    class AutogenConfig {
        +llm_config: dict
        +agent_config: dict
        +group_chat_config: dict
    }

    class ConfigAdapter {
        +adapt_llm_config()
        +adapt_agent_config()
        +adapt_group_chat_config()
    }

    class LLMConfig {
        +provider: str
        +model: str
        +parameters: dict
    }

    class AgentConfig {
        +name: str
        +role: str
        +capabilities: list
    }

    class GroupChatConfig {
        +type: str
        +max_rounds: int
        +termination_conditions: list
    }

    VaahAIConfig --> ConfigAdapter
    ConfigAdapter --> AutogenConfig
    VaahAIConfig --> LLMConfig
    VaahAIConfig --> AgentConfig
    VaahAIConfig --> GroupChatConfig
    ConfigAdapter ..> LLMConfig
    ConfigAdapter ..> AgentConfig
    ConfigAdapter ..> GroupChatConfig
```

## Extension Points

This diagram highlights the extension points in the integration architecture that allow for customization and enhancement.

```mermaid
flowchart TB
    subgraph VaahAI["VaahAI Core"]
        BaseComponents["Base Components"]
    end

    subgraph ExtensionPoints["Extension Points"]
        CustomAgents["Custom Agent Types"]
        CustomGroupChats["Custom Group Chat Patterns"]
        CustomTools["Custom Tool Integration"]
        CustomTermination["Custom Termination Logic"]
        CustomSelectors["Custom Speaker Selectors"]
    end

    subgraph Autogen["Autogen Integration"]
        AutogenCore["Autogen Core Components"]
    end

    BaseComponents -->|"Extend"| ExtensionPoints
    ExtensionPoints -->|"Integrate with"| AutogenCore

    classDef vaahai fill:#f9f,stroke:#333,stroke-width:2px
    classDef extension fill:#bfb,stroke:#333,stroke-width:2px
    classDef autogen fill:#bbf,stroke:#333,stroke-width:2px

    class VaahAI,BaseComponents vaahai
    class ExtensionPoints,CustomAgents,CustomGroupChats,CustomTools,CustomTermination,CustomSelectors extension
    class Autogen,AutogenCore autogen
```

These diagrams provide a comprehensive visual representation of how Microsoft Autogen components will integrate with VaahAI, highlighting the key architectural components, relationships, and extension points.
