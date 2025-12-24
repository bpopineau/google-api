"""Contract tests for TypedDict schemas.

These tests verify that our TypedDict definitions correctly describe
the fields present in actual Google API responses.
"""

from __future__ import annotations

from typing import Any, get_type_hints


def get_typeddict_keys(typed_dict_class: type) -> set[str]:
    """Extract declared keys from a TypedDict class."""
    hints = get_type_hints(typed_dict_class)
    return set(hints.keys())


def assert_keys_exist(data: dict[str, Any], typed_dict_class: type) -> None:
    """Assert that the keys we declared exist in the real API response.

    Note: We don't check that API returns ONLY our keys (pragmatic subset allows extras).
    We just check that the keys we declared actually exist.
    """
    declared_keys = get_typeddict_keys(typed_dict_class)
    actual_keys = set(data.keys())
    declared_keys_in_response = declared_keys & actual_keys

    # For pragmatic subset, most declared keys should be present
    # (some may be optional and omitted by API)
    # We use a threshold-based check
    if len(declared_keys) > 0:
        coverage = len(declared_keys_in_response) / len(declared_keys)
        # At least 50% of our declared keys should be present
        # (optional fields may be missing from any given response)
        assert coverage >= 0.5, (
            f"Too few declared keys present in response. "
            f"Expected at least 50% of {declared_keys}, got {declared_keys_in_response}"
        )


class TestCalendarTypeDictContracts:
    """Contract tests for Calendar API TypedDicts."""

    def test_calendar_event_keys_exist(self) -> None:
        """Verify CalendarEventDict matches actual API response structure."""
        from mygooglib.core.types import CalendarEventDict

        # Sample API response structure (from Google Calendar API docs)
        sample_event: dict[str, Any] = {
            "id": "abc123",
            "summary": "Team Meeting",
            "start": {"dateTime": "2024-01-15T10:00:00-08:00"},
            "end": {"dateTime": "2024-01-15T11:00:00-08:00"},
            "status": "confirmed",
            "htmlLink": "https://calendar.google.com/...",
            "created": "2024-01-01T00:00:00.000Z",
            "updated": "2024-01-14T00:00:00.000Z",
            "description": "Weekly standup",
            "location": "Conference Room A",
            "creator": {"email": "user@example.com"},
            "organizer": {"email": "user@example.com"},
        }

        assert_keys_exist(sample_event, CalendarEventDict)

    def test_calendar_list_entry_keys_exist(self) -> None:
        """Verify CalendarListEntryDict matches actual API response structure."""
        from mygooglib.core.types import CalendarListEntryDict

        # Sample API response structure
        sample_calendar: dict[str, Any] = {
            "id": "primary",
            "summary": "My Calendar",
            "timeZone": "America/Los_Angeles",
            "accessRole": "owner",
        }

        assert_keys_exist(sample_calendar, CalendarListEntryDict)


class TestTasksTypeDictContracts:
    """Contract tests for Tasks API TypedDicts."""

    def test_task_keys_exist(self) -> None:
        """Verify TaskDict matches actual API response structure."""
        from mygooglib.core.types import TaskDict

        sample_task: dict[str, Any] = {
            "id": "task123",
            "title": "Complete project",
            "status": "needsAction",
            "due": "2024-01-20T00:00:00.000Z",
            "notes": "Important deadline",
        }

        assert_keys_exist(sample_task, TaskDict)

    def test_task_list_keys_exist(self) -> None:
        """Verify TaskListDict matches actual API response structure."""
        from mygooglib.core.types import TaskListDict

        sample_tasklist: dict[str, Any] = {
            "id": "list123",
            "title": "Work Tasks",
        }

        assert_keys_exist(sample_tasklist, TaskListDict)


class TestContactsTypeDictContracts:
    """Contract tests for People/Contacts API TypedDicts."""

    def test_contact_keys_exist(self) -> None:
        """Verify ContactDict matches actual flattened contact structure."""
        from mygooglib.core.types import ContactDict

        # Sample flattened contact (as returned by _flatten_person)
        sample_contact: dict[str, Any] = {
            "resourceName": "people/c123456789",
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "etag": "%EgUBBwg...",
        }

        assert_keys_exist(sample_contact, ContactDict)


class TestDocsTypeDictContracts:
    """Contract tests for Docs API TypedDicts."""

    def test_document_keys_exist(self) -> None:
        """Verify DocumentDict matches actual API response structure."""
        from mygooglib.core.types import DocumentDict

        sample_document: dict[str, Any] = {
            "documentId": "doc123abc",
            "title": "My Document",
            "body": {"content": []},
            "revisionId": "abc123",
        }

        assert_keys_exist(sample_document, DocumentDict)
