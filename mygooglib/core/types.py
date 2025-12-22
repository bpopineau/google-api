"""Type definitions for Google API responses.

This module provides TypedDict schemas for Sheets and Gmail API responses,
enabling strict typing while maintaining zero runtime overhead.

All TypedDicts use total=False since Google API responses often omit optional fields.
"""

from __future__ import annotations

from typing import Any, TypedDict

# =============================================================================
# Shared / Common Types
# =============================================================================


class ColorDict(TypedDict, total=False):
    """RGB color representation used in Sheets and other Google APIs.

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#Color
    """

    red: float
    green: float
    blue: float
    alpha: float


class DateDict(TypedDict, total=False):
    """A whole calendar date.

    https://developers.google.com/protocol-buffers/docs/reference/java/com/google/type/Date
    """

    year: int
    month: int
    day: int


# =============================================================================
# Sheets API Types
# =============================================================================


class GridRangeDict(TypedDict, total=False):
    """A range on a sheet. All indexes are zero-based.

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#GridRange
    """

    sheetId: int
    startRowIndex: int
    endRowIndex: int
    startColumnIndex: int
    endColumnIndex: int


class GridPropertiesDict(TypedDict, total=False):
    """Properties of a grid.

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets#GridProperties
    """

    rowCount: int
    columnCount: int
    frozenRowCount: int
    frozenColumnCount: int
    hideGridlines: bool
    rowGroupControlAfter: bool
    columnGroupControlAfter: bool


class SheetPropertiesDict(TypedDict, total=False):
    """Properties of a sheet.

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets#SheetProperties
    """

    sheetId: int
    title: str
    index: int
    sheetType: str
    gridProperties: GridPropertiesDict
    hidden: bool
    tabColor: ColorDict
    tabColorStyle: dict[str, Any]
    rightToLeft: bool
    dataSourceSheetProperties: dict[str, Any]


class SheetDict(TypedDict, total=False):
    """A single sheet within a spreadsheet.

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets#Sheet
    """

    properties: SheetPropertiesDict
    data: list[dict[str, Any]]
    merges: list[GridRangeDict]
    conditionalFormats: list[dict[str, Any]]
    filterViews: list[dict[str, Any]]
    protectedRanges: list[dict[str, Any]]
    basicFilter: dict[str, Any]
    charts: list[dict[str, Any]]
    bandedRanges: list[dict[str, Any]]
    developerMetadata: list[dict[str, Any]]
    rowData: list[dict[str, Any]]
    columnGroups: list[dict[str, Any]]
    rowGroups: list[dict[str, Any]]
    slicers: list[dict[str, Any]]


class SpreadsheetPropertiesDict(TypedDict, total=False):
    """Properties of a spreadsheet.

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#SpreadsheetProperties
    """

    title: str
    locale: str
    autoRecalc: str
    timeZone: str
    defaultFormat: dict[str, Any]
    iterativeCalculationSettings: dict[str, Any]
    spreadsheetTheme: dict[str, Any]


class SpreadsheetDict(TypedDict, total=False):
    """Represents a spreadsheet document.

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#Spreadsheet
    """

    spreadsheetId: str
    properties: SpreadsheetPropertiesDict
    sheets: list[SheetDict]
    namedRanges: list[dict[str, Any]]
    spreadsheetUrl: str
    developerMetadata: list[dict[str, Any]]
    dataSources: list[dict[str, Any]]
    dataSourceSchedules: list[dict[str, Any]]


class ValueRangeDict(TypedDict, total=False):
    """Data within a range of a spreadsheet.

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values#ValueRange
    """

    range: str
    majorDimension: str
    values: list[list[Any]]


class UpdateValuesResponseDict(TypedDict, total=False):
    """The response when updating a range of values in a spreadsheet.

    https://developers.google.com/sheets/api/reference/rest/v4/UpdateValuesResponse
    """

    spreadsheetId: str
    updatedRange: str
    updatedRows: int
    updatedColumns: int
    updatedCells: int
    updatedData: ValueRangeDict


class AppendValuesResponseDict(TypedDict, total=False):
    """The response when appending values.

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append#response-body
    """

    spreadsheetId: str
    tableRange: str
    updates: UpdateValuesResponseDict


class BatchGetValuesResponseDict(TypedDict, total=False):
    """The response when getting multiple ranges of values.

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchGet#response-body
    """

    spreadsheetId: str
    valueRanges: list[ValueRangeDict]


class BatchUpdateValuesResponseDict(TypedDict, total=False):
    """The response when updating multiple ranges of values.

    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchUpdate#response-body
    """

    spreadsheetId: str
    totalUpdatedRows: int
    totalUpdatedColumns: int
    totalUpdatedCells: int
    totalUpdatedSheets: int
    responses: list[UpdateValuesResponseDict]


class SheetInfoDict(TypedDict, total=False):
    """Simplified sheet metadata returned by get_sheets.

    This is a library-specific type representing the normalized format
    returned by the get_sheets function (not a raw API type).
    """

    title: str
    id: int
    index: int
    type: str


# =============================================================================
# Gmail API Types
# =============================================================================


class LabelDict(TypedDict, total=False):
    """A Gmail label.

    https://developers.google.com/gmail/api/reference/rest/v1/users.labels#Label
    """

    id: str
    name: str
    messageListVisibility: str
    labelListVisibility: str
    type: str
    messagesTotal: int
    messagesUnread: int
    threadsTotal: int
    threadsUnread: int
    color: dict[str, str]


class MessagePartBodyDict(TypedDict, total=False):
    """The body of a single MIME message part.

    https://developers.google.com/gmail/api/reference/rest/v1/users.messages#MessagePartBody
    """

    attachmentId: str
    size: int
    data: str


class HeaderDict(TypedDict, total=False):
    """A single header key-value pair."""

    name: str
    value: str


class MessagePartDict(TypedDict, total=False):
    """A single MIME message part.

    https://developers.google.com/gmail/api/reference/rest/v1/users.messages#MessagePart
    """

    partId: str
    mimeType: str
    filename: str
    headers: list[HeaderDict]
    body: MessagePartBodyDict
    parts: list["MessagePartDict"]


class MessageDict(TypedDict, total=False):
    """A Gmail message.

    https://developers.google.com/gmail/api/reference/rest/v1/users.messages#Message
    """

    id: str
    threadId: str
    labelIds: list[str]
    snippet: str
    historyId: str
    internalDate: str
    payload: MessagePartDict
    sizeEstimate: int
    raw: str


class MessageMetadataDict(TypedDict, total=False):
    """Simplified message metadata returned by search_messages.

    This is a library-specific type representing the normalized format
    returned by the search_messages function (not a raw API type).
    """

    id: str
    threadId: str
    subject: str
    from_: str  # 'from' is a reserved word
    to: str
    date: str
    snippet: str
    labelIds: list[str]
    hasAttachment: bool
    isUnread: bool


class MessageFullDict(TypedDict, total=False):
    """Full message details returned by get_message.

    This is a library-specific type representing the normalized format
    returned by the get_message function (not a raw API type).
    """

    id: str
    threadId: str
    subject: str
    from_: str
    to: str
    date: str
    snippet: str
    body: str
    labelIds: list[str]
    attachments: list["AttachmentMetadataDict"]


class AttachmentMetadataDict(TypedDict, total=False):
    """Attachment metadata extracted from a message.

    This is a library-specific type (not a raw API type).
    """

    filename: str
    attachment_id: str
    mime_type: str
    size: int


class ThreadDict(TypedDict, total=False):
    """A Gmail thread (collection of related messages).

    https://developers.google.com/gmail/api/reference/rest/v1/users.threads#Thread
    """

    id: str
    snippet: str
    historyId: str
    messages: list[MessageDict]


class SendMessageResponseDict(TypedDict, total=False):
    """Response from sending a message.

    https://developers.google.com/gmail/api/reference/rest/v1/users.messages/send#response-body
    """

    id: str
    threadId: str
    labelIds: list[str]


# =============================================================================
# Type Aliases for Common Patterns
# =============================================================================

# Sheets
CellValue = str | int | float | bool | None
RowData = list[CellValue]
RangeData = list[RowData]


# =============================================================================
# Dry Run Types
# =============================================================================


class DryRunReport(TypedDict, total=False):
    """Report returned when an operation is run with dry_run=True.

    This provides a structured preview of what the operation would do
    without actually performing it.

    Attributes:
        action: Operation identifier (e.g., "drive.delete", "sheets.update").
        resource_id: The ID or name of the affected resource.
        details: Dictionary of proposed changes. Contents vary by operation:
            - drive.delete: {"file_name": "...", "permanent": bool}
            - drive.upload: {"local_path": "...", "parent_id": "...", "name": "..."}
            - drive.create_folder: {"name": "...", "parent_id": "..."}
            - sheets.update: {"range": "...", "values_preview": [...], "total_cells": int}
            - sheets.append: {"range": "...", "row_count": int}
        reason: Optional explanation (useful for sync operations).
    """

    action: str
    resource_id: str
    details: dict[str, Any]
    reason: str
