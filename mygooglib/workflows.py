"""High-level multi-service workflows."""

from __future__ import annotations

from typing import Any

from mygooglib.calendar import add_event
from mygooglib.sheets import get_range


def import_events_from_sheets(
    clients: Any,
    spreadsheet_id: str,
    range_name: str,
    *,
    calendar_id: str = "primary",
    dry_run: bool = False,
) -> dict:
    """Import calendar events from a Google Sheet.

    Expected columns: [Summary, Start, End/Duration, Description]
    - Start and End can be strings parsable by your lib or datetime/date.
    - Duration can be an integer (minutes).

    Returns:
        Summary dict: {created: int, skipped: int, errors: list[str]}
    """
    rows = get_range(clients.sheets.service, spreadsheet_id, range_name)
    if not rows:
        return {"created": 0, "skipped": 0, "errors": ["No data found in range"]}

    created = 0
    skipped = 0
    errors = []

    for i, row in enumerate(rows):
        if not row or not row[0]:  # Skip empty rows or rows without summary
            skipped += 1
            continue

        try:
            summary = row[0]
            start_str = row[1] if len(row) > 1 else None
            end_val = row[2] if len(row) > 2 else None
            description = row[3] if len(row) > 3 else None

            if not start_str:
                errors.append(f"Row {i + 1}: Missing start time")
                continue

            # Basic parsing if they are strings (mygooglib.calendar.add_event handles some or we can help)
            # Actually, let's keep it simple and assume the user provides parsable strings or datetimes.

            kwargs: dict[str, Any] = {
                "summary": summary,
                "start": start_str,  # add_event needs to be robust here or we parse
                "description": description,
                "calendar_id": calendar_id,
            }

            # If end_val is integer-like, treat as duration_minutes
            try:
                if end_val is not None:
                    duration = int(str(end_val))
                    kwargs["duration_minutes"] = duration
            except (ValueError, TypeError):
                if end_val:
                    kwargs["end"] = end_val

            if not dry_run:
                add_event(clients.calendar.service, **kwargs)

            created += 1
        except Exception as e:
            errors.append(f"Row {i + 1} ({row[0]}): {e}")

    return {"created": created, "skipped": skipped, "errors": errors}
