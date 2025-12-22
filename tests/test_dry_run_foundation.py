"""Tests for DryRunReport TypedDict and dry-run foundation.

These tests verify the structure and type compatibility of the DryRunReport
type used across all dry-run enabled operations.
"""

from __future__ import annotations

from mygooglib.core.types import DryRunReport


class TestDryRunReportStructure:
    """Tests for DryRunReport TypedDict structure."""

    def test_dry_run_report_has_required_keys(self) -> None:
        """DryRunReport should support the documented keys."""
        report: DryRunReport = {
            "action": "drive.delete",
            "resource_id": "abc123",
            "details": {"file_name": "test.txt", "permanent": False},
        }
        assert report["action"] == "drive.delete"
        assert report["resource_id"] == "abc123"
        assert "file_name" in report["details"]

    def test_dry_run_report_with_reason(self) -> None:
        """DryRunReport should accept optional reason field."""
        report: DryRunReport = {
            "action": "drive.sync_upload",
            "resource_id": "folder_id",
            "details": {"local_path": "/tmp/file.txt"},
            "reason": "File modified after last sync",
        }
        assert report.get("reason") == "File modified after last sync"

    def test_dry_run_report_minimum_valid(self) -> None:
        """DryRunReport should work with minimal fields."""
        # TypedDict with total=False allows partial initialization
        report: DryRunReport = {
            "action": "sheets.update",
            "resource_id": "spreadsheet_id",
            "details": {},
        }
        assert "action" in report
        assert report.get("reason") is None


class TestDryRunReportPatterns:
    """Test expected patterns for different operation types."""

    def test_drive_delete_pattern(self) -> None:
        """Drive delete reports should follow expected pattern."""
        report: DryRunReport = {
            "action": "drive.delete",
            "resource_id": "file_id_123",
            "details": {
                "file_name": "document.pdf",
                "permanent": True,
            },
        }
        assert report["action"] == "drive.delete"
        assert report["details"]["permanent"] is True

    def test_drive_upload_pattern(self) -> None:
        """Drive upload reports should follow expected pattern."""
        report: DryRunReport = {
            "action": "drive.upload",
            "resource_id": "pending",
            "details": {
                "local_path": "/home/user/file.txt",
                "parent_id": "parent_folder_id",
                "name": "file.txt",
            },
        }
        assert report["details"]["local_path"] == "/home/user/file.txt"

    def test_sheets_update_pattern(self) -> None:
        """Sheets update reports should follow expected pattern."""
        report: DryRunReport = {
            "action": "sheets.update",
            "resource_id": "spreadsheet_abc",
            "details": {
                "range": "Sheet1!A1:B2",
                "values_preview": [["a", "b"], ["c", "d"]],
                "total_cells": 4,
            },
        }
        assert report["details"]["total_cells"] == 4

    def test_sync_folder_pattern(self) -> None:
        """Sync folder should return list of DryRunReport objects."""
        reports: list[DryRunReport] = [
            {
                "action": "drive.upload",
                "resource_id": "pending",
                "details": {"local_path": "/path/to/new_file.txt"},
                "reason": "New file not found in Drive",
            },
            {
                "action": "drive.update",
                "resource_id": "existing_file_id",
                "details": {"local_path": "/path/to/modified.txt"},
                "reason": "Local file newer than remote",
            },
        ]
        assert len(reports) == 2
        assert all("reason" in r for r in reports)


class TestMakeDryRunReportHelper:
    """Tests for the make_dry_run_report factory function."""

    def test_basic_report_creation(self) -> None:
        """make_dry_run_report should create valid reports."""
        from mygooglib.core.utils.base import make_dry_run_report

        report = make_dry_run_report(
            "drive.delete",
            "file_123",
            {"permanent": True},
        )
        assert report["action"] == "drive.delete"
        assert report["resource_id"] == "file_123"
        assert report["details"]["permanent"] is True

    def test_report_with_reason(self) -> None:
        """make_dry_run_report should include reason when provided."""
        from mygooglib.core.utils.base import make_dry_run_report

        report = make_dry_run_report(
            "drive.upload",
            "pending",
            {"local_path": "/tmp/file.txt"},
            reason="File newer than remote",
        )
        assert report.get("reason") == "File newer than remote"

    def test_report_without_details(self) -> None:
        """make_dry_run_report should use empty dict when no details."""
        from mygooglib.core.utils.base import make_dry_run_report

        report = make_dry_run_report("sheets.clear", "sheet_id")
        assert report["details"] == {}

    def test_report_without_reason(self) -> None:
        """make_dry_run_report should not include reason key if None."""
        from mygooglib.core.utils.base import make_dry_run_report

        report = make_dry_run_report("drive.delete", "file_id")
        assert "reason" not in report
