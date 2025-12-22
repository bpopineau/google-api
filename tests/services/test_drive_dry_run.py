"""Tests for Drive API dry_run functionality.

These tests verify that dry_run=True returns DryRunReport without
making actual API calls.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mygooglib.services.drive import (
    create_folder,
    delete_file,
    upload_file,
)


class TestDeleteFileDryRun:
    """Tests for delete_file with dry_run=True."""

    def test_delete_file_dry_run_returns_report(self) -> None:
        """delete_file with dry_run=True should return DryRunReport."""
        mock_drive = MagicMock()
        # Mock the files().get() call for fetching file name
        mock_drive.files().get().execute.return_value = {"name": "test.txt"}

        result = delete_file(mock_drive, "file_123", dry_run=True)

        assert isinstance(result, dict)
        assert result["action"] == "drive.delete"
        assert result["resource_id"] == "file_123"
        assert result["details"]["file_name"] == "test.txt"
        assert result["details"]["permanent"] is False

    def test_delete_file_dry_run_permanent(self) -> None:
        """delete_file with dry_run=True and permanent=True."""
        mock_drive = MagicMock()
        mock_drive.files().get().execute.return_value = {"name": "important.pdf"}

        result = delete_file(mock_drive, "file_456", permanent=True, dry_run=True)

        assert result["details"]["permanent"] is True
        assert result["details"]["file_name"] == "important.pdf"

    def test_delete_file_dry_run_no_api_modify(self) -> None:
        """delete_file with dry_run=True should not call files().delete()."""
        mock_drive = MagicMock()
        mock_drive.files().get().execute.return_value = {"name": "test.txt"}

        delete_file(mock_drive, "file_123", dry_run=True)

        # Should NOT call delete or update (the modifying operations)
        mock_drive.files().delete.assert_not_called()
        mock_drive.files().update.assert_not_called()


class TestUploadFileDryRun:
    """Tests for upload_file with dry_run=True."""

    def test_upload_file_dry_run_returns_report(self, tmp_path: Path) -> None:
        """upload_file with dry_run=True should return DryRunReport."""
        # Create a real temp file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")

        mock_drive = MagicMock()

        result = upload_file(mock_drive, test_file, dry_run=True)

        assert isinstance(result, dict)
        assert result["action"] == "drive.upload"
        assert result["resource_id"] == "pending"
        assert result["details"]["name"] == "test.txt"
        assert result["details"]["parent_id"] == "root"
        assert result["details"]["size_bytes"] > 0

    def test_upload_file_dry_run_with_parent(self, tmp_path: Path) -> None:
        """upload_file with dry_run=True should include parent_id."""
        test_file = tmp_path / "data.csv"
        test_file.write_text("a,b,c")

        mock_drive = MagicMock()

        result = upload_file(
            mock_drive, test_file, parent_id="folder_123", dry_run=True
        )

        assert result["details"]["parent_id"] == "folder_123"

    def test_upload_file_dry_run_no_api_call(self, tmp_path: Path) -> None:
        """upload_file with dry_run=True should not call files().create()."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        mock_drive = MagicMock()

        upload_file(mock_drive, test_file, dry_run=True)

        mock_drive.files().create.assert_not_called()

    def test_upload_file_still_validates_file_exists(self) -> None:
        """upload_file should raise FileNotFoundError even with dry_run=True."""
        mock_drive = MagicMock()

        with pytest.raises(FileNotFoundError):
            upload_file(mock_drive, "/nonexistent/file.txt", dry_run=True)


class TestCreateFolderDryRun:
    """Tests for create_folder with dry_run=True."""

    def test_create_folder_dry_run_returns_report(self) -> None:
        """create_folder with dry_run=True should return DryRunReport."""
        mock_drive = MagicMock()

        result = create_folder(mock_drive, "New Folder", dry_run=True)

        assert isinstance(result, dict)
        assert result["action"] == "drive.create_folder"
        assert result["resource_id"] == "pending"
        assert result["details"]["name"] == "New Folder"
        assert result["details"]["parent_id"] == "root"

    def test_create_folder_dry_run_with_parent(self) -> None:
        """create_folder with dry_run=True should include parent_id."""
        mock_drive = MagicMock()

        result = create_folder(
            mock_drive, "Subfolder", parent_id="parent_123", dry_run=True
        )

        assert result["details"]["parent_id"] == "parent_123"

    def test_create_folder_dry_run_no_api_call(self) -> None:
        """create_folder with dry_run=True should not call files().create()."""
        mock_drive = MagicMock()

        create_folder(mock_drive, "Test Folder", dry_run=True)

        mock_drive.files().create.assert_not_called()


class TestSyncFolderDryRunReports:
    """Tests for sync_folder returning DryRunReport objects."""

    def test_sync_folder_dry_run_returns_reports_key(self, tmp_path: Path) -> None:
        """sync_folder with dry_run=True should include 'reports' key."""
        from mygooglib.services.drive import sync_folder

        # Create a test file
        (tmp_path / "new_file.txt").write_text("content")

        mock_drive = MagicMock()
        # Mock empty remote folder
        mock_drive.files().list().execute.return_value = {"files": []}

        result = sync_folder(mock_drive, tmp_path, "folder_id", dry_run=True)

        assert "reports" in result
        assert isinstance(result["reports"], list)
        assert len(result["reports"]) == 1  # One new file

    def test_sync_folder_dry_run_report_has_reason(self, tmp_path: Path) -> None:
        """sync_folder dry_run reports should include reason."""
        from mygooglib.services.drive import sync_folder

        (tmp_path / "file.txt").write_text("test")

        mock_drive = MagicMock()
        mock_drive.files().list().execute.return_value = {"files": []}

        result = sync_folder(mock_drive, tmp_path, "folder_id", dry_run=True)

        report = result["reports"][0]
        assert report["action"] == "drive.upload"
        assert "reason" in report
        assert "not found" in report["reason"].lower()

    def test_sync_folder_dry_run_no_api_modify(self, tmp_path: Path) -> None:
        """sync_folder with dry_run=True should not upload/update files."""
        from mygooglib.services.drive import sync_folder

        (tmp_path / "file.txt").write_text("content")

        mock_drive = MagicMock()
        mock_drive.files().list().execute.return_value = {"files": []}

        sync_folder(mock_drive, tmp_path, "folder_id", dry_run=True)

        # Should not call create (upload) for files
        # Note: files().list() is called to check existing files
        mock_drive.files().create.assert_not_called()
