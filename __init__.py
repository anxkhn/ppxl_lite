"""
Perplexity AI Lite - Lightweight Python client for Perplexity AI API.

A simplified version that removes browser automation and account creation,
focusing only on making API calls with existing cookies.
"""

from client import Client

__version__ = "2.0.0"
__all__ = ["Client"]