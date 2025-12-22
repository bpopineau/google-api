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


def raise_for_http_error(http_error: Exception, *, context: str | None = None) -> None:
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

    prefix = f"{context}: " if context else ""

    if status == 400:
        raise InvalidRequestError(f"{prefix}Bad request: {reason}") from http_error
    if status in (401, 403):
        hint = (
            "Check that your token has the required scopes and that the resource is shared with the authorized account. "
            "Ensure the relevant API (e.g., Calendar, Tasks) is enabled in the Google Cloud Console. "
            "If you changed scopes recently, delete token.json and rerun scripts/oauth_setup.py."
        )
        raise AuthError(
            f"{prefix}Auth failed ({status}): {reason}. {hint}"
        ) from http_error
    if status == 404:
        raise NotFoundError(f"{prefix}Not found: {reason}") from http_error
    if status == 429:
        hint = "Rate limited/quota exceeded. Try again later or reduce request rate (batch reads/writes where possible)."
        raise QuotaExceededError(
            f"{prefix}Rate limited: {reason}. {hint}"
        ) from http_error

    # Re-raise as generic wrapper for other codes
    raise GoogleApiError(f"{prefix}HTTP {status}: {reason}") from http_error

