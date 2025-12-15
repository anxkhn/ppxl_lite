import json
from pathlib import Path
from typing import Dict, Optional

_models_path = Path(__file__).parent / "models.json"
with open(_models_path, "r") as f:
    MODEL_INFO: Dict[str, Dict] = json.load(f)

API_BASE_URL = "https://www.perplexity.ai"
API_TIMEOUT = 30

ENDPOINT_SSE_ASK = f"{API_BASE_URL}/rest/sse/perplexity_ask"
ENDPOINT_UPLOAD_URL = f"{API_BASE_URL}/rest/uploads/create_upload_url"

SEARCH_MODES = ["auto", "pro", "reasoning", "deep research", "labs", "study"]
SEARCH_SOURCES = ["web", "scholar", "social"]

MODELS = {
    "auto": ["turbo"],
    "pro": [
        "experimental",
        "pplx_pro",
        "pplx_pro_upgraded",
        "gpt4",
        "gpt4o",
        "gpt41",
        "gpt5",
        "gpt51",
        "gpt52",
        "gpt5_pro",
        "claude2",
        "claude3opus",
        "claude35haiku",
        "claude40opus",
        "claude41opus",
        "claude45opus",
        "claude45sonnet",
        "claude_ombre_eap",
        "claude_lace_eap",
        "gemini",
        "gemini2flash",
        "gemini25pro",
        "gemini30pro",
        "grok",
        "grok2",
        "grok4nonthinking",
        "grok41nonreasoning",
        "kimik2thinking",
        "llama_x_large",
        "mistral",
        "copilot",
        "r1",
        "o3mini",
        "o3",
        "o3pro",
        "pplx_gamma",
        "pplx_reasoning",
        "pplx_sonar_internal_testing",
        "pplx_sonar_internal_testing_v2",
    ],
    "reasoning": [
        "gpt5_thinking",
        "gpt51_thinking",
        "gpt52_thinking",
        "claude37sonnetthinking",
        "claude40opusthinking",
        "claude41opusthinking",
        "claude45opusthinking",
        "claude45sonnetthinking",
        "grok4",
        "grok41reasoning",
        "kimik2thinking",
        "o3",
        "o3mini",
        "pplx_reasoning",
    ],
    "deep research": [
        "pplx_alpha",
        "o4mini",
        "o3pro_research",
        "o3_research",
        "claude40sonnet_research",
        "claude40sonnetthinking_research",
        "claude40opus_research",
        "claude40opusthinking_research",
    ],
    "labs": [
        "pplx_beta",
        "o3pro_labs",
        "o3_labs",
        "claude40sonnetthinking_labs",
        "claude40opusthinking_labs",
    ],
    "study": ["pplx_study"],
}

DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
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


def get_model_info(model_id: str) -> Dict:
    return MODEL_INFO.get(
        model_id,
        {"name": model_id, "description": "Unknown model", "backend": "search"},
    )


def get_backend_for_model(mode: str, model: Optional[str]) -> str:
    if model is None:
        models_for_mode = MODELS.get(mode, ["turbo"])
        return models_for_mode[0] if models_for_mode else "turbo"
    return model
