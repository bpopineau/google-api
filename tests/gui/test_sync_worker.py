"""Tests for SyncWorker."""

from unittest.mock import MagicMock, patch
import pytest
from mygoog_gui.workers import SyncWorker

@pytest.fixture
def mock_clients():
    clients = MagicMock()
    clients.sheets = MagicMock()
    # Default to spreadsheet existing
    clients.sheets.exists.return_value = True
    return clients

def test_sync_worker_success(qtbot, mock_clients, tmp_path):
    # Create some dummy files
    (tmp_path / "file1.txt").write_text("hello")
    (tmp_path / "file2.txt").write_text("world")
    
    # Use a long enough ID
    spreadsheet_id = "a" * 44
    worker = SyncWorker(mock_clients, str(tmp_path), spreadsheet_id, "Sheet1")
    
    mock_clients.sheets.batch_write.return_value = {"updatedRows": 3} # Headers + 2 files
    
    with qtbot.waitSignals([worker.started_scan, worker.started_upload, worker.finished], timeout=5000):
        worker.start()
            
    mock_clients.sheets.batch_write.assert_called_once()
    args, kwargs = mock_clients.sheets.batch_write.call_args
    assert args[0] == spreadsheet_id
    assert args[1] == "Sheet1"
    assert len(args[2]) == 2 # 2 rows of data

def test_sync_worker_empty_dir(qtbot, mock_clients, tmp_path):
    spreadsheet_id = "a" * 44
    worker = SyncWorker(mock_clients, str(tmp_path), spreadsheet_id, "Sheet1")
    
    with qtbot.waitSignal(worker.finished) as blocker:
        worker.start()
        
    assert blocker.args[0]["updatedRows"] == 0

def test_sync_worker_error(qtbot, mock_clients, tmp_path):
    spreadsheet_id = "a" * 44
    worker = SyncWorker(mock_clients, str(tmp_path), spreadsheet_id, "Sheet1")
    
    # Patch FileScanner.scan to fail
    with patch("mygooglib.core.utils.file_scanner.FileScanner.scan", side_effect=Exception("Scan failed")):
        with qtbot.waitSignal(worker.error, timeout=5000) as blocker:
            worker.start()
            
    assert "Scan failed" in blocker.args[0]


