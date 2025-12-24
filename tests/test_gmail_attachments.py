"""Tests for Gmail attachment functions."""

import base64
from unittest.mock import MagicMock, patch

import pytest

from mygooglib.services.gmail import (
    _extract_attachments,
    get_attachment,
    save_attachments,
)
from tests.factories.gmail import MessagePartFactory, MessageFactory


@pytest.fixture
def mock_gmail():
    """Create a mock Gmail service."""
    return MagicMock()


def test_get_attachment_returns_bytes(mock_gmail):
    """Test that get_attachment decodes base64 data correctly."""
    # Create mock attachment data
    original_data = b"Hello, World! This is test attachment content."
    encoded_data = base64.urlsafe_b64encode(original_data).decode("utf-8")

    # Mock the API response
    mock_response = {"data": encoded_data, "size": len(original_data)}
    mock_gmail.users.return_value.messages.return_value.attachments.return_value.get.return_value.execute.return_value = mock_response

    # Call the function
    with patch(
        "mygooglib.services.gmail.execute_with_retry_http_error",
        return_value=mock_response,
    ):
        result = get_attachment(mock_gmail, "msg123", "att456")

    assert result == original_data
    assert isinstance(result, bytes)


def test_extract_attachments_finds_parts():
    """Test that _extract_attachments correctly extracts attachment metadata."""
    payload = {
        "parts": [
            {"filename": "", "mimeType": "text/plain", "body": {"data": "dGVzdA=="}},
            {
                "filename": "report.pdf",
                "mimeType": "application/pdf",
                "body": {"attachmentId": "att123", "size": 1024},
            },
            {
                "filename": "image.png",
                "mimeType": "image/png",
                "body": {"attachmentId": "att456", "size": 2048},
            },
        ]
    }

    result = _extract_attachments(payload)

    assert len(result) == 2
    assert result[0]["filename"] == "report.pdf"
    assert result[0]["attachment_id"] == "att123"
    assert result[1]["filename"] == "image.png"


@patch("mygooglib.services.gmail.get_attachment")
@patch("mygooglib.services.gmail.search_messages")
@patch("mygooglib.services.gmail.execute_with_retry_http_error")
def test_save_attachments_creates_files(
    mock_execute, mock_search, mock_get_att, mock_gmail, tmp_path
):
    """Test that save_attachments downloads and saves files."""
    # Mock search results
    mock_search.return_value = [{"id": "msg123"}]

    # Mock full message with attachment
    payload = {
        "parts": [
            {
                "filename": "test.txt",
                "mimeType": "text/plain",
                "body": {"attachmentId": "att789", "size": 100},
            }
        ]
    }
    msg = MessageFactory.build(id="msg123")
    msg["payload"] = payload
    mock_execute.return_value = msg

    # Mock attachment download
    mock_get_att.return_value = b"File content here"

    # Call save_attachments
    result = save_attachments(mock_gmail, "has:attachment", tmp_path)

    assert len(result) == 1
    assert result[0].name == "test.txt"
    assert result[0].exists()
    assert result[0].read_bytes() == b"File content here"


@patch("mygooglib.services.gmail.get_attachment")
@patch("mygooglib.services.gmail.search_messages")
@patch("mygooglib.services.gmail.execute_with_retry_http_error")
def test_save_attachments_applies_filter(
    mock_execute, mock_search, mock_get_att, mock_gmail, tmp_path
):
    """Test that filename_filter works correctly."""
    mock_search.return_value = [{"id": "msg123"}]

    payload = {
        "parts": [
            {
                "filename": "invoice.pdf",
                "mimeType": "application/pdf",
                "body": {"attachmentId": "att1", "size": 100},
            },
            {
                "filename": "image.png",
                "mimeType": "image/png",
                "body": {"attachmentId": "att2", "size": 200},
            },
        ]
    }
    msg = MessageFactory.build(id="msg123")
    msg["payload"] = payload
    mock_execute.return_value = msg

    mock_get_att.return_value = b"PDF content"
    # Filter to only PDFs
    result = save_attachments(
        mock_gmail, "has:attachment", tmp_path, filename_filter="pdf"
    )

    assert len(result) == 1
    assert result[0].name == "invoice.pdf"
