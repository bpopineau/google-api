"""Library-specific exceptions with actionable messages."""

from __future__ import annotations


class GoogleApiError(Exception):
    """Base exception for mygooglib errors."""

    pass


class AuthError(GoogleApiError):
    """Authentication or authorization failed (401/403)."""

    pass


class NotFoundError(GoogleApiError):
    """Requested resource does not exist (404)."""

    pass


class QuotaExceededError(GoogleApiError):
    """API quota or rate limit exceeded (429)."""

    pass


class InvalidRequestError(GoogleApiError):
    """Request was malformed or invalid (400)."""

    pass


def raise_for_http_error(http_error: Exception) -> None:
    """Convert googleapiclient.errors.HttpError to a library exception.

    Usage:
        try:
            result = service.files().get(...).execute()
        except HttpError as e:
            raise_for_http_error(e)
    """
    # Lazy import to avoid hard dependency at module load
    from googleapiclient.errors import HttpError

    if not isinstance(http_error, HttpError):
        raise http_error

    status = http_error.resp.status
    reason = (
        http_error._get_reason()
        if hasattr(http_error, "_get_reason")
        else str(http_error)
    )

    if status == 400:
        raise InvalidRequestError(f"Bad request: {reason}") from http_error
    if status in (401, 403):
        raise AuthError(f"Auth failed ({status}): {reason}") from http_error
    if status == 404:
        raise NotFoundError(f"Not found: {reason}") from http_error
    if status == 429:
        raise QuotaExceededError(f"Rate limited: {reason}") from http_error

    # Re-raise as generic wrapper for other codes
    raise GoogleApiError(f"HTTP {status}: {reason}") from http_error
