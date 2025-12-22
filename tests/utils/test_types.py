"""Tests for mygooglib.core.types TypedDict schemas.

These tests verify that the TypedDict schemas are correctly defined
and can be used for static type checking with mypy.
"""

from __future__ import annotations

import pytest

from mygooglib.core.types import (
    AppendValuesResponseDict,
    AttachmentMetadataDict,
    BatchGetValuesResponseDict,
    BatchUpdateValuesResponseDict,
    # Type aliases
    CellValue,
    # Shared types
    ColorDict,
    DateDict,
    GridPropertiesDict,
    # Sheets types
    GridRangeDict,
    HeaderDict,
    # Gmail types
    LabelDict,
    MessageDict,
    MessageFullDict,
    MessageMetadataDict,
    MessagePartBodyDict,
    MessagePartDict,
    RangeData,
    RowData,
    SendMessageResponseDict,
    SheetDict,
    SheetPropertiesDict,
    SpreadsheetDict,
    SpreadsheetPropertiesDict,
    ThreadDict,
    UpdateValuesResponseDict,
    ValueRangeDict,
)


class TestSharedTypes:
    """Test shared/common type definitions."""

    def test_color_dict_valid(self) -> None:
        """ColorDict accepts valid RGB color values."""
        color: ColorDict = {"red": 1.0, "green": 0.5, "blue": 0.0}
        assert color["red"] == 1.0
        assert color["green"] == 0.5
        assert color["blue"] == 0.0

    def test_color_dict_with_alpha(self) -> None:
        """ColorDict accepts optional alpha channel."""
        color: ColorDict = {"red": 0.0, "green": 0.0, "blue": 0.0, "alpha": 0.5}
        assert color.get("alpha") == 0.5

    def test_color_dict_empty(self) -> None:
        """ColorDict can be empty (total=False)."""
        color: ColorDict = {}
        assert len(color) == 0

    def test_date_dict_valid(self) -> None:
        """DateDict accepts valid date components."""
        date: DateDict = {"year": 2025, "month": 12, "day": 22}
        assert date["year"] == 2025
        assert date["month"] == 12
        assert date["day"] == 22

    def test_date_dict_partial(self) -> None:
        """DateDict can have partial data (e.g., year only)."""
        date: DateDict = {"year": 2025}
        assert date["year"] == 2025
        assert date.get("month") is None


class TestSheetsTypes:
    """Test Sheets API type definitions."""

    def test_grid_range_dict(self) -> None:
        """GridRangeDict represents a cell range."""
        range_: GridRangeDict = {
            "sheetId": 0,
            "startRowIndex": 0,
            "endRowIndex": 10,
            "startColumnIndex": 0,
            "endColumnIndex": 5,
        }
        assert range_["sheetId"] == 0
        assert range_["endRowIndex"] == 10

    def test_grid_properties_dict(self) -> None:
        """GridPropertiesDict contains grid metadata."""
        props: GridPropertiesDict = {
            "rowCount": 1000,
            "columnCount": 26,
            "frozenRowCount": 1,
        }
        assert props["rowCount"] == 1000
        assert props["frozenRowCount"] == 1

    def test_sheet_properties_dict(self) -> None:
        """SheetPropertiesDict contains sheet metadata."""
        props: SheetPropertiesDict = {
            "sheetId": 0,
            "title": "Sheet1",
            "index": 0,
            "sheetType": "GRID",
            "gridProperties": {"rowCount": 1000, "columnCount": 26},
        }
        assert props["title"] == "Sheet1"
        assert props["gridProperties"]["rowCount"] == 1000

    def test_sheet_dict(self) -> None:
        """SheetDict represents a full sheet."""
        sheet: SheetDict = {
            "properties": {"sheetId": 0, "title": "Data"},
        }
        assert sheet["properties"]["title"] == "Data"

    def test_spreadsheet_properties_dict(self) -> None:
        """SpreadsheetPropertiesDict contains spreadsheet-level properties."""
        props: SpreadsheetPropertiesDict = {
            "title": "My Spreadsheet",
            "locale": "en_US",
            "timeZone": "America/Los_Angeles",
        }
        assert props["title"] == "My Spreadsheet"

    def test_spreadsheet_dict(self) -> None:
        """SpreadsheetDict represents a full spreadsheet."""
        spreadsheet: SpreadsheetDict = {
            "spreadsheetId": "abc123xyz",
            "properties": {"title": "Test Sheet"},
            "sheets": [{"properties": {"sheetId": 0, "title": "Sheet1"}}],
            "spreadsheetUrl": "https://docs.google.com/spreadsheets/d/abc123xyz",
        }
        assert spreadsheet["spreadsheetId"] == "abc123xyz"
        assert len(spreadsheet["sheets"]) == 1

    def test_value_range_dict(self) -> None:
        """ValueRangeDict contains cell values."""
        value_range: ValueRangeDict = {
            "range": "Sheet1!A1:C3",
            "majorDimension": "ROWS",
            "values": [
                ["Header1", "Header2", "Header3"],
                ["Value1", "Value2", 123],
                ["Value4", True, None],
            ],
        }
        assert value_range["range"] == "Sheet1!A1:C3"
        assert len(value_range["values"]) == 3

    def test_update_values_response_dict(self) -> None:
        """UpdateValuesResponseDict captures update results."""
        response: UpdateValuesResponseDict = {
            "spreadsheetId": "abc123",
            "updatedRange": "Sheet1!A1:C3",
            "updatedRows": 3,
            "updatedColumns": 3,
            "updatedCells": 9,
        }
        assert response["updatedCells"] == 9

    def test_append_values_response_dict(self) -> None:
        """AppendValuesResponseDict captures append results."""
        response: AppendValuesResponseDict = {
            "spreadsheetId": "abc123",
            "tableRange": "Sheet1!A1:C10",
            "updates": {
                "spreadsheetId": "abc123",
                "updatedRange": "Sheet1!A11:C11",
                "updatedRows": 1,
                "updatedColumns": 3,
                "updatedCells": 3,
            },
        }
        assert response["updates"]["updatedRows"] == 1

    def test_batch_get_values_response_dict(self) -> None:
        """BatchGetValuesResponseDict for multiple range reads."""
        response: BatchGetValuesResponseDict = {
            "spreadsheetId": "abc123",
            "valueRanges": [
                {"range": "Sheet1!A1:A10", "values": [["a"], ["b"]]},
                {"range": "Sheet1!B1:B10", "values": [["x"], ["y"]]},
            ],
        }
        assert len(response["valueRanges"]) == 2

    def test_batch_update_values_response_dict(self) -> None:
        """BatchUpdateValuesResponseDict for multiple range updates."""
        response: BatchUpdateValuesResponseDict = {
            "spreadsheetId": "abc123",
            "totalUpdatedRows": 10,
            "totalUpdatedColumns": 5,
            "totalUpdatedCells": 50,
            "totalUpdatedSheets": 2,
        }
        assert response["totalUpdatedCells"] == 50


class TestGmailTypes:
    """Test Gmail API type definitions."""

    def test_label_dict(self) -> None:
        """LabelDict represents a Gmail label."""
        label: LabelDict = {
            "id": "INBOX",
            "name": "INBOX",
            "type": "system",
            "messagesTotal": 1000,
            "messagesUnread": 5,
        }
        assert label["id"] == "INBOX"
        assert label["messagesUnread"] == 5

    def test_message_part_body_dict(self) -> None:
        """MessagePartBodyDict contains body data."""
        body: MessagePartBodyDict = {
            "size": 1024,
            "data": "SGVsbG8gV29ybGQh",  # base64 "Hello World!"
        }
        assert body["size"] == 1024

    def test_header_dict(self) -> None:
        """HeaderDict is a simple key-value pair."""
        header: HeaderDict = {"name": "Subject", "value": "Test Email"}
        assert header["name"] == "Subject"

    def test_message_part_dict(self) -> None:
        """MessagePartDict represents a MIME part."""
        part: MessagePartDict = {
            "partId": "0",
            "mimeType": "text/plain",
            "filename": "",
            "headers": [{"name": "Content-Type", "value": "text/plain"}],
            "body": {"size": 100, "data": "dGVzdA=="},
        }
        assert part["mimeType"] == "text/plain"

    def test_message_dict(self) -> None:
        """MessageDict represents a Gmail message."""
        message: MessageDict = {
            "id": "msg123",
            "threadId": "thread456",
            "labelIds": ["INBOX", "UNREAD"],
            "snippet": "This is a test message...",
            "sizeEstimate": 5000,
        }
        assert message["id"] == "msg123"
        assert "UNREAD" in message["labelIds"]

    def test_message_metadata_dict(self) -> None:
        """MessageMetadataDict is the library's normalized format."""
        metadata: MessageMetadataDict = {
            "id": "msg123",
            "threadId": "thread456",
            "subject": "Test Subject",
            "from_": "sender@example.com",
            "to": "recipient@example.com",
            "date": "2025-12-22T12:00:00Z",
            "snippet": "Preview text...",
            "hasAttachment": True,
            "isUnread": False,
        }
        assert metadata["subject"] == "Test Subject"
        assert metadata["hasAttachment"] is True

    def test_message_full_dict(self) -> None:
        """MessageFullDict is the library's full message format."""
        full: MessageFullDict = {
            "id": "msg123",
            "threadId": "thread456",
            "subject": "Full Message Test",
            "from_": "sender@example.com",
            "to": "recipient@example.com",
            "date": "2025-12-22T12:00:00Z",
            "snippet": "Preview...",
            "body": "This is the full message body content.",
            "attachments": [
                {
                    "filename": "document.pdf",
                    "attachment_id": "att123",
                    "mime_type": "application/pdf",
                    "size": 102400,
                }
            ],
        }
        assert full["body"] == "This is the full message body content."
        assert len(full["attachments"]) == 1

    def test_attachment_metadata_dict(self) -> None:
        """AttachmentMetadataDict describes an attachment."""
        attachment: AttachmentMetadataDict = {
            "filename": "report.xlsx",
            "attachment_id": "att789",
            "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "size": 50000,
        }
        assert attachment["filename"] == "report.xlsx"

    def test_thread_dict(self) -> None:
        """ThreadDict represents a Gmail thread."""
        thread: ThreadDict = {
            "id": "thread123",
            "snippet": "Re: Meeting tomorrow...",
            "messages": [
                {"id": "msg1", "threadId": "thread123", "snippet": "Original message"},
                {"id": "msg2", "threadId": "thread123", "snippet": "Reply message"},
            ],
        }
        assert thread["id"] == "thread123"
        assert len(thread["messages"]) == 2

    def test_send_message_response_dict(self) -> None:
        """SendMessageResponseDict contains the sent message info."""
        response: SendMessageResponseDict = {
            "id": "msg789",
            "threadId": "thread789",
            "labelIds": ["SENT"],
        }
        assert response["id"] == "msg789"


class TestTypeAliases:
    """Test type alias definitions."""

    def test_cell_value_types(self) -> None:
        """CellValue can be various primitive types."""
        values: list[CellValue] = ["text", 123, 45.67, True, None]
        assert len(values) == 5

    def test_row_data(self) -> None:
        """RowData is a list of cell values."""
        row: RowData = ["Name", 25, True]
        assert len(row) == 3

    def test_range_data(self) -> None:
        """RangeData is a 2D list of cell values."""
        data: RangeData = [
            ["Header1", "Header2"],
            ["Value1", 100],
            ["Value2", 200],
        ]
        assert len(data) == 3
        assert len(data[0]) == 2
