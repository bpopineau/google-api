"""VCR Integration Tests - Demonstrates cassette recording and replay.

These tests are designed to make REAL network calls when recording cassettes,
and replay from cassettes when in 'none' mode.
"""

from __future__ import annotations

import pytest


@pytest.mark.vcr
def test_vcr_google_discovery_api() -> None:
    """Test that we can record/replay a simple Google API discovery call.

    This test hits the public Google Discovery API to verify VCR is working.
    No authentication required for this endpoint.
    """
    import json
    import urllib.request

    # Google's public discovery endpoint - no auth needed
    url = "https://www.googleapis.com/discovery/v1/apis?preferred=true"

    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    # Verify we got a valid response
    assert "items" in data
    assert "kind" in data
    assert data["kind"] == "discovery#directoryList"
    # Should have multiple Google APIs listed
    assert len(data["items"]) > 10
