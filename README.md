# Perplexity AI Lite

A lightweight Python client for the Perplexity AI API. Simple, focused, and minimal dependencies.

## Features

- Simple API with minimal setup
- Multiple search modes (auto, pro, reasoning, deep research, labs, study)
- File upload support for document analysis
- Streaming responses
- Multiple sources (web, scholar, social)
- Support for 70+ models from OpenAI, Anthropic, Google, xAI, and others

## Requirements

- Python 3.8+
- curl-cffi

## Installation

```bash
pip install curl-cffi
```

## Quick Start

### Anonymous Mode

```python
from client import Client

client = Client()
response = client.search("What is artificial intelligence?")
print(response['answer'])
```

### With Authentication

Most features require authentication cookies from your Perplexity account.

1. Create `cookies.json` with your session cookies:

```json
{
  "next-auth.csrf-token": "your-csrf-token",
  "next-auth.session-token": "your-session-token"
}
```

2. Use in your code:

```python
import json
from client import Client

with open('cookies.json', 'r') as f:
    cookies = json.load(f)

client = Client(cookies)

response = client.search(
    "Explain quantum computing",
    mode='pro',
    model='gpt52',
    sources=['web', 'scholar']
)
print(response['answer'])
```

### Getting Cookies

1. Login to [perplexity.ai](https://perplexity.ai)
2. Open Developer Tools (F12)
3. Go to Network tab
4. Refresh the page
5. Right-click the first request, Copy as cURL
6. Convert at [curlconverter.com](https://curlconverter.com)
7. Extract cookies and save to `cookies.json`

## API Reference

### Client Class

```python
Client(cookies: Optional[Dict[str, str]] = None)
```

### get_user_info Method

```python
client.get_user_info() -> Optional[Dict]
```

Returns user info including email, username, subscription_tier, or None if not authenticated.

### get_limits Method

```python
client.get_limits() -> Optional[Dict]
```

Returns usage limits including gpt4_limit, pplx_alpha_limit, query_count, etc.

### search Method

```python
client.search(
    query: str,
    mode: str = "auto",
    model: Optional[str] = None,
    sources: List[str] = ["web"],
    files: Dict[str, bytes] = None,
    stream: bool = False,
    language: str = "en-US",
    follow_up: Optional[Dict] = None,
    incognito: bool = False
) -> Union[Dict, Generator]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| query | str | required | Search query |
| mode | str | "auto" | Search mode |
| model | str | None | Specific model to use |
| sources | list | ["web"] | Information sources |
| files | dict | None | Files to upload |
| stream | bool | False | Enable streaming |
| language | str | "en-US" | Language code |
| follow_up | dict | None | Previous query context |
| incognito | bool | False | Incognito mode |

**Response:**

```python
{
    "answer": "The AI-generated response",
    "text": "...",
    "chunks": [...]
}
```

## Search Modes

| Mode | Backend | Description | Auth Required |
|------|---------|-------------|---------------|
| auto | search | Fast default search | No |
| pro | search | Advanced models | Yes |
| reasoning | search | Complex reasoning | Yes |
| deep research | research | In-depth research | Yes |
| labs | studio | Multi-step tasks | Yes |
| study | study | Routine research | Yes |

## Available Models

See [MODELS.md](MODELS.md) for the complete list of 70+ available models.

**Quick Reference:**

- **Fast:** `turbo` (anonymous), `experimental` (Sonar)
- **Quality:** `gpt52`, `claude45sonnet`, `gemini30pro`
- **Reasoning:** `gpt52_thinking`, `claude45sonnetthinking`
- **Research:** `pplx_alpha`, `o3pro_research`

## Examples

### Streaming Response

```python
for chunk in client.search("Tell me about AI", stream=True):
    if 'answer' in chunk:
        print(chunk['answer'], end='', flush=True)
```

### File Upload

```python
with open('document.pdf', 'rb') as f:
    response = client.search(
        "Summarize this document",
        files={'document.pdf': f.read()}
    )
```

### Deep Research

```python
response = client.search(
    "Latest developments in quantum computing",
    mode="deep research",
    model="pplx_alpha",
    sources=["scholar", "web"]
)
```

## Project Structure

```
ppxl_lite/
  __init__.py      # Package exports
  client.py        # Main client class
  config.py        # Models and configuration
  cookies.json     # Your authentication (git-ignored)
  example.py       # Usage examples
  verify_cookies.py # Cookie verification
  test_*.py        # Test scripts
```

## Troubleshooting

**401 Unauthorized:** Refresh your cookies from browser.

**Model not available:** Check account tier. Some models require Pro or Max subscription.

**No answer in response:** Model may be deprecated or not available for your account type.

**502 errors:** Temporary API issues. Retry after a few seconds.

## License

MIT License - see LICENSE file.

## Disclaimer

This is an unofficial API wrapper. Use responsibly and respect Perplexity.ai's terms of service.
