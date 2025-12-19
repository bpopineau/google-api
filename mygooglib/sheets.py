"""Google Sheets wrapper — get_range, update_range, append_row.

These helpers take the raw Sheets v4 Resource from `get_clients().sheets`.
They return plain Python types by default, with a `raw=True` escape hatch.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any

from mygooglib.utils.base import BaseClient
from mygooglib.utils.retry import api_call, execute_with_retry_http_error

try:
    import pandas as pd
except ImportError:
    pd = None

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
    escaped = title.replace("'", "''")
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


@api_call("Sheets get_range", is_write=False)
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


@api_call("Sheets update_range", is_write=True)
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


@api_call("Sheets append_row", is_write=True)
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


@api_call("Sheets get_sheets", is_write=False)
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

    request = sheets.spreadsheets().get(
        spreadsheetId=spreadsheet_real_id, fields="sheets(properties)"
    )
    response = execute_with_retry_http_error(request, is_write=False)

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


def to_dataframe(
    sheets: Any,
    spreadsheet_id: str,
    a1_range: str,
    *,
    drive: Any | None = None,
    header: bool = True,
) -> "pd.DataFrame":
    """Read a range into a Pandas DataFrame.

    Requires 'pandas' to be installed.

    Args:
        sheets: Sheets API Resource
        spreadsheet_id: Spreadsheet ID, title, or URL
        a1_range: A1 range string
        drive: Optional Drive API Resource for title resolution
        header: If True, use the first row as the header

    Returns:
        A pandas DataFrame.

    Raises:
        ImportError: If pandas is not installed.
    """
    if pd is None:
        raise ImportError("Pandas is required for this feature. Install 'pandas'.")

    values = get_range(sheets, spreadsheet_id, a1_range, drive=drive)
    if not values:
        return pd.DataFrame()

    if header:
        return pd.DataFrame(values[1:], columns=values[0])
    return pd.DataFrame(values)


def from_dataframe(
    sheets: Any,
    spreadsheet_id: str,
    sheet_name: str,
    df: "pd.DataFrame",
    *,
    drive: Any | None = None,
    start_cell: str = "A1",
    include_header: bool = True,
    include_index: bool = False,
    resize: bool = False,
) -> dict | None:
    """Write a Pandas DataFrame to a sheet.

    Args:
        sheets: Sheets API Resource
        spreadsheet_id: Spreadsheet ID, title, or URL
        sheet_name: Tab name to write to
        df: The DataFrame to write
        drive: Optional Drive API Resource
        start_cell: Top-left cell (default 'A1')
        include_header: Whether to write column names
        include_index: Whether to write the index
        resize: If True, clear the sheet and resize it to fit (not implemented in v0.3)

    Returns:
        Result of update_range.
    """
    if pd is None:
        raise ImportError("Pandas is required for this feature. Install 'pandas'.")

    # Convert to list of lists, handling NaNs as empty strings (JSON compliant)
    values = df.fillna("").reset_index(drop=not include_index).values.tolist()

    if include_header:
        cols = list(df.columns)
        if include_index:
            # If index is included, we need a name for the index column(s)
            index_names = list(df.index.names)
            # If simple unnamed index, just empty string
            index_names = [n if n else "" for n in index_names]
            cols = index_names + cols
        values.insert(0, cols)

    # Construct target range
    safe_sheet = _quote_sheet_name(sheet_name)
    target_range = f"{safe_sheet}!{start_cell}"

    return update_range(
        sheets,
        spreadsheet_id,
        target_range,
        values,
        drive=drive,
        value_input_option="USER_ENTERED",  # Usually want implicit conversion
    )


@api_call("Sheets batch_get", is_write=False)
def batch_get(
    sheets: Any,
    spreadsheet_id: str,
    ranges: list[str],
    *,
    drive: Any | None = None,
    parent_id: str | None = None,
    allow_multiple: bool = False,
    major_dimension: str | None = None,
    value_render_option: str | None = None,
    date_time_render_option: str | None = None,
    raw: bool = False,
) -> dict[str, list[list[Any]]] | dict:
    """Read multiple ranges from a spreadsheet in a single API call.

    Args:
        sheets: Sheets API Resource
        spreadsheet_id: Spreadsheet ID, title, or URL
        ranges: List of A1 range strings (e.g., ["Sheet1!A1:B10", "Sheet2!C1:D5"])
        drive: Drive API Resource (required if spreadsheet_id is a title)
        parent_id: Optional Drive folder ID for title resolution
        allow_multiple: Allow multiple title matches
        major_dimension: "ROWS" or "COLUMNS" (optional)
        value_render_option: "FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"
        date_time_render_option: "SERIAL_NUMBER" or "FORMATTED_STRING"
        raw: If True, return the full API response dict

    Returns:
        Dict mapping range strings to their values (list-of-lists).
        If raw=True, returns the full API response.
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
            "Spreadsheet identifier looks like a title; pass drive=clients.drive."
        )

    request = (
        sheets.spreadsheets()
        .values()
        .batchGet(
            spreadsheetId=spreadsheet_real_id,
            ranges=ranges,
            majorDimension=major_dimension,
            valueRenderOption=value_render_option,
            dateTimeRenderOption=date_time_render_option,
        )
    )
    response = execute_with_retry_http_error(request, is_write=False)

    if raw:
        return response

    # Map each range to its values
    result: dict[str, list[list[Any]]] = {}
    for value_range in response.get("valueRanges", []):
        range_key = value_range.get("range", "")
        result[range_key] = value_range.get("values", [])
    return result


@api_call("Sheets batch_update", is_write=True)
def batch_update(
    sheets: Any,
    spreadsheet_id: str,
    updates: list[dict[str, Any]],
    *,
    drive: Any | None = None,
    parent_id: str | None = None,
    allow_multiple: bool = False,
    value_input_option: str = "RAW",
    include_values_in_response: bool = False,
    response_value_render_option: str | None = None,
    response_date_time_render_option: str | None = None,
    raw: bool = False,
) -> dict:
    """Update multiple ranges in a spreadsheet in a single API call.

    Args:
        sheets: Sheets API Resource
        spreadsheet_id: Spreadsheet ID, title, or URL
        updates: List of dicts with "range" and "values" keys.
                 Example: [{"range": "A1:B2", "values": [[1, 2], [3, 4]]}]
        drive: Drive API Resource (required if spreadsheet_id is a title)
        parent_id: Optional Drive folder ID for title resolution
        allow_multiple: Allow multiple title matches
        value_input_option: "RAW" (default) or "USER_ENTERED"
        include_values_in_response: If True, response includes written values
        response_value_render_option: Optional render option for returned values
        response_date_time_render_option: Optional datetime render option
        raw: If True, return the full API response dict

    Returns:
        Summary dict with totalUpdatedRows, totalUpdatedCells, etc.
        If raw=True, returns the full API response.
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
            "Spreadsheet identifier looks like a title; pass drive=clients.drive."
        )

    # Build the data array for batchUpdate
    data = []
    for update in updates:
        range_str = update.get("range")
        values = update.get("values", [])
        if not range_str:
            raise ValueError("Each update must have a 'range' key")
        data.append({"range": range_str, "values": [list(row) for row in values]})

    body = {
        "valueInputOption": value_input_option,
        "data": data,
        "includeValuesInResponse": include_values_in_response,
        "responseValueRenderOption": response_value_render_option,
        "responseDateTimeRenderOption": response_date_time_render_option,
    }

    request = (
        sheets.spreadsheets()
        .values()
        .batchUpdate(spreadsheetId=spreadsheet_real_id, body=body)
    )
    response = execute_with_retry_http_error(request, is_write=True)

    if raw:
        return response

    return {
        "spreadsheetId": response.get("spreadsheetId"),
        "totalUpdatedRows": response.get("totalUpdatedRows"),
        "totalUpdatedColumns": response.get("totalUpdatedColumns"),
        "totalUpdatedCells": response.get("totalUpdatedCells"),
        "totalUpdatedSheets": response.get("totalUpdatedSheets"),
    }


class BatchUpdater:
    """Context manager for batching Sheets updates.

    Collects multiple update operations and executes them as a single
    batchUpdate API call when the context exits.

    Example:
        with BatchUpdater(sheets, spreadsheet_id) as batch:
            batch.update("A1:B2", [[1, 2], [3, 4]])
            batch.update("C1:D2", [[5, 6], [7, 8]])
        # Both updates are sent in a single API call on context exit

    Args:
        sheets: Sheets API Resource from get_clients().sheets
        spreadsheet_id: Spreadsheet ID, title, or URL
        drive: Optional Drive API Resource for title resolution
        parent_id: Optional Drive folder ID for title resolution
        allow_multiple: Allow multiple title matches
        value_input_option: "RAW" (default) or "USER_ENTERED"
    """

    def __init__(
        self,
        sheets: Any,
        spreadsheet_id: str,
        *,
        drive: Any | None = None,
        parent_id: str | None = None,
        allow_multiple: bool = False,
        value_input_option: str = "RAW",
    ):
        self._sheets = sheets
        self._spreadsheet_id = spreadsheet_id
        self._drive = drive
        self._parent_id = parent_id
        self._allow_multiple = allow_multiple
        self._value_input_option = value_input_option
        self._updates: list[dict[str, Any]] = []

    def update(self, range: str, values: Sequence[Sequence[Any]]) -> None:
        """Queue an update to be executed on context exit.

        Args:
            range: A1 notation range (e.g., "Sheet1!A1:B2")
            values: 2D list of values to write
        """
        self._updates.append({"range": range, "values": [list(row) for row in values]})

    def append(self, range: str, row: Sequence[Any]) -> None:
        """Queue a single row append (convenience method).

        Args:
            range: A1 notation range (e.g., "Sheet1!A:Z")
            row: Single row of values to append
        """
        self._updates.append({"range": range, "values": [list(row)]})

    def __enter__(self) -> "BatchUpdater":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # Only commit if no exception and we have updates
        if exc_type is None and self._updates:
            batch_update(
                self._sheets,
                self._spreadsheet_id,
                self._updates,
                drive=self._drive,
                parent_id=self._parent_id,
                allow_multiple=self._allow_multiple,
                value_input_option=self._value_input_option,
            )

    @property
    def pending_count(self) -> int:
        """Return the number of queued updates."""
        return len(self._updates)


class SheetsClient(BaseClient):
    """Simplified Google Sheets API wrapper focusing on common operations."""

    def __init__(self, service: Any, drive: Any | None = None):
        """Initialize with an authorized Sheets API service object.

        Args:
            service: Sheets API Resource from get_clients().sheets
            drive: Optional Drive API Resource for title-based resolution
        """
        super().__init__(service)
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

    def to_dataframe(
        self,
        spreadsheet_id: str,
        a1_range: str,
        *,
        header: bool = True,
    ) -> "pd.DataFrame":
        """Read a range into a Pandas DataFrame."""
        return to_dataframe(
            self.service,
            spreadsheet_id,
            a1_range,
            drive=self.drive,
            header=header,
        )

    def from_dataframe(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        df: "pd.DataFrame",
        *,
        start_cell: str = "A1",
        include_header: bool = True,
        include_index: bool = False,
        resize: bool = False,
    ) -> dict | None:
        """Write a Pandas DataFrame to a sheet."""
        return from_dataframe(
            self.service,
            spreadsheet_id,
            sheet_name,
            df,
            drive=self.drive,
            start_cell=start_cell,
            include_header=include_header,
            include_index=include_index,
        )

    def batch_get(
        self,
        spreadsheet_id: str,
        ranges: list[str],
        *,
        parent_id: str | None = None,
        allow_multiple: bool = False,
        major_dimension: str | None = None,
        value_render_option: str | None = None,
        date_time_render_option: str | None = None,
        raw: bool = False,
    ) -> dict[str, list[list[Any]]] | dict:
        """Read multiple ranges from a spreadsheet in a single API call."""
        return batch_get(
            self.service,
            spreadsheet_id,
            ranges,
            drive=self.drive,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
            major_dimension=major_dimension,
            value_render_option=value_render_option,
            date_time_render_option=date_time_render_option,
            raw=raw,
        )

    def batch_update(
        self,
        spreadsheet_id: str,
        updates: list[dict[str, Any]],
        *,
        parent_id: str | None = None,
        allow_multiple: bool = False,
        value_input_option: str = "RAW",
        include_values_in_response: bool = False,
        response_value_render_option: str | None = None,
        response_date_time_render_option: str | None = None,
        raw: bool = False,
    ) -> dict:
        """Update multiple ranges in a spreadsheet in a single API call."""
        return batch_update(
            self.service,
            spreadsheet_id,
            updates,
            drive=self.drive,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
            value_input_option=value_input_option,
            include_values_in_response=include_values_in_response,
            response_value_render_option=response_value_render_option,
            response_date_time_render_option=response_date_time_render_option,
            raw=raw,
        )

    def batch(
        self,
        spreadsheet_id: str,
        *,
        parent_id: str | None = None,
        allow_multiple: bool = False,
        value_input_option: str = "RAW",
    ) -> BatchUpdater:
        """Create a batch context manager for efficient bulk updates.

        Example:
            with client.batch(spreadsheet_id) as batch:
                batch.update("A1:B2", [[1, 2], [3, 4]])
                batch.update("C1:D2", [[5, 6], [7, 8]])
            # Both updates sent in a single API call

        Args:
            spreadsheet_id: Spreadsheet ID, title, or URL
            parent_id: Optional Drive folder ID for title resolution
            allow_multiple: Allow multiple title matches
            value_input_option: "RAW" (default) or "USER_ENTERED"

        Returns:
            BatchUpdater context manager
        """
        return BatchUpdater(
            self.service,
            spreadsheet_id,
            drive=self.drive,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
            value_input_option=value_input_option,
        )


@api_call("Sheets clear_sheet", is_write=True)
def clear_sheet(
    sheets: Any,
    spreadsheet_id: str,
    sheet_name: str,
    *,
    drive: Any | None = None,
    parent_id: str | None = None,
    allow_multiple: bool = False,
    raw: bool = False,
) -> dict | None:
    """Clear all values from a specific sheet (tab).

    Args:
        sheets: Sheets API Resource
        spreadsheet_id: Spreadsheet ID, title, or URL
        sheet_name: Name of the sheet to clear (e.g., 'Sheet1')
        drive: Drive API Resource (required if spreadsheet_id is a title)
        parent_id: Optional Drive folder ID for title resolution
        allow_multiple: Allow multiple title matches
        raw: If True, return full API response

    Returns:
        Summary dict of cleared range, or full response if raw=True.
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

    safe_sheet = _quote_sheet_name(sheet_name)
    # Clear the entire sheet
    range_to_clear = f"{safe_sheet}"

    request = (
        sheets.spreadsheets()
        .values()
        .clear(spreadsheetId=spreadsheet_real_id, range=range_to_clear)
    )
    response = execute_with_retry_http_error(request, is_write=True)

    if raw:
        return response
    if not response:
        return None

    return {
        "clearedRange": response.get("clearedRange"),
    }


def batch_write(
    sheets: Any,
    spreadsheet_id: str,
    sheet_name: str,
    rows: Sequence[Sequence[Any]],
    *,
    headers: Sequence[str] | None = None,
    drive: Any | None = None,
    parent_id: str | None = None,
    allow_multiple: bool = False,
    clear: bool = False,
    start_cell: str = "A1",
) -> dict | None:
    """Write a batch of rows to a sheet, optionally clearing it first.

    Args:
        sheets: Sheets API Resource
        spreadsheet_id: Spreadsheet ID, title, or URL
        sheet_name: Name of the sheet to write to
        rows: List of lists containing the data rows
        headers: Optional list of header strings to write as the first row
        drive: Drive API Resource (required if spreadsheet_id is a title)
        parent_id: Optional Drive folder ID for title resolution
        allow_multiple: Allow multiple title matches
        clear: If True, clear the sheet before writing
        start_cell: Top-left cell to start writing (default 'A1')

    Returns:
        Result of the update_range call.
    """
    if clear:
        clear_sheet(
            sheets,
            spreadsheet_id,
            sheet_name,
            drive=drive,
            parent_id=parent_id,
            allow_multiple=allow_multiple,
        )

    values = list(rows)
    if headers:
        values.insert(0, list(headers))

    safe_sheet = _quote_sheet_name(sheet_name)
    target_range = f"{safe_sheet}!{start_cell}"

    return update_range(
        sheets,
        spreadsheet_id,
        target_range,
        values,
        drive=drive,
        parent_id=parent_id,
        allow_multiple=allow_multiple,
        value_input_option="USER_ENTERED",
    )
