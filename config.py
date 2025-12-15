"""
Configuration constants for Perplexity AI API (Lite Version) - Clean Version.

Simplified configuration with essential API endpoints and only working models.
"""

from typing import Dict, Optional

# API Configuration
API_BASE_URL = "https://www.perplexity.ai"
API_TIMEOUT = 30

# Essential Endpoints
ENDPOINT_SSE_ASK = f"{API_BASE_URL}/rest/sse/perplexity_ask"
ENDPOINT_UPLOAD_URL = f"{API_BASE_URL}/rest/uploads/create_upload_url"

# Search Modes
SEARCH_MODES = ["auto", "pro", "reasoning", "deep research"]
SEARCH_SOURCES = ["web", "scholar", "social"]

# Model Mappings - Only working models included
MODEL_MAPPINGS: Dict[str, Dict[Optional[str], str]] = {
    "auto": {None: "turbo"},
    "pro": {
        None: "pplx_pro",
        "sonar": "experimental",
        "gpt-5.2": "gpt52",
        "claude-4.5-sonnet": "claude45sonnet",
        "grok-4.1": "grok41nonreasoning",
    },
    "reasoning": {
        None: "pplx_reasoning",
        "claude-4.5-sonnet-thinking": "claude45sonnetthinking",
        "kimi-k2-thinking": "kimik2thinking",
        "grok-4.1-reasoning": "grok41reasoning",
    },
    "deep research": {None: "pplx_alpha"},
}

# HTTP Headers (Chrome impersonation)
DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "dnt": "1",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not;A=Brand";v="24", "Chromium";v="128"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"128.0.6613.120"',
    "sec-ch-ua-full-version-list": '"Not;A=Brand";v="24.0.0.0", "Chromium";v="128.0.6613.120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": '"19.0.0"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}