"""
Google Calendar API wrapper.

Provides a Pythonic interface for calendar event management.
"""

from datetime import date, datetime, timedelta, timezone
from typing import Any

from goog.auth import GoogleAuth
from goog.utils import logger, with_retry


class CalendarClient:
    """
    Pythonic wrapper for Google Calendar API.

    Provides intuitive methods for calendar operations:
    - Add, update, and delete events
    - List events in a time range
    - Handle datetime and timezone conversion

    Example:
        >>> from goog import GoogleAuth, CalendarClient
        >>> from datetime import datetime
        >>> auth = GoogleAuth()
        >>> calendar = CalendarClient(auth)
        >>> calendar.add_event(
        ...     summary="Meeting",
        ...     start=datetime(2024, 1, 15, 10, 0),
        ...     duration_minutes=60
        ... )
    """

    def __init__(self, auth: GoogleAuth, default_timezone: str = "UTC"):
        """
        Initialize the Calendar client.

        Args:
            auth: GoogleAuth instance for authentication.
            default_timezone: Default timezone for events without tzinfo.
        """
        self._auth = auth
        self._service = None
        self.default_timezone = default_timezone

    @property
    def service(self):
        """Lazily initialize and return the Calendar service."""
        if self._service is None:
            self._service = self._auth.build_service("calendar", "v3")
        return self._service

    def _format_datetime(self, dt: datetime | date) -> dict[str, str]:
        """
        Format a datetime for the Calendar API.

        Returns a dict with either 'dateTime' or 'date' key.
        """
        if isinstance(dt, datetime):
            # If no timezone, assume default
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return {
                "dateTime": dt.isoformat(),
                "timeZone": self.default_timezone,
            }
        else:
            # All-day event (date only)
            return {"date": dt.isoformat()}

    @with_retry()
    def add_event(
        self,
        summary: str,
        start: datetime | date,
        end: datetime | date | None = None,
        duration_minutes: int | None = None,
        calendar_id: str = "primary",
        description: str | None = None,
        location: str | None = None,
        attendees: list[str] | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Create a calendar event.

        Args:
            summary: Event title.
            start: Start datetime or date (for all-day events).
            end: End datetime/date. If not provided, uses duration_minutes.
            duration_minutes: Duration in minutes. Default 60 if end not provided.
            calendar_id: Calendar ID. Default "primary".
            description: Optional event description.
            location: Optional event location.
            attendees: Optional list of attendee email addresses.
            **kwargs: Additional event properties passed to the API.

        Returns:
            The event ID.

        Example:
            >>> event_id = calendar.add_event(
            ...     summary="Team Meeting",
            ...     start=datetime(2024, 1, 15, 14, 0),
            ...     duration_minutes=30,
            ...     location="Conference Room A"
            ... )
        """
        # Calculate end time if not provided
        if end is None:
            if isinstance(start, datetime):
                duration = duration_minutes or 60
                end = start + timedelta(minutes=duration)
            else:
                # All-day event defaults to same day
                end = start

        event_body = {
            "summary": summary,
            "start": self._format_datetime(start),
            "end": self._format_datetime(end),
        }

        if description:
            event_body["description"] = description
        if location:
            event_body["location"] = location
        if attendees:
            event_body["attendees"] = [{"email": email} for email in attendees]

        # Add any extra kwargs
        event_body.update(kwargs)

        logger.info(f"Creating event: {summary}")
        result = (
            self.service.events()
            .insert(calendarId=calendar_id, body=event_body)
            .execute()
        )

        event_id = result.get("id")
        logger.debug(f"Created event with ID: {event_id}")
        return event_id

    @with_retry()
    def list_events(
        self,
        calendar_id: str = "primary",
        time_min: datetime | None = None,
        time_max: datetime | None = None,
        max_results: int = 100,
        single_events: bool = True,
        order_by: str = "startTime",
    ) -> list[dict]:
        """
        List calendar events.

        Args:
            calendar_id: Calendar ID. Default "primary".
            time_min: Start of time range (default: now).
            time_max: End of time range (default: no limit).
            max_results: Maximum events to return.
            single_events: Expand recurring events into instances.
            order_by: Sort order - "startTime" or "updated".

        Returns:
            List of event dictionaries.

        Example:
            >>> from datetime import datetime, timedelta
            >>> now = datetime.now()
            >>> events = calendar.list_events(
            ...     time_min=now,
            ...     time_max=now + timedelta(days=7)
            ... )
            >>> for event in events:
            ...     print(event['summary'], event['start'])
        """
        # Default time_min to now
        if time_min is None:
            time_min = datetime.now(timezone.utc)
        elif time_min.tzinfo is None:
            time_min = time_min.replace(tzinfo=timezone.utc)

        params = {
            "calendarId": calendar_id,
            "timeMin": time_min.isoformat(),
            "maxResults": max_results,
            "singleEvents": single_events,
            "orderBy": order_by,
        }

        if time_max:
            if time_max.tzinfo is None:
                time_max = time_max.replace(tzinfo=timezone.utc)
            params["timeMax"] = time_max.isoformat()

        logger.debug(f"Listing events from {time_min}")
        result = self.service.events().list(**params).execute()

        events = result.get("items", [])
        logger.info(f"Found {len(events)} events")
        return events

    @with_retry()
    def get_event(self, event_id: str, calendar_id: str = "primary") -> dict:
        """
        Get a single event by ID.

        Args:
            event_id: The event ID.
            calendar_id: Calendar ID. Default "primary".

        Returns:
            Event dictionary.
        """
        return (
            self.service.events()
            .get(calendarId=calendar_id, eventId=event_id)
            .execute()
        )

    @with_retry()
    def update_event(
        self,
        event_id: str,
        calendar_id: str = "primary",
        **updates: Any,
    ) -> dict:
        """
        Update an existing event.

        Args:
            event_id: The event ID to update.
            calendar_id: Calendar ID. Default "primary".
            **updates: Event fields to update.

        Returns:
            Updated event dictionary.

        Example:
            >>> calendar.update_event(
            ...     event_id="abc123",
            ...     summary="Updated Title",
            ...     location="New Location"
            ... )
        """
        # Get current event
        event = self.get_event(event_id, calendar_id)

        # Apply updates
        for key, value in updates.items():
            if key in ("start", "end") and isinstance(value, (datetime, date)):
                event[key] = self._format_datetime(value)
            else:
                event[key] = value

        logger.info(f"Updating event: {event_id}")
        return (
            self.service.events()
            .update(calendarId=calendar_id, eventId=event_id, body=event)
            .execute()
        )

    @with_retry()
    def delete_event(self, event_id: str, calendar_id: str = "primary") -> None:
        """
        Delete an event.

        Args:
            event_id: The event ID to delete.
            calendar_id: Calendar ID. Default "primary".

        Example:
            >>> calendar.delete_event("abc123")
        """
        logger.info(f"Deleting event: {event_id}")
        self.service.events().delete(
            calendarId=calendar_id,
            eventId=event_id,
        ).execute()

    @with_retry()
    def list_calendars(self) -> list[dict]:
        """
        List all calendars the user has access to.

        Returns:
            List of calendar dictionaries with id, summary, etc.

        Example:
            >>> calendars = calendar.list_calendars()
            >>> for cal in calendars:
            ...     print(cal['summary'], cal['id'])
        """
        result = self.service.calendarList().list().execute()
        calendars = result.get("items", [])
        logger.info(f"Found {len(calendars)} calendars")
        return calendars

    @with_retry()
    def quick_add(
        self,
        text: str,
        calendar_id: str = "primary",
    ) -> str:
        """
        Create an event using natural language.

        Args:
            text: Natural language event description.
            calendar_id: Calendar ID. Default "primary".

        Returns:
            The event ID.

        Example:
            >>> calendar.quick_add("Meeting tomorrow at 3pm")
        """
        logger.info(f"Quick adding event: {text}")
        result = (
            self.service.events().quickAdd(calendarId=calendar_id, text=text).execute()
        )
        event_id = result.get("id")
        logger.debug(f"Created event with ID: {event_id}")
        return event_id
