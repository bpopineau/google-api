"""Retry helpers for transient Google API failures.

The google-api-python-client does not automatically retry failed requests.
For personal automation, a small amount of retry/backoff significantly reduces
flake from 429s and transient 5xx responses.

This module intentionally:
- Retries only well-known transient statuses by default
- Avoids logging sensitive request/response details
"""

from __future__ import annotations

import os
import random
import time
from collections.abc import Iterable
from typing import Any

from googleapiclient.errors import HttpError

from mygooglib.core.utils.logging import get_logger

_DEFAULT_RETRY_STATUSES: tuple[int, ...] = (429, 500, 502, 503, 504)


def _env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _parse_retry_after_seconds(e: HttpError) -> float | None:
    resp = getattr(e, "resp", None)
    if resp is None:
        return None
    getter = getattr(resp, "get", None)
    if not callable(getter):
        return None

    raw = getter("retry-after") or getter("Retry-After")
    if not raw:
        return None
    try:
        return float(str(raw))
    except (TypeError, ValueError):
        return None


def execute_with_retry_http_error(
    request: Any,
    *,
    is_write: bool = False,
    attempts: int | None = None,
    initial_backoff_s: float | None = None,
    max_backoff_s: float | None = None,
    retry_statuses: Iterable[int] = _DEFAULT_RETRY_STATUSES,
) -> Any:
    """Execute a request, retrying transient HttpError statuses.

    This inspects the HttpError itself to determine status.

    Safety note:
        By default, retries are enabled for read-only operations and disabled
        for writes, because retrying writes can cause duplicate side effects
        (e.g., sending an email twice or appending a row twice) if the server
        processed the request but the client timed out.

    WARNING:
        If you override 'attempts' for write operations (is_write=True), be aware
        that failed requests might have been processed by the server even if the
        client didn't receive a response. This can lead to duplicate operations:
        - Emails sent multiple times
        - Rows appended multiple times
        - Files uploaded multiple times
        Only increase write retries if your operation is truly idempotent.

    Args:
        request: The API request object to execute
        is_write: Whether this is a write operation (affects default retry behavior)
        attempts: Number of attempts (overrides env-based defaults)
        initial_backoff_s: Initial backoff time in seconds
        max_backoff_s: Maximum backoff time in seconds
        retry_statuses: HTTP status codes to retry (default: 429, 500, 502, 503, 504)

    Returns:
        The API response from request.execute()

    Raises:
        HttpError: If all retry attempts are exhausted or status is not retryable
    """

    retry_enabled = _env_bool("MYGOOGLIB_RETRY_ENABLED", True)

    attempts_read = _env_int("MYGOOGLIB_RETRY_ATTEMPTS_READ", 4)
    attempts_write = _env_int("MYGOOGLIB_RETRY_ATTEMPTS_WRITE", 1)

    initial_backoff_s = (
        initial_backoff_s
        if initial_backoff_s is not None
        else _env_float("MYGOOGLIB_RETRY_INITIAL_BACKOFF_S", 0.5)
    )
    max_backoff_s = (
        max_backoff_s
        if max_backoff_s is not None
        else _env_float("MYGOOGLIB_RETRY_MAX_BACKOFF_S", 8.0)
    )

    effective_attempts = attempts
    if effective_attempts is None:
        effective_attempts = attempts_write if is_write else attempts_read
    if not retry_enabled:
        effective_attempts = 1

    if effective_attempts < 1:
        raise ValueError("attempts must be >= 1")

    retry_set = set(int(s) for s in retry_statuses)

    logger = get_logger("mygooglib.retry")

    for attempt in range(1, effective_attempts + 1):
        try:
            return request.execute()
        except HttpError as e:
            status = int(getattr(getattr(e, "resp", None), "status", 0) or 0)
            if attempt >= effective_attempts or status not in retry_set:
                raise

            retry_after_s = _parse_retry_after_seconds(e)

            # Exponential backoff with a small jitter (or honor Retry-After when present).
            backoff = (
                retry_after_s
                if retry_after_s is not None
                else min(max_backoff_s, initial_backoff_s * (2 ** (attempt - 1)))
            )
            jitter = random.uniform(0.85, 1.15)

            sleep_s = max(0.0, backoff * jitter)
            logger.warning(
                "Retrying after HTTP %s (attempt %s/%s, write=%s, sleep=%.2fs)",
                status,
                attempt,
                effective_attempts,
                is_write,
                sleep_s,
            )
            time.sleep(sleep_s)

    # Unreachable
    raise AssertionError("execute_with_retry_http_error: fell through")


def api_call(context: str, *, is_write: bool = False):
    """Decorator that wraps API calls with retry and error handling.

    This decorator eliminates the try/except boilerplate pattern:

        try:
            request = service.method(...)
            response = execute_with_retry_http_error(request, is_write=False)
        except HttpError as e:
            raise_for_http_error(e, context="...")
            raise

    Usage:
        @api_call("Tasks list_tasklists", is_write=False)
        def list_tasklists(tasks, *, max_results=100):
            request = tasks.tasklists().list(maxResults=max_results)
            return execute_with_retry_http_error(request, is_write=False)

    Args:
        context: Context string for error messages (e.g., "Drive list_files")
        is_write: Whether this is a write operation (affects retry behavior)

    Returns:
        Decorated function with automatic error handling.
    """
    from functools import wraps

    from mygooglib.core.exceptions import raise_for_http_error

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HttpError as e:
                raise_for_http_error(e, context=context)
                raise  # Unreachable but satisfies type checker

        return wrapper

    return decorator

