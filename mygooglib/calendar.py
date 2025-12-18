"""Google Calendar wrapper — add_event, list_events.

These helpers take the raw Calendar v3 Resource from `get_clients().calendar`.
They return plain Python types by default, with a `raw=True` escape hatch.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

from googleapiclient.errors import HttpError

from mygooglib.exceptions import raise_for_http_error
from mygooglib.utils.datetime import to_rfc3339
from mygooglib.utils.retry import execute_with_retry_http_error


def add_event(
    calendar: Any,
    *,
    summary: str,
    start: dt.datetime | dt.date,
    end: dt.datetime | dt.date | None = None,
    duration_minutes: int | None = None,
    description: str | None = None,
    location: str | None = None,
    calendar_id: str = "primary",
    raw: bool = False,
) -> str | dict:
    """Add an event to a Google Calendar.

    Args:
        calendar: Calendar API Resource from get_clients().calendar
        summary: Event title
        start: Start datetime or date (for all-day)
        end: End datetime or date. If None, calculated from duration or set to start + 1h.
        duration_minutes: Optional duration if end is not provided.
        description: Optional event description
        location: Optional location string
        calendar_id: Calendar ID (default "primary")
        raw: If True, return full API response dict

    Returns:
        Event ID string by default, or full response if raw=True.
    """
    is_all_day = not isinstance(start, dt.datetime)

    if end is None:
        if duration_minutes is not None:
            if is_all_day:
                # For all-day, duration doesn't make much sense in minutes,
                # but we'll treat it as days if it's a multiple of 1440.
                days = max(1, duration_minutes // 1440)
                end = start + dt.timedelta(days=days)
            else:
                end = start + dt.timedelta(minutes=duration_minutes)
        else:
            # Default 1 hour or 1 day
            if is_all_day:
                end = start + dt.timedelta(days=1)
            else:
                end = start + dt.timedelta(hours=1)

    event: dict[str, Any] = {
        "summary": summary,
    }
    if description:
        event["description"] = description
    if location:
        event["location"] = location

    if is_all_day:
        event["start"] = {"date": to_rfc3339(start)}
        event["end"] = {"date": to_rfc3339(end)}
    else:
        event["start"] = {"dateTime": to_rfc3339(start)}
        event["end"] = {"dateTime": to_rfc3339(end)}

    try:
        request = calendar.events().insert(calendarId=calendar_id, body=event)
        response = execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Calendar add_event")
        raise

    return response if raw else response.get("id")


def list_events(
    calendar: Any,
    *,
    calendar_id: str = "primary",
    time_min: dt.datetime | None = None,
    time_max: dt.datetime | None = None,
    max_results: int = 100,
    raw: bool = False,
    progress_callback: Any | None = None,
) -> list[dict] | dict:
    """List events from a calendar.

    Args:
        calendar: Calendar API Resource
        calendar_id: Calendar ID (default "primary")
        time_min: Lower bound (inclusive) for an event's end time.
        time_max: Upper bound (exclusive) for an event's start time.
        max_results: Maximum number of events to return.
        raw: If True, return full API response dict.
        progress_callback: Optional callback(count) for progress tracking.

    Returns:
        List of event dicts by default, or full response if raw=True.
    """
    all_items = []
    page_token = None

    try:
        while True:
            request = calendar.events().list(
                calendarId=calendar_id,
                timeMin=to_rfc3339(time_min) if time_min else None,
                timeMax=to_rfc3339(time_max) if time_max else None,
                maxResults=min(max_results - len(all_items), 2500)
                if max_results
                else 2500,
                singleEvents=True,
                orderBy="startTime",
                pageToken=page_token,
            )
            response = execute_with_retry_http_error(request, is_write=False)
            items = response.get("items", [])
            all_items.extend(items)

            if progress_callback:
                progress_callback(len(items))

            page_token = response.get("nextPageToken")
            if not page_token or (max_results and len(all_items) >= max_results):
                break

    except HttpError as e:
        raise_for_http_error(e, context="Calendar list_events")
        raise

    if raw:
        return {"items": all_items}
    return all_items


def delete_event(
    calendar: Any,
    event_id: str,
    *,
    calendar_id: str = "primary",
) -> None:
    """Delete an event from a Google Calendar."""
    try:
        request = calendar.events().delete(calendarId=calendar_id, eventId=event_id)
        execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Calendar delete_event")
        raise


class CalendarClient:
    """Simplified Google Calendar API wrapper focusing on common operations."""

    def __init__(self, service: Any):
        """Initialize with an authorized Calendar API service object."""
        self.service = service

    def add_event(
        self,
        *,
        summary: str,
        start: dt.datetime | dt.date,
        end: dt.datetime | dt.date | None = None,
        duration_minutes: int | None = None,
        description: str | None = None,
        location: str | None = None,
        calendar_id: str = "primary",
        raw: bool = False,
    ) -> str | dict:
        """Add an event to a Google Calendar."""
        return add_event(
            self.service,
            summary=summary,
            start=start,
            end=end,
            duration_minutes=duration_minutes,
            description=description,
            location=location,
            calendar_id=calendar_id,
            raw=raw,
        )

    def list_events(
        self,
        *,
        calendar_id: str = "primary",
        time_min: dt.datetime | None = None,
        time_max: dt.datetime | None = None,
        max_results: int = 100,
        raw: bool = False,
        progress_callback: Any | None = None,
    ) -> list[dict] | dict:
        """List events from a calendar."""
        return list_events(
            self.service,
            calendar_id=calendar_id,
            time_min=time_min,
            time_max=time_max,
            max_results=max_results,
            raw=raw,
            progress_callback=progress_callback,
        )

    def delete_event(
        self,
        event_id: str,
        *,
        calendar_id: str = "primary",
    ) -> None:
        """Delete an event from a Google Calendar."""
        return delete_event(self.service, event_id, calendar_id=calendar_id)
