"""Tests for SheetsClient.exists."""

from unittest.mock import MagicMock, patch
import pytest
from googleapiclient.errors import HttpError
from mygooglib.services.sheets import SheetsClient

@pytest.fixture
def mock_service():
    return MagicMock()

@pytest.fixture
def mock_drive():
    return MagicMock()

@pytest.fixture
def client(mock_service, mock_drive):
    return SheetsClient(mock_service, drive=mock_drive)

def test_exists_success(client, mock_service):
    # Setup
    spreadsheet_id = "some_valid_id"
    mock_service.spreadsheets.return_value.get.return_value.execute.return_value = {"spreadsheetId": spreadsheet_id}
    
    assert client.exists(spreadsheet_id) is True
    mock_service.spreadsheets.return_value.get.assert_called_with(
        spreadsheetId=spreadsheet_id, fields="spreadsheetId"
    )

def test_exists_not_found(client, mock_service):
    # Setup
    spreadsheet_id = "missing_id"
    resp = MagicMock()
    resp.status = 404
    error = HttpError(resp, b'{"error": {"message": "Not found"}}')
    mock_service.spreadsheets.return_value.get.return_value.execute.side_effect = error
    
    assert client.exists(spreadsheet_id) is False

def test_exists_with_title_resolution(client, mock_service, mock_drive):
    # Setup
    title = "My Sheet"
    spreadsheet_id = "resolved_id"
    
    # Mock resolve_spreadsheet (called by SheetsClient.exists via self.resolve_spreadsheet)
    with patch("mygooglib.services.sheets.resolve_spreadsheet", return_value=spreadsheet_id):
        mock_service.spreadsheets.return_value.get.return_value.execute.return_value = {"spreadsheetId": spreadsheet_id}
        
        assert client.exists(title) is True
        
def test_exists_resolution_fails(client, mock_service):
    # Setup
    title = "Unknown Sheet"
    
    with patch("mygooglib.services.sheets.resolve_spreadsheet", side_effect=ValueError("Not found")):
        assert client.exists(title) is False


