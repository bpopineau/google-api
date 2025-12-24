"""Tests for mygooglib.core.types TypedDict schemas.

These tests verify that the TypedDict schemas are correctly defined
and can be used for static type checking with mypy.
"""

from __future__ import annotations

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
from tests.factories.common import ColorFactory, DateFactory
from tests.factories.gmail import MessageFactory, ThreadFactory
from tests.factories.sheets import SpreadsheetFactory, ValueRangeFactory


class TestSharedTypes:
    """Test shared/common type definitions."""

    def test_color_dict_valid(self) -> None:
        """ColorDict accepts valid RGB color values."""
        color: ColorDict = ColorFactory.build(red=1.0, green=0.5, blue=0.0)
        assert color["red"] == 1.0
        assert color["green"] == 0.5
        assert color["blue"] == 0.0

    def test_color_dict_with_alpha(self) -> None:
        """ColorDict accepts optional alpha channel."""
        color: ColorDict = ColorFactory.build(red=0.0, green=0.0, blue=0.0, alpha=0.5)
        assert color.get("alpha") == 0.5

    def test_color_dict_empty(self) -> None:
        """ColorDict can be empty (total=False)."""
        color: ColorDict = {}
        assert len(color) == 0

    def test_date_dict_valid(self) -> None:
        """DateDict accepts valid date components."""
        date: DateDict = DateFactory.build(year=2025, month=12, day=22)
        assert date["year"] == 2025
        assert date["month"] == 12
        assert date["day"] == 22


class TestSheetsTypes:
    """Test Sheets API type definitions."""

    def test_spreadsheet_dict(self) -> None:
        """SpreadsheetDict represents a full spreadsheet."""
        spreadsheet: SpreadsheetDict = SpreadsheetFactory.build(
            spreadsheetId="abc123xyz",
            properties={"title": "Test Sheet"},
            sheets=[{"properties": {"sheetId": 0, "title": "Sheet1"}}],
        )
        assert spreadsheet["spreadsheetId"] == "abc123xyz"
        assert len(spreadsheet["sheets"]) == 1

    def test_value_range_dict(self) -> None:
        """ValueRangeDict contains cell values."""
        value_range: ValueRangeDict = ValueRangeFactory.build(
            range="Sheet1!A1:C3",
            majorDimension="ROWS",
            values=[
                ["Header1", "Header2", "Header3"],
                ["Value1", "Value2", 123],
                ["Value4", True, None],
            ],
        )
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

    def test_message_dict(self) -> None:
        """MessageDict represents a Gmail message."""
        message: MessageDict = MessageFactory.build(
            id="msg123",
            threadId="thread456",
            labelIds=["INBOX", "UNREAD"],
            snippet="This is a test message...",
            sizeEstimate=5000,
        )
        assert message["id"] == "msg123"
        assert "UNREAD" in message["labelIds"]

    def test_thread_dict(self) -> None:
        """ThreadDict represents a Gmail thread."""
        thread: ThreadDict = ThreadFactory.build(
            id="thread123",
            snippet="Re: Meeting tomorrow...",
            messages=[
                {"id": "msg1", "threadId": "thread123", "snippet": "Original message"},
                {"id": "msg2", "threadId": "thread123", "snippet": "Reply message"},
            ],
        )
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
