"""Generic pagination helper for Google API list operations.

Google APIs typically return paginated responses with a `nextPageToken`.
This module provides a reusable helper to handle that pattern.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from mygooglib.core.utils.retry import execute_with_retry_http_error


def paginate(
    make_request: Callable[[str | None], Any],
    *,
    max_results: int | None = None,
    items_key: str = "items",
    progress_callback: Callable[[int], None] | None = None,
) -> list[dict]:
    """Execute paginated API requests and collect all results.

    Args:
        make_request: Callable that takes page_token (str|None) and returns
            an API request object (not yet executed).
        max_results: Maximum total items to retrieve (None = no limit).
        items_key: Key in response dict containing items (default "items").
        progress_callback: Optional callback(batch_count) called after each page.

    Returns:
        List of all items across all pages (up to max_results).

    Example:
        def make_req(token):
            return drive.files().list(pageToken=token, pageSize=100)

        files = paginate(make_req, max_results=500)
    """
    all_items: list[dict] = []
    page_token: str | None = None

    while True:
        request = make_request(page_token)
        response = execute_with_retry_http_error(request, is_write=False)

        items = response.get(items_key, [])
        all_items.extend(items)

        if progress_callback:
            progress_callback(len(items))

        page_token = response.get("nextPageToken")

        # Stop if no more pages or we've hit the limit
        if not page_token or (max_results and len(all_items) >= max_results):
            break

    # Trim to max_results if we exceeded
    if max_results and len(all_items) > max_results:
        all_items = all_items[:max_results]

    return all_items
