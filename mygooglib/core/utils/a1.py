"""A1 notation helpers for Sheets."""

from __future__ import annotations

import re


def col_to_a1(col: int) -> str:
    """Convert 1-indexed column number to A1 letter(s). 1 -> 'A', 27 -> 'AA'.

    Args:
        col: Column number (1-indexed). Must be between 1 and 18278 (max Sheets columns: ZZZ).

    Raises:
        ValueError: If col is out of valid range.

    Examples:
        >>> col_to_a1(1)
        'A'
        >>> col_to_a1(27)
        'AA'
        >>> col_to_a1(28)
        'AB'
    """
    if col < 1:
        raise ValueError("Column must be >= 1")
    # Google Sheets maximum is column ZZZ (18278)
    if col > 18278:
        raise ValueError(
            "Column must be <= 18278 (ZZZ is the maximum in Google Sheets)"
        )
    result = []
    while col:
        col, rem = divmod(col - 1, 26)
        result.append(chr(65 + rem))
    return "".join(reversed(result))


def a1_to_col(letters: str) -> int:
    """Convert A1 column letters to 1-indexed number. 'A' -> 1, 'AA' -> 27.

    Examples:
        >>> a1_to_col('A')
        1
        >>> a1_to_col('AA')
        27
        >>> a1_to_col('Z')
        26
    """
    letters = letters.upper()
    result = 0
    for char in letters:
        result = result * 26 + (ord(char) - 64)
    return result


def a1_to_range(
    a1_range: str,
) -> tuple[str | None, int, int, int | None, int | None]:
    """Parse an A1 range string into components.

    Args:
        a1_range: A1 notation string like "Sheet1!A1:C10" or "A1:B5"

    Returns:
        Tuple of (sheet_name, start_row, start_col, end_row, end_col).
        sheet_name is None if not specified.
        end_row and end_col are None if it's a single cell.

    Examples:
        >>> a1_to_range("A1")
        (None, 1, 1, None, None)
        >>> a1_to_range("A1:C10")
        (None, 1, 1, 10, 3)
        >>> a1_to_range("Sheet1!A1:C10")
        ('Sheet1', 1, 1, 10, 3)
    """
    sheet_name: str | None = None
    cell_range = a1_range

    # Check for sheet name prefix
    if "!" in a1_range:
        sheet_part, cell_range = a1_range.rsplit("!", 1)
        # Remove surrounding quotes if present
        if sheet_part.startswith("'") and sheet_part.endswith("'"):
            sheet_part = sheet_part[1:-1].replace("''", "'")
        sheet_name = sheet_part

    # Parse cell range (e.g., "A1:C10" or "A1")
    cell_pattern = re.compile(r"^([A-Za-z]+)(\d+)(?::([A-Za-z]+)(\d+))?$")
    match = cell_pattern.match(cell_range)
    if not match:
        raise ValueError(f"Invalid A1 notation: {a1_range}")

    start_col_str, start_row_str, end_col_str, end_row_str = match.groups()

    start_row = int(start_row_str)
    start_col = a1_to_col(start_col_str)

    end_row: int | None = None
    end_col: int | None = None
    if end_row_str and end_col_str:
        end_row = int(end_row_str)
        end_col = a1_to_col(end_col_str)

    return (sheet_name, start_row, start_col, end_row, end_col)


def range_to_a1(
    sheet_name: str | None,
    start_row: int,
    start_col: int,
    end_row: int | None = None,
    end_col: int | None = None,
) -> str:
    """Build an A1 range string from 1-indexed row/col coordinates.

    Examples:
        >>> range_to_a1(None, 1, 1)
        'A1'
        >>> range_to_a1(None, 1, 1, 10, 3)
        'A1:C10'
        >>> range_to_a1('Data', 1, 1, 10, 3)
        'Data!A1:C10'
    """
    start = f"{col_to_a1(start_col)}{start_row}"
    if end_row is None and end_col is None:
        cell = start
    else:
        end = f"{col_to_a1(end_col or start_col)}{end_row or start_row}"
        cell = f"{start}:{end}"

    if sheet_name:
        # Quote sheet name if it contains spaces or special chars
        if re.search(r"[\s']", sheet_name):
            sheet_name = f"'{sheet_name}'"
        return f"{sheet_name}!{cell}"
    return cell
