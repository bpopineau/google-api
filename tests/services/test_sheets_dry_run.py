"""Tests for Sheets API dry_run functionality.

These tests verify that dry_run=True returns DryRunReport without
making actual API calls.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from mygooglib.services.sheets import (
    append_row,
    batch_update,
    update_range,
)


class TestUpdateRangeDryRun:
    """Tests for update_range with dry_run=True."""

    def test_update_range_dry_run_returns_report(self) -> None:
        """update_range with dry_run=True should return DryRunReport."""
        mock_sheets = MagicMock()

        result = update_range(
            mock_sheets,
            "spreadsheet_123456789012345678901",
            "Sheet1!A1:B2",
            [["a", "b"], ["c", "d"]],
            dry_run=True,
        )

        assert isinstance(result, dict)
        assert result["action"] == "sheets.update"
        assert result["resource_id"] == "spreadsheet_123456789012345678901"
        assert result["details"]["range"] == "Sheet1!A1:B2"
        assert result["details"]["total_rows"] == 2
        assert result["details"]["total_cells"] == 4

    def test_update_range_dry_run_with_preview(self) -> None:
        """update_range with dry_run=True should include values preview."""
        mock_sheets = MagicMock()

        values = [["r1c1", "r1c2", "r1c3"], ["r2c1", "r2c2", "r2c3"]]
        result = update_range(
            mock_sheets,
            "spreadsheet_123456789012345678901",
            "Sheet1!A1:C2",
            values,
            dry_run=True,
        )

        assert "values_preview" in result["details"]
        assert len(result["details"]["values_preview"]) == 2

    def test_update_range_dry_run_no_api_call(self) -> None:
        """update_range with dry_run=True should not call API."""
        mock_sheets = MagicMock()

        update_range(
            mock_sheets,
            "spreadsheet_123456789012345678901",
            "Sheet1!A1",
            [["test"]],
            dry_run=True,
        )

        mock_sheets.spreadsheets().values().update.assert_not_called()


class TestAppendRowDryRun:
    """Tests for append_row with dry_run=True."""

    def test_append_row_dry_run_returns_report(self) -> None:
        """append_row with dry_run=True should return DryRunReport."""
        mock_sheets = MagicMock()

        result = append_row(
            mock_sheets,
            "spreadsheet_123456789012345678901",
            "Sheet1",
            ["a", "b", "c"],
            dry_run=True,
        )

        assert isinstance(result, dict)
        assert result["action"] == "sheets.append"
        assert result["details"]["sheet_name"] == "Sheet1"
        assert result["details"]["column_count"] == 3

    def test_append_row_dry_run_with_preview(self) -> None:
        """append_row with dry_run=True should include values preview."""
        mock_sheets = MagicMock()

        values = ["val1", "val2", "val3", "val4", "val5"]
        result = append_row(
            mock_sheets,
            "spreadsheet_123456789012345678901",
            "Data",
            values,
            dry_run=True,
        )

        assert result["details"]["values_preview"] == values

    def test_append_row_dry_run_no_api_call(self) -> None:
        """append_row with dry_run=True should not call API."""
        mock_sheets = MagicMock()

        append_row(
            mock_sheets,
            "spreadsheet_123456789012345678901",
            "Sheet1",
            ["test"],
            dry_run=True,
        )

        mock_sheets.spreadsheets().values().append.assert_not_called()


class TestBatchUpdateDryRun:
    """Tests for batch_update with dry_run=True."""

    def test_batch_update_dry_run_returns_report(self) -> None:
        """batch_update with dry_run=True should return DryRunReport."""
        mock_sheets = MagicMock()

        updates = [
            {"range": "A1:B2", "values": [[1, 2], [3, 4]]},
            {"range": "C1:D2", "values": [[5, 6], [7, 8]]},
        ]
        result = batch_update(
            mock_sheets,
            "spreadsheet_123456789012345678901",
            updates,
            dry_run=True,
        )

        assert isinstance(result, dict)
        assert result["action"] == "sheets.batch_update"
        assert result["details"]["range_count"] == 2
        assert result["details"]["total_cells"] == 8

    def test_batch_update_dry_run_ranges_preview(self) -> None:
        """batch_update with dry_run=True should include ranges preview."""
        mock_sheets = MagicMock()

        updates = [
            {"range": "Sheet1!A1", "values": [["x"]]},
            {"range": "Sheet2!B2", "values": [["y"]]},
        ]
        result = batch_update(
            mock_sheets,
            "spreadsheet_123456789012345678901",
            updates,
            dry_run=True,
        )

        preview = result["details"]["ranges_preview"]
        assert len(preview) == 2
        assert preview[0]["range"] == "Sheet1!A1"
        assert preview[1]["range"] == "Sheet2!B2"

    def test_batch_update_dry_run_no_api_call(self) -> None:
        """batch_update with dry_run=True should not call API."""
        mock_sheets = MagicMock()

        batch_update(
            mock_sheets,
            "spreadsheet_123456789012345678901",
            [{"range": "A1", "values": [["test"]]}],
            dry_run=True,
        )

        mock_sheets.spreadsheets().values().batchUpdate.assert_not_called()
