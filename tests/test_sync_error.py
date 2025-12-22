"""Reproduction test for SyncWorker 404 error fix."""

from unittest.mock import MagicMock, patch
import pytest
from googleapiclient.errors import HttpError
from mygooglib.gui.workers import SyncWorker

@pytest.fixture
def mock_clients():
    clients = MagicMock()
    # Mock SheetsClient methods
    clients.sheets = MagicMock()
    return clients

def test_sync_worker_handles_missing_spreadsheet(qtbot, mock_clients, tmp_path):
    # Setup: Create a file to scan
    (tmp_path / "file1.txt").write_text("hello")
    
    spreadsheet_id = "deleted_id_12345"
    worker = SyncWorker(mock_clients, str(tmp_path), spreadsheet_id, "Sheet1")
    
    # 1. exists() returns False (spreadsheet missing)
    mock_clients.sheets.exists.return_value = False
    
    # 2. create_spreadsheet() returns a new ID
    new_id = "new_spreadsheet_id_67890"
    mock_clients.sheets.create_spreadsheet.return_value = new_id
    
    # 3. batch_write() succeeds
    mock_clients.sheets.batch_write.return_value = {"updatedRows": 2}
    
    with qtbot.waitSignal(worker.finished, timeout=5000) as blocker:
        worker.start()
            
    assert blocker.args[0]["updatedRows"] == 2
    mock_clients.sheets.exists.assert_called_once_with(spreadsheet_id)
    mock_clients.sheets.create_spreadsheet.assert_called_once()
    mock_clients.sheets.batch_write.assert_called_once()
    # Verify it used the new_id
    args, kwargs = mock_clients.sheets.batch_write.call_args
    assert args[0] == new_id
