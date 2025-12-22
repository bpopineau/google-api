"""Tests for Sheets BatchUpdater context manager."""

from unittest.mock import MagicMock, patch

import pytest

from mygooglib.services.sheets import BatchUpdater


@pytest.fixture
def mock_sheets():
    """Create a mock Sheets service."""
    return MagicMock()


def test_batch_updater_queues_updates(mock_sheets):
    """Test that updates are queued but not executed until exit."""
    updater = BatchUpdater(mock_sheets, "test-spreadsheet-id")

    updater.update("A1:B2", [[1, 2], [3, 4]])
    updater.update("C1:D2", [[5, 6], [7, 8]])

    assert updater.pending_count == 2
    assert updater._updates[0] == {"range": "A1:B2", "values": [[1, 2], [3, 4]]}
    assert updater._updates[1] == {"range": "C1:D2", "values": [[5, 6], [7, 8]]}


def test_batch_updater_append_method(mock_sheets):
    """Test the append convenience method."""
    updater = BatchUpdater(mock_sheets, "test-spreadsheet-id")

    updater.append("Sheet1!A:Z", ["value1", "value2", "value3"])

    assert updater.pending_count == 1
    assert updater._updates[0] == {
        "range": "Sheet1!A:Z",
        "values": [["value1", "value2", "value3"]],
    }


@patch("mygooglib.services.sheets.batch_update")
def test_batch_updater_commits_on_exit(mock_batch_update, mock_sheets):
    """Test that updates are committed on context exit."""
    mock_batch_update.return_value = {"totalUpdatedCells": 8}

    with BatchUpdater(mock_sheets, "test-spreadsheet-id") as batch:
        batch.update("A1:B2", [[1, 2], [3, 4]])
        batch.update("C1:D2", [[5, 6], [7, 8]])

    # Verify batch_update was called with correct arguments
    mock_batch_update.assert_called_once()
    args, kwargs = mock_batch_update.call_args

    assert args[0] == mock_sheets
    assert args[1] == "test-spreadsheet-id"
    assert len(args[2]) == 2  # Two updates


@patch("mygooglib.services.sheets.batch_update")
def test_batch_updater_no_commit_on_exception(mock_batch_update, mock_sheets):
    """Test that updates are NOT committed if an exception occurs."""
    try:
        with BatchUpdater(mock_sheets, "test-spreadsheet-id") as batch:
            batch.update("A1:B2", [[1, 2]])
            raise ValueError("Simulated error")
    except ValueError:
        pass

    # batch_update should NOT have been called
    mock_batch_update.assert_not_called()


@patch("mygooglib.services.sheets.batch_update")
def test_batch_updater_no_commit_if_empty(mock_batch_update, mock_sheets):
    """Test that batch_update is not called if no updates were queued."""
    with BatchUpdater(mock_sheets, "test-spreadsheet-id"):
        pass  # No updates

    mock_batch_update.assert_not_called()


