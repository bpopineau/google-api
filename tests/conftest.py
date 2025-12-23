"""Pytest configuration and fixtures for the test suite.

This module configures VCR.py for cassette-based integration testing,
with automatic sanitization of sensitive data like OAuth tokens.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Ensure scripts path is in sys.path
scripts_dir = Path(__file__).parent.parent / "scripts"
if str(scripts_dir) not in sys.path:
    sys.path.append(str(scripts_dir))

import pytest  # noqa: E402

# Cassettes directory
CASSETTES_DIR = Path(__file__).parent / "cassettes"


@pytest.fixture(scope="function")
def vcr_config() -> dict[str, Any]:
    """Configure VCR for pytest-recording.

    Returns:
        VCR configuration dictionary with sanitization filters.
    """
    return {
        "cassette_library_dir": str(CASSETTES_DIR),
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "filter_headers": [
            ("authorization", "<ACCESS_TOKEN>"),
            ("Authorization", "<ACCESS_TOKEN>"),
            ("x-goog-api-key", "<API_KEY>"),
        ],
        "filter_post_data_parameters": [
            ("client_secret", "<CLIENT_SECRET>"),
            ("refresh_token", "<REFRESH_TOKEN>"),
            ("access_token", "<ACCESS_TOKEN>"),
        ],
        "filter_query_parameters": [
            ("key", "<API_KEY>"),
        ],
        "decode_compressed_response": True,
        "before_record_response": _sanitize_response,
    }


def _sanitize_response(response: dict[str, Any]) -> dict[str, Any]:
    """Sanitize sensitive data from recorded responses.

    Args:
        response: The HTTP response dictionary from VCR.

    Returns:
        Sanitized response with sensitive fields replaced.
    """
    # Sanitize common sensitive fields in response body
    body = response.get("body", {})
    if isinstance(body, dict):
        string_body = body.get("string", b"")
        if isinstance(string_body, bytes):
            try:
                decoded = string_body.decode("utf-8")
                # Replace common sensitive patterns
                # Email addresses
                import re

                decoded = re.sub(
                    r'"email"\s*:\s*"[^"]*@[^"]*"',
                    '"email": "<REDACTED_EMAIL>"',
                    decoded,
                )
                # Access tokens in response
                decoded = re.sub(
                    r'"access_token"\s*:\s*"[^"]*"',
                    '"access_token": "<ACCESS_TOKEN>"',
                    decoded,
                )
                decoded = re.sub(
                    r'"refresh_token"\s*:\s*"[^"]*"',
                    '"refresh_token": "<REFRESH_TOKEN>"',
                    decoded,
                )
                body["string"] = decoded.encode("utf-8")
            except (UnicodeDecodeError, AttributeError):
                pass  # Leave binary data as-is

    return response


@pytest.fixture(scope="session", autouse=True)
def ensure_cassettes_dir() -> None:
    """Ensure the cassettes directory exists."""
    CASSETTES_DIR.mkdir(exist_ok=True)
