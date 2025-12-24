"""Datetime helpers for Calendar/Tasks RFC3339 formatting."""

from __future__ import annotations

import datetime as dt
import os
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# Default timezone for naive datetimes.
#
# On some Windows installs, IANA timezone data isn't available unless the
# optional `tzdata` package is installed. We fall back to UTC rather than
# failing at import time.
_DEFAULT_TZ_KEY = os.environ.get("MYGOOGLIB_DEFAULT_TZ", "America/New_York")
DEFAULT_TZ: ZoneInfo | dt.timezone
try:
    DEFAULT_TZ = ZoneInfo(_DEFAULT_TZ_KEY)
except ZoneInfoNotFoundError:
    import warnings

    warnings.warn(
        f"Timezone '{_DEFAULT_TZ_KEY}' not found. Falling back to UTC. "
        "Install 'tzdata' package for proper timezone support.",
        UserWarning,
        stacklevel=2,
    )
    DEFAULT_TZ = dt.timezone.utc


def to_rfc3339(value: dt.datetime | dt.date) -> str:
    """Convert a Python date or datetime to RFC3339 string for Google APIs.

    - date -> 'YYYY-MM-DD' (all-day event format)
    - naive datetime -> localized to DEFAULT_TZ then formatted
    - aware datetime -> formatted as-is

    Examples:
        >>> to_rfc3339(dt.date(2024, 1, 15))
        '2024-01-15'
        >>> to_rfc3339(dt.datetime(2024, 1, 15, 10, 30, tzinfo=dt.timezone.utc))
        '2024-01-15T10:30:00+00:00'
    """
    if isinstance(value, dt.datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=DEFAULT_TZ)
        return value.isoformat()
    # date only (all-day)
    return value.isoformat()


def from_rfc3339(value: str) -> dt.datetime | dt.date:
    """Parse an RFC3339 string back to datetime or date.

    Examples:
        >>> from_rfc3339('2024-01-15')
        datetime.date(2024, 1, 15)
        >>> from_rfc3339('2024-01-15T10:30:00+00:00')
        datetime.datetime(2024, 1, 15, 10, 30, tzinfo=datetime.timezone.utc)
    """
    # All-day events come as 'YYYY-MM-DD'
    if len(value) == 10:
        return dt.date.fromisoformat(value)
    return dt.datetime.fromisoformat(value)
