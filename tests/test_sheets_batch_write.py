"""Tests for sheets.batch_write."""

from unittest.mock import MagicMock, patch

import pytest

from mygooglib.services.sheets import batch_write


@pytest.fixture
def mock_sheets():
    """Create a mock Sheets service."""
    return MagicMock()


@patch("mygooglib.services.sheets.update_range")
@patch("mygooglib.services.sheets.clear_sheet")
def test_batch_write_basic(mock_clear, mock_update, mock_sheets):
    """Test basic batch write without clearing or headers."""
    rows = [[1, 2], [3, 4]]
    batch_write(mock_sheets, "sheet_id", "Sheet1", rows)

    mock_clear.assert_not_called()
    mock_update.assert_called_once_with(
        mock_sheets,
        "sheet_id",
        "Sheet1!A1",
        [[1, 2], [3, 4]],
        drive=None,
        parent_id=None,
        allow_multiple=False,
        value_input_option="USER_ENTERED",
    )


@patch("mygooglib.services.sheets.update_range")
@patch("mygooglib.services.sheets.clear_sheet")
def test_batch_write_with_clear(mock_clear, mock_update, mock_sheets):
    """Test batch write with clear option."""
    rows = [[1, 2]]
    batch_write(mock_sheets, "sheet_id", "Sheet1", rows, clear=True)

    mock_clear.assert_called_once_with(
        mock_sheets,
        "sheet_id",
        "Sheet1",
        drive=None,
        parent_id=None,
        allow_multiple=False,
    )
    mock_update.assert_called_once()


@patch("mygooglib.services.sheets.update_range")
@patch("mygooglib.services.sheets.clear_sheet")
def test_batch_write_with_headers(mock_clear, mock_update, mock_sheets):
    """Test batch write with headers."""
    headers = ["Col1", "Col2"]
    rows = [[1, 2]]
    batch_write(mock_sheets, "sheet_id", "Sheet1", rows, headers=headers)

    mock_update.assert_called_once_with(
        mock_sheets,
        "sheet_id",
        "Sheet1!A1",
        [["Col1", "Col2"], [1, 2]],
        drive=None,
        parent_id=None,
        allow_multiple=False,
        value_input_option="USER_ENTERED",
    )


@patch("mygooglib.services.sheets.update_range")
@patch("mygooglib.services.sheets.clear_sheet")
def test_batch_write_custom_start_cell(mock_clear, mock_update, mock_sheets):
    """Test batch write with custom start cell."""
    rows = [[1, 2]]
    batch_write(mock_sheets, "sheet_id", "Sheet1", rows, start_cell="B2")

    mock_update.assert_called_once_with(
        mock_sheets,
        "sheet_id",
        "Sheet1!B2",
        [[1, 2]],
        drive=None,
        parent_id=None,
        allow_multiple=False,
        value_input_option="USER_ENTERED",
    )
