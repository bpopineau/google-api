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
    """Quote a sheet name for use in A1 notation (internal helper).
    
    A1 notation requires single quotes when the sheet name contains spaces or special characters.
    Embedded single quotes must be escaped by doubling them.
    
    Args:
        sheet_name: The raw sheet name
        
    Returns:
        The properly quoted sheet name for A1 notation
        
    Examples:
        'Sheet1' -> 'Sheet1'
        'My Sheet' -> "'My Sheet'"
        "Bob's Sheet" -> "'Bob''s Sheet'"
    """
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
    chunk_size: int | None = None,
    progress_callback: Any | None = None,
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
            chunk_size: If set, read the range in chunks of this many rows/cols
            progress_callback: Optional callable(current_count, total_count)

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

    if not chunk_size:
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

    # Chunked reading logic
    # This is a simplified version that assumes a standard A1 range like "Sheet1!A1:C1000"
    # and only chunks along the major dimension (default ROWS).
    from mygooglib.utils.a1 import a1_to_range, range_to_a1

    sheet_name, start_row, start_col, end_row, end_col = a1_to_range(a1_range)

    # If end_row or end_col is None, we don't know the total size easily without fetching metadata.
    # For simplicity in v0.1, we'll only chunk if both are provided.
    if end_row is None or end_col is None:
        # Fallback to non-chunked
        return get_range(
            sheets,
            spreadsheet_real_id,
            a1_range,
            major_dimension=major_dimension,
            value_render_option=value_render_option,
            date_time_render_option=date_time_render_option,
            raw=raw,
        )

    all_values: list[list[Any]] = []

    is_rows = (major_dimension or "ROWS") == "ROWS"
    total = (end_row - start_row + 1) if is_rows else (end_col - start_col + 1)

    for i in range(0, total, chunk_size):
        if is_rows:
            c_start_row = start_row + i
            c_end_row = min(start_row + i + chunk_size - 1, end_row)
            c_start_col, c_end_col = start_col, end_col
        else:
            c_start_col = start_col + i
            c_end_col = min(start_col + i + chunk_size - 1, end_col)
            c_start_row, c_end_row = start_row, end_row

        chunk_a1 = range_to_a1(
            sheet_name, c_start_row, c_start_col, c_end_row, c_end_col
        )

        chunk_values = get_range(
            sheets,
            spreadsheet_real_id,
            chunk_a1,
            major_dimension=major_dimension,
            value_render_option=value_render_option,
            date_time_render_option=date_time_render_option,
        )

        if is_rows:
            all_values.extend(chunk_values)
        else:
            # If COLUMNS, we need to merge carefully if we want a single list-of-lists.
            # But usually get_range returns list of columns.
            all_values.extend(chunk_values)

        if progress_callback:
            progress_callback(len(all_values), total)

    return all_values


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


def get_sheets(
    sheets: Any,
    spreadsheet_id: str,
    *,
    drive: Any | None = None,
    parent_id: str | None = None,
    allow_multiple: bool = False,
    raw: bool = False,
) -> list[dict] | dict:
    """Get metadata for all sheets (tabs) in a spreadsheet.

    Args:
        sheets: Sheets API Resource
        spreadsheet_id: Spreadsheet ID, title, or URL
        drive: Drive API Resource (for title resolution)
        parent_id: Optional parent ID for title resolution
        allow_multiple: Allow multiple title matches
        raw: If True, return full API response

    Returns:
        List of sheet metadata dicts (title, id, index, type).
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

    try:
        request = sheets.spreadsheets().get(
            spreadsheetId=spreadsheet_real_id, fields="sheets(properties)"
        )
        response = execute_with_retry_http_error(request, is_write=False)
    except HttpError as e:
        raise_for_http_error(e, context="Sheets get_sheets")
        raise

    if raw:
        return response

    results = []
    for s in response.get("sheets", []):
        props = s.get("properties", {})
        results.append(
            {
                "title": props.get("title"),
                "id": props.get("sheetId"),
                "index": props.get("index"),
                "type": props.get("sheetType"),
            }
        )
    return results


class SheetsClient:
    """Simplified Google Sheets API wrapper focusing on common operations."""

    def __init__(self, service: Any, drive: Any | None = None):
        """Initialize with an authorized Sheets API service object.

        Args:
            service: Sheets API Resource from get_clients().sheets
            drive: Optional Drive API Resource for title-based resolution
        """
        self.service = service
        self.drive = drive

    def resolve_spreadsheet(
        self,
        identifier: str,
        *,
        parent_id: str | None = None,
        allow_multiple: bool = False,
    ) -> str:
        """Resolve a spreadsheet identifier (ID, title, or URL) to an ID."""
        return resolve_spreadsheet(
            self.drive,
            identifier,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
        )

    def open_by_title(
        self,
        title: str,
        *,
        parent_id: str | None = None,
        allow_multiple: bool = False,
    ) -> str:
        """Find a Google Sheet by title using the Drive API."""
        return open_by_title(
            self.drive,
            title,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
        )

    def get_range(
        self,
        spreadsheet_id: str,
        a1_range: str,
        *,
        parent_id: str | None = None,
        allow_multiple: bool = False,
        major_dimension: str | None = None,
        value_render_option: str | None = None,
        date_time_render_option: str | None = None,
        raw: bool = False,
        chunk_size: int | None = None,
        progress_callback: Any | None = None,
    ) -> list[list[Any]] | dict:
        """Read a range of values from a spreadsheet."""
        return get_range(
            self.service,
            spreadsheet_id,
            a1_range,
            drive=self.drive,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
            major_dimension=major_dimension,
            value_render_option=value_render_option,
            date_time_render_option=date_time_render_option,
            raw=raw,
            chunk_size=chunk_size,
            progress_callback=progress_callback,
        )

    def update_range(
        self,
        spreadsheet_id: str,
        a1_range: str,
        values: Sequence[Sequence[Any]],
        *,
        parent_id: str | None = None,
        allow_multiple: bool = False,
        value_input_option: str = "RAW",
        include_values_in_response: bool = False,
        response_value_render_option: str | None = None,
        response_date_time_render_option: str | None = None,
        raw: bool = False,
    ) -> dict | None:
        """Update a range of values in a spreadsheet."""
        return update_range(
            self.service,
            spreadsheet_id,
            a1_range,
            values,
            drive=self.drive,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
            value_input_option=value_input_option,
            include_values_in_response=include_values_in_response,
            response_value_render_option=response_value_render_option,
            response_date_time_render_option=response_date_time_render_option,
            raw=raw,
        )

    def append_row(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        values: Sequence[Any],
        *,
        parent_id: str | None = None,
        allow_multiple: bool = False,
        value_input_option: str = "RAW",
        insert_data_option: str | None = None,
        include_values_in_response: bool = False,
        raw: bool = False,
    ) -> dict | None:
        """Append a single row to the end of a sheet."""
        return append_row(
            self.service,
            spreadsheet_id,
            sheet_name,
            values,
            drive=self.drive,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
            value_input_option=value_input_option,
            insert_data_option=insert_data_option,
            include_values_in_response=include_values_in_response,
            raw=raw,
        )

    def get_sheets(
        self,
        spreadsheet_id: str,
        *,
        parent_id: str | None = None,
        allow_multiple: bool = False,
        raw: bool = False,
    ) -> list[dict] | dict:
        """Get metadata for all sheets (tabs) in a spreadsheet."""
        return get_sheets(
            self.service,
            spreadsheet_id,
            drive=self.drive,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
            raw=raw,
        )
