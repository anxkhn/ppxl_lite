# Perplexity AI Lite

A lightweight Python client for the Perplexity AI API. Use your existing Free, Pro, or Max account to access Perplexity's AI capabilities via Python without paying per-API-call pricing.

This is an unofficial library based on independent reverse engineering.

## Features

- Use your existing Perplexity account (Free/Pro/Max)
- Multiple search modes (auto, pro, reasoning, deep research, labs, study)
- File upload support for document analysis
- Streaming responses
- Multiple sources (web, scholar, social)
- 70+ models from OpenAI, Anthropic, Google, xAI, and others

**For the complete list of models and their availability, see [MODELS.md](MODELS.md).**

## Requirements

- Python 3.8+
- curl-cffi

## Installation

```bash
pip install curl-cffi
```

## Quick Start

```python
import json
from client import Client

with open('cookies.json', 'r') as f:
    cookies = json.load(f)

client = Client(cookies)

response = client.search("What is quantum computing?", mode='pro', model='gpt52')
print(response['answer'])
```

## Authentication

Most features require authentication cookies from your Perplexity account.

Create `cookies.json`:

```json
{
  "next-auth.csrf-token": "your-csrf-token",
  "next-auth.session-token": "your-session-token"
}
```

### Getting Cookies

1. Login to [perplexity.ai](https://perplexity.ai)
2. Open Developer Tools (F12)
3. Go to Network tab
4. Refresh the page
5. Right-click the first request, Copy as cURL
6. Convert at [curlconverter.com](https://curlconverter.com)
7. Extract cookies and save to `cookies.json`

### Verify Authentication

Use `get_user_info()` to check if your cookies work:

```python
client = Client(cookies)

user = client.get_user_info()
if user:
    print(f"Logged in as: {user['email']}")
    print(f"Subscription: {user['subscription_tier']}")
else:
    print("Not authenticated")
```

### Check Usage Limits

Use `get_limits()` to see your remaining quota:

```python
limits = client.get_limits()
if limits:
    print(f"Pro searches remaining: {limits['gpt4_limit']}")
    print(f"Research quota: {limits['pplx_alpha_limit']}")
    print(f"Labs quota: {limits['pplx_beta_limit']}")
    print(f"Total queries made: {limits['query_count']}")
```

## API Reference

### Client(cookies)

Create a client instance. Pass cookies for authenticated access.

### get_user_info()

Returns user info (email, username, subscription_tier) or None if not authenticated.

### get_limits()

Returns usage limits (gpt4_limit, pplx_alpha_limit, query_count, etc.) or None.

### search(query, mode, model, sources, files, stream, language, follow_up, incognito)

Execute a search query.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| query | str | required | Search query |
| mode | str | "auto" | Search mode |
| model | str | None | Specific model |
| sources | list | ["web"] | Information sources |
| files | dict | None | Files to upload |
| stream | bool | False | Enable streaming |
| language | str | "en-US" | Language code |
| follow_up | dict | None | Previous query context |
| incognito | bool | False | Incognito mode |

## Search Modes

| Mode | Description | Limits |
|------|-------------|--------|
| auto | Basic search with Turbo | Unlimited |
| pro | Advanced search with model selection | Unlimited for Pro/Max |
| reasoning | Complex reasoning with thinking models | Unlimited for Pro/Max |
| deep research | Extended research | Limited for Pro, unlimited for Max |
| labs | Multi-step tasks | 50/month for Pro, unlimited for Max |
| study | Routine research | New mode |

**See [MODELS.md](MODELS.md) for the complete list of 70+ available models.**

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
  __init__.py
  client.py
  config.py
  models.json
  cookies.example.json
  pyproject.toml
  requirements.txt
  LICENSE
  README.md
  MODELS.md
```

## Troubleshooting

**401 Unauthorized:** Refresh your cookies from browser.

**Model not available:** Check your account tier. Some models require Pro or Max subscription.

**No answer in response:** Model may be deprecated or not available for your account.

## License

MIT License

## Disclaimer

This is an unofficial API wrapper based on independent reverse engineering. Use responsibly and respect Perplexity.ai's terms of service.
