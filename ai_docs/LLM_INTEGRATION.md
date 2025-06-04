# VaahAI LLM Integration

This document details how VaahAI integrates with various Large Language Model (LLM) providers, explaining the architecture, abstraction layers, and implementation details.

## LLM Integration Overview

VaahAI supports multiple LLM providers through a unified abstraction layer, allowing users to choose their preferred provider while maintaining consistent functionality.

## Supported LLM Providers

### OpenAI

- Models: GPT-3.5-Turbo, GPT-4
- API: OpenAI REST API
- Authentication: API Key
- Features: Chat completions, function calling, streaming responses

### Anthropic Claude

- Models: Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku
- API: Anthropic REST API
- Authentication: API Key
- Features: Chat completions, streaming responses

### Junie

- Models: Junie models
- API: Junie REST API
- Authentication: API Key
- Features: Chat completions

### Ollama (Local)

- Models: Various open-source models
- API: Ollama REST API
- Authentication: None (local)
- Features: Local execution, no data transmission

## LLM Provider Interface

VaahAI implements a provider interface that abstracts the differences between LLM services:

```python
class LLMProvider:
    """Base class for LLM providers."""
    
    def __init__(self, config):
        """Initialize with configuration."""
        self.config = config
    
    def generate(self, prompt, options=None):
        """Generate a response to the prompt."""
        raise NotImplementedError("Providers must implement generate")
    
    def generate_stream(self, prompt, options=None):
        """Generate a streaming response to the prompt."""
        raise NotImplementedError("Providers must implement generate_stream")
    
    def validate_connection(self):
        """Validate the connection to the provider."""
        raise NotImplementedError("Providers must implement validate_connection")
```

## Provider Implementation

Each provider implements the LLMProvider interface with provider-specific logic:

### OpenAI Implementation

```python
class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""
    
    def __init__(self, config):
        """Initialize with configuration."""
        super().__init__(config)
        self.client = openai.Client(api_key=self._get_api_key())
    
    def generate(self, prompt, options=None):
        """Generate a response using OpenAI."""
        options = options or {}
        response = self.client.chat.completions.create(
            model=self.config.get("llm.model", "gpt-4"),
            messages=[{"role": "user", "content": prompt}],
            temperature=options.get("temperature", self.config.get("llm.temperature", 0.7)),
            max_tokens=options.get("max_tokens", self.config.get("llm.max_tokens", 2000)),
        )
        return response.choices[0].message.content
    
    def generate_stream(self, prompt, options=None):
        """Generate a streaming response using OpenAI."""
        options = options or {}
        response = self.client.chat.completions.create(
            model=self.config.get("llm.model", "gpt-4"),
            messages=[{"role": "user", "content": prompt}],
            temperature=options.get("temperature", self.config.get("llm.temperature", 0.7)),
            max_tokens=options.get("max_tokens", self.config.get("llm.max_tokens", 2000)),
            stream=True,
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def validate_connection(self):
        """Validate the connection to OpenAI."""
        try:
            self.client.models.list()
            return True
        except Exception as e:
            raise ConnectionError(f"Failed to connect to OpenAI: {e}")
    
    def _get_api_key(self):
        """Get the API key from secure storage."""
        # Implementation
```

## Provider Factory

A factory pattern is used to create the appropriate provider based on configuration:

```python
class LLMProviderFactory:
    """Factory for creating LLM providers."""
    
    @staticmethod
    def create_provider(config):
        """Create an LLM provider based on configuration."""
        provider_name = config.get("llm.provider", "openai").lower()
        
        if provider_name == "openai":
            return OpenAIProvider(config)
        elif provider_name == "claude":
            return ClaudeProvider(config)
        elif provider_name == "junie":
            return JunieProvider(config)
        elif provider_name == "ollama":
            return OllamaProvider(config)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")
```

## Prompt Management

VaahAI manages prompts through a template system:

```python
class PromptTemplate:
    """Template for LLM prompts."""
    
    def __init__(self, template_path):
        """Initialize with template path."""
        with open(template_path, "r") as f:
            self.template = f.read()
    
    def format(self, **kwargs):
        """Format the template with the provided variables."""
        return self.template.format(**kwargs)
```

## Response Processing

Responses from LLMs are processed and normalized:

```python
class ResponseProcessor:
    """Process and normalize LLM responses."""
    
    def process_json(self, response_text):
        """Extract and parse JSON from response."""
        try:
            # Find JSON in response
            json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = response_text
            
            # Parse JSON
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")
    
    def process_markdown(self, response_text):
        """Process markdown response."""
        # Implementation
    
    def process_text(self, response_text):
        """Process plain text response."""
        # Implementation
```

## Error Handling

VaahAI implements robust error handling for LLM interactions:

```python
class LLMError(Exception):
    """Base class for LLM-related errors."""
    pass

class ConnectionError(LLMError):
    """Error connecting to LLM provider."""
    pass

class AuthenticationError(LLMError):
    """Authentication error with LLM provider."""
    pass

class QuotaExceededError(LLMError):
    """Quota exceeded with LLM provider."""
    pass

class ContentFilterError(LLMError):
    """Content filtered by LLM provider."""
    pass

class ResponseFormatError(LLMError):
    """Error in response format from LLM."""
    pass
```

## Retry Logic

For transient errors, VaahAI implements retry logic:

```python
def with_retry(func):
    """Decorator for retrying LLM operations."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except (ConnectionError, TimeoutError) as e:
                if attempt == max_retries - 1:
                    raise
                
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2
    
    return wrapper
```

## Rate Limiting

To respect API rate limits, VaahAI implements rate limiting:

```python
class RateLimiter:
    """Rate limiter for API calls."""
    
    def __init__(self, calls_per_minute):
        """Initialize with calls per minute."""
        self.calls_per_minute = calls_per_minute
        self.call_times = collections.deque()
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        now = time.time()
        
        # Remove old calls
        while self.call_times and now - self.call_times[0] > 60:
            self.call_times.popleft()
        
        # Check if rate limit would be exceeded
        if len(self.call_times) >= self.calls_per_minute:
            # Wait until oldest call is more than 60 seconds ago
            sleep_time = 60 - (now - self.call_times[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        # Record this call
        self.call_times.append(time.time())
```

## Token Management

To optimize token usage and costs, VaahAI implements token counting:

```python
class TokenCounter:
    """Count tokens for LLM requests."""
    
    def __init__(self, model):
        """Initialize with model."""
        self.model = model
        self.encoding = tiktoken.encoding_for_model(model)
    
    def count_tokens(self, text):
        """Count tokens in text."""
        return len(self.encoding.encode(text))
    
    def truncate_to_tokens(self, text, max_tokens):
        """Truncate text to fit within max_tokens."""
        tokens = self.encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text
        
        truncated_tokens = tokens[:max_tokens]
        return self.encoding.decode(truncated_tokens)
```

## Streaming Support

For responsive user experience, VaahAI supports streaming responses:

```python
def process_streaming_response(stream, callback):
    """Process a streaming response with callback."""
    full_response = ""
    
    for chunk in stream:
        full_response += chunk
        callback(chunk, full_response)
    
    return full_response
```

## Caching

To improve performance and reduce API costs, VaahAI implements response caching:

```python
class ResponseCache:
    """Cache for LLM responses."""
    
    def __init__(self, cache_dir=None, ttl=3600):
        """Initialize with cache directory and TTL."""
        self.cache_dir = cache_dir or os.path.join(os.path.expanduser("~"), ".vaahai", "cache")
        self.ttl = ttl
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def get(self, key):
        """Get cached response for key."""
        cache_file = self._get_cache_file(key)
        
        if not os.path.exists(cache_file):
            return None
        
        # Check if cache is expired
        if time.time() - os.path.getmtime(cache_file) > self.ttl:
            os.remove(cache_file)
            return None
        
        with open(cache_file, "r") as f:
            return f.read()
    
    def set(self, key, value):
        """Set cached response for key."""
        cache_file = self._get_cache_file(key)
        
        with open(cache_file, "w") as f:
            f.write(value)
    
    def _get_cache_file(self, key):
        """Get cache file path for key."""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, key_hash)
```

## Security Considerations

VaahAI implements several security measures for LLM integration:

1. **API Key Security**:
   - API keys are stored in the system keyring
   - Keys are never logged or exposed in error messages
   - Environment variables can be used as an alternative

2. **Data Privacy**:
   - Option for local LLM execution via Ollama
   - Clear documentation of what data is sent to external services
   - No unnecessary data transmission

3. **Content Filtering**:
   - Respect provider content policies
   - Handle content filter errors gracefully
   - Provide clear user feedback on filtered content

## Performance Considerations

VaahAI optimizes LLM performance through:

1. **Prompt Optimization**:
   - Efficient prompt design to minimize tokens
   - Clear instructions to reduce clarification rounds
   - Examples for few-shot learning when beneficial

2. **Batching**:
   - Combine related requests when possible
   - Process results in parallel

3. **Streaming**:
   - Stream responses for better user experience
   - Process partial results as they arrive

## Provider-Specific Considerations

### OpenAI

- Function calling for structured outputs
- Support for GPT-4 vision capabilities
- Handling of content policy restrictions

### Claude

- Longer context windows
- Different prompt formatting requirements
- Tool use capabilities

### Junie

- Specific API limitations and features
- Response format differences

### Ollama

- Local execution considerations
- Model download and management
- Performance tuning for local hardware

## Extension Points

The LLM integration architecture supports extension through:

1. **Custom Providers**:
   - Implement the LLMProvider interface
   - Register with the provider factory

2. **Custom Prompt Templates**:
   - Create new prompt templates
   - Override default templates

3. **Response Processors**:
   - Add custom response processing
   - Support new output formats
