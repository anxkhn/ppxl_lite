# Perplexity AI Lite

A lightweight Python client for Perplexity AI API. Simple, clean, and focused on making API calls to integrate Perplexity AI into your projects.

## Features

- **Simple API Integration** - Easy to use with just a few lines of code
- **Multiple Search Modes** - auto, pro, reasoning, deep research
- **File Upload Support** - Analyze documents with AI
- **Streaming Responses** - Real-time response streaming
- **Multiple Sources** - web, scholar, social
- **All Major Models** - sonar, gpt-5.2, claude-4.5-sonnet, grok-4.1
- **Lightweight** - Only 1 dependency (curl-cffi)

## Installation

```bash
pip install curl-cffi
```

## Quick Start

### Basic Usage (Anonymous)

```python
from perplexity_lite import Client

# Create client (anonymous mode)
client = Client()

# Simple search
response = client.search("What is artificial intelligence?")
print(response['answer'])
```

### With Account Cookies

First, save your cookies to `cookies.json`:
```json
{
    "next-auth.csrf-token": "your-csrf-token",
    "next-auth.session-token": "your-session-token"
}
```

Then use them in your code:
```python
import json
from perplexity_lite import Client

# Load cookies
with open('cookies.json', 'r') as f:
    cookies = json.load(f)

# Create client with cookies
client = Client(cookies)

# Use pro mode with advanced model
response = client.search(
    "Explain quantum computing in detail",
    mode='pro',
    model='claude-4.5-sonnet',
    sources=['web', 'scholar']
)
print(response['answer'])
```

#### How to Get Cookies:
1. Login to [Perplexity.ai](https://perplexity.ai)
2. Open Developer Tools (F12)
3. Go to Network tab
4. Refresh page
5. Right-click first request → Copy → Copy as cURL (bash)
6. Convert at [curlconverter.com](https://curlconverter.com)
7. Extract the cookies dictionary and save to `cookies.json`

### Streaming Responses

```python
from perplexity_lite import Client

client = Client()

# Stream response in real-time
for chunk in client.search("Tell me about AI", stream=True):
    if 'answer' in chunk:
        print(chunk['answer'], end='', flush=True)
```

### File Upload

```python
from perplexity_lite import Client

client = Client(cookies)  # File upload requires account

# Upload and analyze file
with open('document.pdf', 'rb') as f:
    response = client.search(
        "Summarize this document",
        files={'document.pdf': f.read()}
    )
print(response['answer'])
```

## Available Modes and Models

### Search Modes
- `auto` - Basic search (anonymous)
- `pro` - Enhanced search with advanced models (requires account)
- `reasoning` - Complex reasoning tasks (requires account)
- `deep research` - In-depth research (requires account)

### Available Models

**Pro Mode:**
- `sonar` - Experimental backend
- `gpt-5.2` - GPT-5.2 model
- `claude-4.5-sonnet` - Claude 4.5 Sonnet
- `grok-4.1` - Grok 4.1

**Reasoning Mode:**
- `claude-4.5-sonnet-thinking` - Claude with reasoning
- `kimi-k2-thinking` - Kimi K2 thinking model
- `grok-4.1-reasoning` - Grok reasoning

## API Reference

### Client Class

```python
class Client:
    def __init__(self, cookies: Optional[Dict[str, str]] = None)

    def search(
        self,
        query: str,
        mode: str = "auto",
        model: Optional[str] = None,
        sources: List[str] = ["web"],
        files: Dict[str, Union[str, bytes]] = None,
        stream: bool = False,
        language: str = "en-US",
        follow_up: Optional[Dict] = None,
        incognito: bool = False
    ) -> Union[Dict, Generator]
```

### Parameters

- `query` (str): Search query
- `mode` (str): Search mode ('auto', 'pro', 'reasoning', 'deep research')
- `model` (str, optional): Model to use (see models list)
- `sources` (List[str]): Information sources (['web', 'scholar', 'social'])
- `files` (Dict, optional): Files to upload {filename: content}
- `stream` (bool): Enable streaming responses
- `language` (str): Language code (default: 'en-US')
- `follow_up` (Dict, optional): Previous query for context
- `incognito` (bool): Enable incognito mode

### Response Format

```python
{
    "answer": "The AI-generated answer",
    "text": "...",  # Additional response data
    "chunks": [...] # Answer chunks if available
}
```

## Use Cases

- **Research Assistants** - Quick answers to complex questions
- **Content Analysis** - Analyze documents with AI
- **Chatbots** - Add AI capabilities to your apps
- **Data Processing** - Extract insights from data
- **Educational Tools** - Explain concepts interactively

## Examples

### Research Assistant
```python
from perplexity_lite import Client
import json

with open('cookies.json', 'r') as f:
    cookies = json.load(f)

client = Client(cookies)

# Research a topic
response = client.search(
    "Latest developments in quantum computing",
    mode="deep research",
    sources=["scholar", "web"]
)

print(f"Research result: {response['answer']}")
```

### Document Q&A
```python
from perplexity_lite import Client

client = Client(cookies)

# Upload and ask questions about a document
with open('report.pdf', 'rb') as f:
    content = f.read()

response = client.search(
    "What are the key findings in this report?",
    files={'report.pdf': content}
)

print(response['answer'])
```

## License

MIT License

## Disclaimer

This is an unofficial API wrapper. Use responsibly and respect Perplexity.ai's terms of service.