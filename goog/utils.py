"""
Utility functions and common exceptions for the goog library.
"""

import functools
import logging
import time
from typing import Callable, ParamSpec, TypeVar

from googleapiclient.errors import HttpError

# Type variables for decorator
P = ParamSpec("P")
T = TypeVar("T")

# Logger for the library
logger = logging.getLogger("goog")


# ============================================================================
# Custom Exceptions
# ============================================================================


class GoogleAPIError(Exception):
    """Base exception for all Google API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class NotFoundError(GoogleAPIError):
    """Resource not found (HTTP 404)."""

    pass


class PermissionDeniedError(GoogleAPIError):
    """Access denied (HTTP 403)."""

    pass


class QuotaExceededError(GoogleAPIError):
    """API quota exceeded (HTTP 429)."""

    pass


class AuthenticationError(GoogleAPIError):
    """Authentication failed (HTTP 401)."""

    pass


# ============================================================================
# Retry Decorator
# ============================================================================

# Status codes that should trigger a retry
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

# Maximum number of retry attempts
MAX_RETRIES = 3

# Base delay in seconds for exponential backoff
BASE_DELAY = 1.0


def with_retry(
    max_retries: int = MAX_RETRIES,
    retryable_codes: set[int] = RETRYABLE_STATUS_CODES,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator that retries a function on transient HTTP errors.

    Uses exponential backoff: delay = BASE_DELAY * (2 ** attempt)

    Args:
        max_retries: Maximum number of retry attempts.
        retryable_codes: Set of HTTP status codes that trigger retry.

    Returns:
        Decorated function with retry logic.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            last_exception: Exception | None = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except HttpError as e:
                    status_code = e.resp.status if hasattr(e, "resp") else None

                    if status_code not in retryable_codes or attempt >= max_retries:
                        # Convert to our custom exceptions
                        raise _convert_http_error(e) from e

                    last_exception = e
                    delay = BASE_DELAY * (2**attempt)
                    logger.warning(
                        f"Request failed with status {status_code}, "
                        f"retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})"
                    )
                    time.sleep(delay)

            # Should not reach here, but just in case
            if last_exception:
                raise _convert_http_error(last_exception) from last_exception
            raise GoogleAPIError("Unexpected error in retry logic")

        return wrapper

    return decorator


def _convert_http_error(error: HttpError) -> GoogleAPIError:
    """Convert HttpError to appropriate custom exception."""
    status_code = error.resp.status if hasattr(error, "resp") else None
    message = str(error)

    if status_code == 404:
        return NotFoundError(message, status_code)
    elif status_code == 403:
        return PermissionDeniedError(message, status_code)
    elif status_code == 429:
        return QuotaExceededError(message, status_code)
    elif status_code == 401:
        return AuthenticationError(message, status_code)
    else:
        return GoogleAPIError(message, status_code)


# ============================================================================
# Logging Setup
# ============================================================================


def setup_logging(
    level: str = "INFO",
    format_string: str | None = None,
) -> None:
    """
    Configure logging for the goog library.

    Args:
        level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
        format_string: Optional custom format string for log messages.
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(format_string))

    logger.setLevel(getattr(logging, level.upper()))
    logger.addHandler(handler)

    # Prevent duplicate logs if called multiple times
    logger.propagate = False
