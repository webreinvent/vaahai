# VaahAI Custom Agent Class Hierarchy

This document provides a detailed view of the class hierarchy in VaahAI's custom agent architecture, focusing on reusability and extensibility.

## Core Interface Hierarchy

```mermaid
classDiagram
    class IAgent {
        <<interface>>
        +initialize(config) void
        +process_message(message) Dict
        +get_capabilities() List~string~
    }
    
    class IMessageProcessor {
        <<interface>>
        +process(message) Dict
    }
    
    class ITool {
        <<interface>>
        +execute(parameters) Any
        +get_description() string
        +get_parameters() Dict
    }
    
    class IGroupChat {
        <<interface>>
        +add_agent(agent) void
        +remove_agent(agent) void
        +start_chat(message) void
        +end_chat() void
    }
    
    IAgent <|-- BaseAgent
    IMessageProcessor <|-- BaseMessageProcessor
    ITool <|-- BaseTool
    IGroupChat <|-- BaseGroupChat
```

## Agent Implementation Hierarchy

```mermaid
classDiagram
    class BaseAgent {
        <<abstract>>
        #_config Dict
        #_capabilities List~string~
        +initialize(config) void
        +process_message(message) Dict
        +get_capabilities() List~string~
        #_validate_config() bool
    }
    
    class AgentDecorator {
        <<abstract>>
        -_agent IAgent
        +initialize(config) void
        +process_message(message) Dict
        +get_capabilities() List~string~
    }
    
    BaseAgent <|-- ConversationalAgent
    BaseAgent <|-- AssistantAgent
    BaseAgent <|-- UserProxyAgent
    BaseAgent <|-- SpecializedAgent
    
    AgentDecorator <|-- LoggingAgentDecorator
    AgentDecorator <|-- MetricsAgentDecorator
    AgentDecorator <|-- CachingAgentDecorator
    AgentDecorator <|-- RateLimitingAgentDecorator
    
    SpecializedAgent <|-- CodeReviewAgent
    SpecializedAgent <|-- SecurityAuditAgent
    SpecializedAgent <|-- LanguageDetectionAgent
    SpecializedAgent <|-- ReportGenerationAgent
```

## Adapter Layer

```mermaid
classDiagram
    class IAgentAdapter {
        <<interface>>
        +initialize(config) void
        +adapt_agent(agent) void
        +adapt_message_to_external(message) Dict
        +adapt_message_from_external(message) Dict
    }
    
    class AutogenAgentAdapter {
        -_vaah_agent IAgent
        -_autogen_agent Any
        +initialize(config) void
        +adapt_agent(agent) void
        +adapt_message_to_external(message) Dict
        +adapt_message_from_external(message) Dict
        -_convert_to_autogen_format(message) Dict
        -_convert_to_vaah_format(message) Dict
    }
    
    class AutogenGroupChatAdapter {
        -_vaah_group_chat IGroupChat
        -_autogen_group_chat Any
        +initialize(config) void
        +adapt_group_chat(group_chat) void
        +adapt_message_to_external(message) Dict
        +adapt_message_from_external(message) Dict
    }
    
    IAgentAdapter <|-- AutogenAgentAdapter
    IAgentAdapter <|-- AutogenGroupChatAdapter
```

## Factory Pattern Implementation

```mermaid
classDiagram
    class AgentFactory {
        +create_agent(agent_type, config) IAgent
        +register_agent_type(agent_type, agent_class) void
        +get_registered_agent_types() List~string~
    }
    
    class GroupChatFactory {
        +create_group_chat(chat_type, config) IGroupChat
        +register_chat_type(chat_type, chat_class) void
        +get_registered_chat_types() List~string~
    }
    
    class ToolFactory {
        +create_tool(tool_type, config) ITool
        +register_tool_type(tool_type, tool_class) void
        +get_registered_tool_types() List~string~
    }
```

## Strategy Pattern Implementation

```mermaid
classDiagram
    class IMessageProcessingStrategy {
        <<interface>>
        +process(message) Dict
    }
    
    class SimpleProcessingStrategy {
        +process(message) Dict
    }
    
    class AdvancedProcessingStrategy {
        +process(message) Dict
    }
    
    class ChainProcessingStrategy {
        -_strategies List~IMessageProcessingStrategy~
        +add_strategy(strategy) void
        +process(message) Dict
    }
    
    IMessageProcessingStrategy <|-- SimpleProcessingStrategy
    IMessageProcessingStrategy <|-- AdvancedProcessingStrategy
    IMessageProcessingStrategy <|-- ChainProcessingStrategy
```

## Dependency Injection System

```mermaid
classDiagram
    class DependencyContainer {
        -_instances Map~Type, Any~
        -_factories Map~Type, Function~
        +register_instance(interface_type, instance) void
        +register_factory(interface_type, factory) void
        +resolve(interface_type) Any
    }
    
    class ServiceLocator {
        -_services Map~string, Any~
        +register_service(name, service) void
        +get_service(name) Any
        +has_service(name) bool
    }
```

## Plugin System

```mermaid
classDiagram
    class PluginManager {
        -_plugins Map~string, Any~
        +load_plugin(plugin_name, plugin_path) void
        +get_plugin(plugin_name) Any
        +register_plugin_hooks(plugin_name, hooks) void
    }
    
    class IPlugin {
        <<interface>>
        +initialize() void
        +get_hooks() Dict
        +get_name() string
        +get_version() string
    }
    
    class BasePlugin {
        <<abstract>>
        #_name string
        #_version string
        #_hooks Dict
        +initialize() void
        +get_hooks() Dict
        +get_name() string
        +get_version() string
    }
    
    IPlugin <|-- BasePlugin
```

## Event System

```mermaid
classDiagram
    class EventManager {
        -_subscribers Map~string, List~Function~~
        +subscribe(event_type, handler) void
        +publish(event_type, event_data) void
    }
    
    class IEventHandler {
        <<interface>>
        +handle_event(event_data) void
    }
    
    class BaseEventHandler {
        <<abstract>>
        +handle_event(event_data) void
    }
    
    IEventHandler <|-- BaseEventHandler
    BaseEventHandler <|-- MessageReceivedHandler
    BaseEventHandler <|-- AgentCreatedHandler
    BaseEventHandler <|-- ErrorOccurredHandler
```

## Configuration System

```mermaid
classDiagram
    class IConfig {
        <<interface>>
        +to_dict() Dict
        +validate() bool
    }
    
    class BaseConfig {
        <<abstract>>
        #_data Dict
        +to_dict() Dict
        +validate() bool
        +from_dict(data) BaseConfig
    }
    
    class AgentConfig {
        -_agent_type string
        -_parameters Dict
        +get_agent_type() string
        +get_parameters() Dict
        +set_parameter(key, value) void
    }
    
    class GroupChatConfig {
        -_chat_type string
        -_agents List~AgentConfig~
        -_parameters Dict
        +get_chat_type() string
        +get_agents() List~AgentConfig~
        +add_agent(agent_config) void
        +get_parameters() Dict
    }
    
    IConfig <|-- BaseConfig
    BaseConfig <|-- AgentConfig
    BaseConfig <|-- GroupChatConfig
```

## Reusability and Extensibility Features

This class hierarchy emphasizes reusability and extensibility through:

1. **Interface-Based Design**: All components are defined through interfaces
2. **Decorator Pattern**: For dynamically adding capabilities to agents
3. **Strategy Pattern**: For swappable message processing algorithms
4. **Adapter Pattern**: For clean integration with Autogen
5. **Factory Pattern**: For flexible object creation
6. **Dependency Injection**: For flexible component composition
7. **Plugin System**: For dynamically loading new functionality
8. **Event System**: For extensible event handling
9. **Configuration System**: For separating configuration from implementation

These patterns work together to create a highly reusable and extensible agent architecture that can adapt to changing requirements while maintaining a clean separation between VaahAI and Autogen components.
