"""A1 notation helpers for Sheets."""

from __future__ import annotations

import re


def col_to_a1(col: int) -> str:
    """Convert 1-indexed column number to A1 letter(s). 1 -> 'A', 27 -> 'AA'.
    
    Args:
        col: Column number (1-indexed). Must be between 1 and 18278 (max Sheets columns: ZZZ).
        
    Raises:
        ValueError: If col is out of valid range.
    """
    if col < 1:
        raise ValueError("Column must be >= 1")
    # Google Sheets maximum is column ZZZ (18278)
    if col > 18278:
        raise ValueError("Column must be <= 18278 (ZZZ is the maximum in Google Sheets)")
    result = []
    while col:
        col, rem = divmod(col - 1, 26)
        result.append(chr(65 + rem))
    return "".join(reversed(result))


def a1_to_col(letters: str) -> int:
    """Convert A1 column letters to 1-indexed number. 'A' -> 1, 'AA' -> 27."""
    letters = letters.upper()
    result = 0
    for char in letters:
        result = result * 26 + (ord(char) - 64)
    return result


def range_to_a1(
    start_row: int,
    start_col: int,
    end_row: int | None = None,
    end_col: int | None = None,
    sheet_name: str | None = None,
) -> str:
    """Build an A1 range string from 1-indexed row/col coordinates.

    Examples:
        range_to_a1(1, 1) -> 'A1'
        range_to_a1(1, 1, 10, 3) -> 'A1:C10'
        range_to_a1(1, 1, 10, 3, sheet_name='Data') -> "'Data'!A1:C10"
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
