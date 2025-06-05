# Message Handling in VaahAI

This document describes the message handling system in VaahAI, including message structure, validation, processing, and integration with agents.

## Message Structure

Messages in VaahAI follow a standardized structure defined by JSON schemas. Each message has:

- `message_id`: Unique identifier for the message
- `sender_id`: Identifier of the sender agent
- `receiver_id`: Identifier of the intended recipient agent
- `timestamp`: ISO-formatted timestamp of when the message was created
- `message_type`: Type of message (text, function_call, function_result, error, system)
- `content`: Content of the message, structure depends on message type
- `conversation_id`: Identifier for the conversation this message belongs to
- `in_reply_to`: Optional ID of the message this is replying to
- `metadata`: Optional additional metadata for the message

## Message Types

VaahAI supports the following message types:

1. **Text Messages**: Simple text content with optional formatting
2. **Function Call Messages**: Request to execute a function with arguments
3. **Function Result Messages**: Result of a function execution
4. **Error Messages**: Information about errors that occurred
5. **System Messages**: System-level notifications and commands

## Message Class

The `Message` class provides an object-oriented interface for working with messages:

```python
# Creating a text message
message = Message.create_text_message(
    sender_id="user",
    receiver_id="assistant",
    text="Hello, how are you?",
    format="plain"
)

# Creating a function call message
message = Message.create_function_call(
    sender_id="assistant",
    receiver_id="tool_agent",
    function_name="get_weather",
    arguments={"location": "San Francisco"},
    description="Get weather information"
)
```

## Message Validation

All messages are validated against JSON schemas defined in `message_schema.py`. The validation ensures:

- Required fields are present
- Field types are correct
- Message content matches the expected structure for its type
- Additional properties are allowed for extensibility

## Message Processing

The `MessageProcessor` class provides a framework for processing messages:

```python
class CustomProcessor(MessageProcessor):
    async def process(self, message):
        # Process the message
        message.get_content()["processed"] = True
        return message
```

## Message Bus

The `MessageBus` facilitates communication between agents:

- Publishers can send messages to specific recipients
- Subscribers can register to receive messages
- Message processors can be attached to transform messages
- Message history is maintained for each conversation

## Integration with Agents

Agents implement the `process_message` method to handle incoming messages:

```python
async def process_message(self, message):
    # Process the message through registered processors
    for processor in self._message_processors:
        message = await processor.process(message)
    
    # Generate a response
    response = await self._generate_response(message)
    
    # Add the message and response to history
    self._add_to_history(message)
    self._add_to_history(response)
    
    return response
```

## Testing

The message handling system includes comprehensive tests:

- Unit tests for the `Message` class and its validation
- Tests for `MessageProcessor` and `MessageBus`
- Integration tests with agent implementations
- Tests for specialized agent message handling
