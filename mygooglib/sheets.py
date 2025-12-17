"""Google Sheets wrapper — get_range, update_range, append_row.

These helpers take the raw Sheets v4 Resource from `get_clients().sheets`.
They return plain Python types by default, with a `raw=True` escape hatch.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any

from googleapiclient.errors import HttpError

from mygooglib.exceptions import raise_for_http_error
from mygooglib.utils.retry import execute_with_retry_http_error

GOOGLE_SHEET_MIME = "application/vnd.google-apps.spreadsheet"


_SHEETS_URL_RE = re.compile(r"/spreadsheets/d/([a-zA-Z0-9-_]+)")


def resolve_spreadsheet(
    drive: Any,
    identifier: str,
    *,
    parent_id: str | None = None,
    allow_multiple: bool = False,
) -> str:
    """Resolve a spreadsheet identifier (ID, title, or URL) to an ID.

    Accepted identifier forms:
    - Spreadsheet ID (the long token)
    - Full Sheets URL containing `/spreadsheets/d/<id>`
    - Title (exact match), resolved via Drive search

    Args:
        drive: Drive API Resource from get_clients().drive
        identifier: ID, URL, or title
        parent_id: Optional Drive folder ID to scope title-based search
        allow_multiple: Only applies to title-based search

    Returns:
        Spreadsheet ID.
    """
    identifier = identifier.strip()
    if not identifier:
        raise ValueError("identifier must be a non-empty string")

    match = _SHEETS_URL_RE.search(identifier)
    if match:
        return match.group(1)

    # Heuristic: Drive/Sheets IDs are URL-safe base64-ish and typically long.
    if re.fullmatch(r"[a-zA-Z0-9-_]{20,}", identifier):
        return identifier

    return open_by_title(
        drive,
        identifier,
        parent_id=parent_id,
        allow_multiple=allow_multiple,
    )


def open_by_id(spreadsheet_id: str) -> str:
    """Return a spreadsheet ID unchanged.

    This exists mostly for symmetry with `open_by_title` and to make calling
    code read clearly.
    """
    return spreadsheet_id


def open_by_title(
    drive: Any,
    title: str,
    *,
    parent_id: str | None = None,
    allow_multiple: bool = False,
) -> str:
    """Find a Google Sheet by title using the Drive API.

    Sheets API does not provide a "search by title" endpoint; Drive does.

    Args:
        drive: Drive API Resource from get_clients().drive
        title: Exact spreadsheet title to match
        parent_id: Optional Drive folder ID to scope the search
        allow_multiple: If False (default), raise if multiple matches are found

    Returns:
        The spreadsheet ID.

    Raises:
        ValueError: if no matches are found, or multiple matches and allow_multiple=False
    """
    from mygooglib.drive import list_files

    # Escape single quotes in Drive query
    escaped = title.replace("'", "\\'")
    results = list_files(
        drive,
        query=f"name = '{escaped}'",
        parent_id=parent_id,
        mime_type=GOOGLE_SHEET_MIME,
        trashed=False,
        fields="id, name, parents",
    )

    if not results:
        scope = f" under parent {parent_id}" if parent_id else ""
        raise ValueError(f"No spreadsheet found with title '{title}'{scope}.")

    if len(results) > 1 and not allow_multiple:
        ids = [r.get("id") for r in results]
        raise ValueError(
            f"Multiple spreadsheets found with title '{title}'. "
            f"Pass parent_id to disambiguate, or allow_multiple=True. Matches: {ids}"
        )

    return results[0]["id"]


def _quote_sheet_name(sheet_name: str) -> str:
    # A1 requires single quotes when name contains spaces/special chars.
    # Embedded single quotes must be escaped by doubling.
    if re.search(r"[\s']", sheet_name):
        safe = sheet_name.replace("'", "''")
        return f"'{safe}'"
    return sheet_name


def get_range(
    sheets: Any,
    spreadsheet_id: str,
    a1_range: str,
    *,
    drive: Any | None = None,
    parent_id: str | None = None,
    allow_multiple: bool = False,
    major_dimension: str | None = None,
    value_render_option: str | None = None,
    date_time_render_option: str | None = None,
    raw: bool = False,
) -> list[list[Any]] | dict:
    """Read a range of values from a spreadsheet.

    Args:
            sheets: Sheets API Resource from get_clients().sheets
            spreadsheet_id: Spreadsheet ID, title, or full Sheets URL
            drive: Drive API Resource (required if spreadsheet_id is a title)
            parent_id: Optional Drive folder ID to scope title-based search
            allow_multiple: Allow multiple title matches (returns first)
            a1_range: A1 range string, e.g. "Sheet1!A1:C10"
            major_dimension: "ROWS" or "COLUMNS" (optional)
            value_render_option: "FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"
            date_time_render_option: "SERIAL_NUMBER" or "FORMATTED_STRING"
            raw: If True, return the full API response dict

    Returns:
            By default, list-of-lists of values (missing/empty returns []).
            If raw=True, the full API response dict.
    """
    spreadsheet_real_id = (
        resolve_spreadsheet(
            drive,
            spreadsheet_id,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
        )
        if drive is not None
        else spreadsheet_id
    )

    # If it doesn't look like an ID/URL and no drive was supplied, guide the caller.
    if (
        drive is None
        and not _SHEETS_URL_RE.search(spreadsheet_id)
        and not re.fullmatch(r"[a-zA-Z0-9-_]{20,}", spreadsheet_id.strip())
    ):
        raise ValueError(
            "Spreadsheet identifier looks like a title; pass drive=clients.drive or call resolve_spreadsheet() first."
        )

    try:
        request = (
            sheets.spreadsheets()
            .values()
            .get(
                spreadsheetId=spreadsheet_real_id,
                range=a1_range,
                majorDimension=major_dimension,
                valueRenderOption=value_render_option,
                dateTimeRenderOption=date_time_render_option,
            )
        )
        response = execute_with_retry_http_error(request, is_write=False)
    except HttpError as e:
        raise_for_http_error(e, context="Sheets get_range")
        raise

    return response if raw else response.get("values", [])


def update_range(
    sheets: Any,
    spreadsheet_id: str,
    a1_range: str,
    values: Sequence[Sequence[Any]],
    *,
    drive: Any | None = None,
    parent_id: str | None = None,
    allow_multiple: bool = False,
    value_input_option: str = "RAW",
    include_values_in_response: bool = False,
    response_value_render_option: str | None = None,
    response_date_time_render_option: str | None = None,
    raw: bool = False,
) -> dict | None:
    """Update a range of values in a spreadsheet.

    Args:
            sheets: Sheets API Resource
            spreadsheet_id: Spreadsheet ID, title, or full Sheets URL
            drive: Drive API Resource (required if spreadsheet_id is a title)
            parent_id: Optional Drive folder ID to scope title-based search
            allow_multiple: Allow multiple title matches (returns first)
            a1_range: A1 range string to update
            values: 2D list-of-lists (rows) to write
            value_input_option: "RAW" (default) or "USER_ENTERED"
            include_values_in_response: If True, response includes written values
            response_value_render_option: Optional render option for returned values
            response_date_time_render_option: Optional datetime render option
            raw: If True, return the full API response dict

    Returns:
            Small summary dict by default, or full response if raw=True.
            Returns None if the API returns an empty response.
    """
    spreadsheet_real_id = (
        resolve_spreadsheet(
            drive,
            spreadsheet_id,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
        )
        if drive is not None
        else spreadsheet_id
    )

    if (
        drive is None
        and not _SHEETS_URL_RE.search(spreadsheet_id)
        and not re.fullmatch(r"[a-zA-Z0-9-_]{20,}", spreadsheet_id.strip())
    ):
        raise ValueError(
            "Spreadsheet identifier looks like a title; pass drive=clients.drive or call resolve_spreadsheet() first."
        )

    body = {"values": [list(row) for row in values]}
    try:
        request = (
            sheets.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_real_id,
                range=a1_range,
                valueInputOption=value_input_option,
                includeValuesInResponse=include_values_in_response,
                responseValueRenderOption=response_value_render_option,
                responseDateTimeRenderOption=response_date_time_render_option,
                body=body,
            )
        )
        response = execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Sheets update_range")
        raise

    if raw:
        return response
    if not response:
        return None
    return {
        "updatedRange": response.get("updatedRange"),
        "updatedRows": response.get("updatedRows"),
        "updatedColumns": response.get("updatedColumns"),
        "updatedCells": response.get("updatedCells"),
    }


def append_row(
    sheets: Any,
    spreadsheet_id: str,
    sheet_name: str,
    values: Sequence[Any],
    *,
    drive: Any | None = None,
    parent_id: str | None = None,
    allow_multiple: bool = False,
    value_input_option: str = "RAW",
    insert_data_option: str | None = None,
    include_values_in_response: bool = False,
    raw: bool = False,
) -> dict | None:
    """Append a single row to the end of a sheet.

    Args:
            sheets: Sheets API Resource
            spreadsheet_id: Spreadsheet ID, title, or full Sheets URL
            drive: Drive API Resource (required if spreadsheet_id is a title)
            parent_id: Optional Drive folder ID to scope title-based search
            allow_multiple: Allow multiple title matches (returns first)
            sheet_name: Tab name (not an A1 range)
            values: 1D row values
            value_input_option: "RAW" (default) or "USER_ENTERED"
            insert_data_option: "INSERT_ROWS" or "OVERWRITE" (optional)
            include_values_in_response: If True, response includes written values
            raw: If True, return full API response

    Returns:
            Small summary dict by default, or full response if raw=True.
    """
    spreadsheet_real_id = (
        resolve_spreadsheet(
            drive,
            spreadsheet_id,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
        )
        if drive is not None
        else spreadsheet_id
    )

    if (
        drive is None
        and not _SHEETS_URL_RE.search(spreadsheet_id)
        and not re.fullmatch(r"[a-zA-Z0-9-_]{20,}", spreadsheet_id.strip())
    ):
        raise ValueError(
            "Spreadsheet identifier looks like a title; pass drive=clients.drive or call resolve_spreadsheet() first."
        )

    # Use column A as the table anchor range for appends.
    safe_sheet = _quote_sheet_name(sheet_name)
    append_range = f"{safe_sheet}!A:A"
    body = {"values": [list(values)]}

    try:
        request = (
            sheets.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_real_id,
                range=append_range,
                valueInputOption=value_input_option,
                insertDataOption=insert_data_option,
                includeValuesInResponse=include_values_in_response,
                body=body,
            )
        )
        response = execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Sheets append_row")
        raise

    if raw:
        return response
    if not response:
        return None

    updates = response.get("updates") or {}
    return {
        "updatedRange": updates.get("updatedRange"),
        "updatedRows": updates.get("updatedRows"),
        "updatedColumns": updates.get("updatedColumns"),
        "updatedCells": updates.get("updatedCells"),
    }
