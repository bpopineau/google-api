"""
Google Sheets API wrapper.

Provides a Pythonic interface for spreadsheet operations.
"""

from typing import Any

from goog.auth import GoogleAuth
from goog.utils import logger, with_retry


class SheetsClient:
    """
    Pythonic wrapper for Google Sheets API.

    Provides intuitive methods for spreadsheet operations through
    Spreadsheet and Worksheet objects.

    Example:
        >>> from goog import GoogleAuth, SheetsClient
        >>> auth = GoogleAuth()
        >>> sheets = SheetsClient(auth)
        >>> spreadsheet = sheets.open_by_id("spreadsheet_id")
        >>> ws = spreadsheet.sheets[0]
        >>> print(ws.get_value(1, 1))  # Get A1
    """

    def __init__(self, auth: GoogleAuth):
        """
        Initialize the Sheets client.

        Args:
            auth: GoogleAuth instance for authentication.
        """
        self._auth = auth
        self._service = None

    @property
    def service(self):
        """Lazily initialize and return the Sheets service."""
        if self._service is None:
            self._service = self._auth.build_service("sheets", "v4")
        return self._service

    @with_retry()
    def open_by_id(self, spreadsheet_id: str) -> "Spreadsheet":
        """
        Open a spreadsheet by its ID.

        Args:
            spreadsheet_id: The ID from the spreadsheet URL.

        Returns:
            A Spreadsheet object.

        Example:
            >>> ss = sheets.open_by_id("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")
            >>> print(ss.title)
        """
        logger.info(f"Opening spreadsheet: {spreadsheet_id}")
        metadata = (
            self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        )
        return Spreadsheet(self, spreadsheet_id, metadata)

    @with_retry()
    def create(self, title: str) -> "Spreadsheet":
        """
        Create a new spreadsheet.

        Args:
            title: Title for the new spreadsheet.

        Returns:
            A Spreadsheet object for the new spreadsheet.

        Example:
            >>> ss = sheets.create("My New Spreadsheet")
            >>> print(ss.id)
        """
        logger.info(f"Creating spreadsheet: {title}")
        body = {"properties": {"title": title}}
        result = self.service.spreadsheets().create(body=body).execute()
        return Spreadsheet(self, result["spreadsheetId"], result)


class Spreadsheet:
    """
    Represents a Google Spreadsheet.

    Provides access to individual worksheets (sheets) and spreadsheet metadata.
    """

    def __init__(
        self,
        client: SheetsClient,
        spreadsheet_id: str,
        metadata: dict,
    ):
        """
        Initialize a Spreadsheet object.

        Args:
            client: The SheetsClient that created this spreadsheet.
            spreadsheet_id: The spreadsheet ID.
            metadata: The spreadsheet metadata from the API.
        """
        self._client = client
        self._id = spreadsheet_id
        self._metadata = metadata
        self._worksheets: list[Worksheet] | None = None

    @property
    def id(self) -> str:
        """The spreadsheet ID."""
        return self._id

    @property
    def title(self) -> str:
        """The spreadsheet title."""
        return self._metadata.get("properties", {}).get("title", "")

    @property
    def sheets(self) -> list["Worksheet"]:
        """
        List of all worksheets in this spreadsheet.

        Returns:
            List of Worksheet objects.
        """
        if self._worksheets is None:
            self._worksheets = []
            for sheet_data in self._metadata.get("sheets", []):
                props = sheet_data.get("properties", {})
                ws = Worksheet(
                    self._client,
                    self._id,
                    props.get("sheetId"),
                    props.get("title", ""),
                )
                self._worksheets.append(ws)
        return self._worksheets

    @property
    def sheet_titles(self) -> list[str]:
        """List of all worksheet titles."""
        return [ws.title for ws in self.sheets]

    def __getitem__(self, key: str | int) -> "Worksheet":
        """
        Get a worksheet by title or index.

        Args:
            key: Worksheet title (str) or index (int).

        Returns:
            The Worksheet object.

        Example:
            >>> ws = spreadsheet["Sheet1"]  # by title
            >>> ws = spreadsheet[0]  # by index
        """
        if isinstance(key, int):
            return self.sheets[key]

        for ws in self.sheets:
            if ws.title == key:
                return ws

        raise KeyError(f"Worksheet not found: {key}")


class Worksheet:
    """
    Represents a single worksheet (tab) in a spreadsheet.

    Provides intuitive methods for reading and writing cell data.
    """

    def __init__(
        self,
        client: SheetsClient,
        spreadsheet_id: str,
        sheet_id: int,
        title: str,
    ):
        """
        Initialize a Worksheet object.

        Args:
            client: The SheetsClient for API calls.
            spreadsheet_id: The parent spreadsheet ID.
            sheet_id: The numeric sheet ID.
            title: The worksheet title.
        """
        self._client = client
        self._spreadsheet_id = spreadsheet_id
        self._sheet_id = sheet_id
        self._title = title

    @property
    def title(self) -> str:
        """The worksheet title."""
        return self._title

    @property
    def sheet_id(self) -> int:
        """The numeric sheet ID."""
        return self._sheet_id

    def _col_to_letter(self, col: int) -> str:
        """Convert 1-indexed column number to letter (1='A', 27='AA')."""
        result = ""
        while col > 0:
            col, remainder = divmod(col - 1, 26)
            result = chr(65 + remainder) + result
        return result

    def _range_notation(
        self,
        start_row: int,
        start_col: int,
        end_row: int | None = None,
        end_col: int | None = None,
    ) -> str:
        """Build A1 notation range string."""
        start = f"{self._col_to_letter(start_col)}{start_row}"
        if end_row is None and end_col is None:
            return f"'{self._title}'!{start}"
        end = f"{self._col_to_letter(end_col or start_col)}{end_row or start_row}"
        return f"'{self._title}'!{start}:{end}"

    @with_retry()
    def get_value(self, row: int, col: int) -> Any:
        """
        Get the value at a specific cell.

        Args:
            row: Row number (1-indexed).
            col: Column number (1-indexed).

        Returns:
            The cell value, or None if empty.

        Example:
            >>> value = ws.get_value(1, 1)  # Get A1
        """
        range_notation = self._range_notation(row, col)
        result = (
            self._client.service.spreadsheets()
            .values()
            .get(spreadsheetId=self._spreadsheet_id, range=range_notation)
            .execute()
        )
        values = result.get("values", [[]])
        return values[0][0] if values and values[0] else None

    @with_retry()
    def update_value(
        self,
        row: int,
        col: int,
        value: Any,
        value_input_option: str = "USER_ENTERED",
    ) -> None:
        """
        Update a single cell.

        Args:
            row: Row number (1-indexed).
            col: Column number (1-indexed).
            value: The value to set.
            value_input_option: How to interpret the value.
                               "USER_ENTERED" (default) or "RAW".

        Example:
            >>> ws.update_value(1, 1, "Hello")  # Set A1
            >>> ws.update_value(2, 1, 42)  # Set A2
        """
        range_notation = self._range_notation(row, col)
        body = {"values": [[value]]}
        logger.debug(f"Updating {range_notation} to {value}")
        self._client.service.spreadsheets().values().update(
            spreadsheetId=self._spreadsheet_id,
            range=range_notation,
            valueInputOption=value_input_option,
            body=body,
        ).execute()

    @with_retry()
    def get_row(self, row: int) -> list[Any]:
        """
        Get all values in a row.

        Args:
            row: Row number (1-indexed).

        Returns:
            List of values in the row.

        Example:
            >>> headers = ws.get_row(1)
        """
        range_notation = f"'{self._title}'!{row}:{row}"
        result = (
            self._client.service.spreadsheets()
            .values()
            .get(spreadsheetId=self._spreadsheet_id, range=range_notation)
            .execute()
        )
        values = result.get("values", [[]])
        return values[0] if values else []

    @with_retry()
    def get_column(self, col: int) -> list[Any]:
        """
        Get all values in a column.

        Args:
            col: Column number (1-indexed).

        Returns:
            List of values in the column.

        Example:
            >>> amounts = ws.get_column(2)  # Get column B
        """
        col_letter = self._col_to_letter(col)
        range_notation = f"'{self._title}'!{col_letter}:{col_letter}"
        result = (
            self._client.service.spreadsheets()
            .values()
            .get(
                spreadsheetId=self._spreadsheet_id,
                range=range_notation,
                majorDimension="COLUMNS",
            )
            .execute()
        )
        values = result.get("values", [[]])
        return values[0] if values else []

    @with_retry()
    def append_row(
        self,
        values: list[Any],
        value_input_option: str = "USER_ENTERED",
    ) -> None:
        """
        Append a row at the bottom of the sheet.

        Args:
            values: List of values for the new row.
            value_input_option: How to interpret values.

        Example:
            >>> ws.append_row(["2024-01-15", 100, "Groceries"])
        """
        range_notation = f"'{self._title}'!A:A"
        body = {"values": [values]}
        logger.debug(f"Appending row with {len(values)} values")
        self._client.service.spreadsheets().values().append(
            spreadsheetId=self._spreadsheet_id,
            range=range_notation,
            valueInputOption=value_input_option,
            insertDataOption="INSERT_ROWS",
            body=body,
        ).execute()

    @with_retry()
    def get_all_values(self) -> list[list[Any]]:
        """
        Get all values in the worksheet.

        Returns:
            2D list of all cell values.

        Example:
            >>> all_data = ws.get_all_values()
            >>> for row in all_data:
            ...     print(row)
        """
        result = (
            self._client.service.spreadsheets()
            .values()
            .get(spreadsheetId=self._spreadsheet_id, range=self._title)
            .execute()
        )
        return result.get("values", [])

    @with_retry()
    def update_range(
        self,
        start_row: int,
        start_col: int,
        values: list[list[Any]],
        value_input_option: str = "USER_ENTERED",
    ) -> None:
        """
        Update a range of cells.

        Args:
            start_row: Starting row (1-indexed).
            start_col: Starting column (1-indexed).
            values: 2D list of values to write.
            value_input_option: How to interpret values.

        Example:
            >>> ws.update_range(1, 1, [["A1", "B1"], ["A2", "B2"]])
        """
        if not values or not values[0]:
            return

        end_row = start_row + len(values) - 1
        end_col = start_col + len(values[0]) - 1
        range_notation = self._range_notation(start_row, start_col, end_row, end_col)

        body = {"values": values}
        logger.debug(f"Updating range {range_notation}")
        self._client.service.spreadsheets().values().update(
            spreadsheetId=self._spreadsheet_id,
            range=range_notation,
            valueInputOption=value_input_option,
            body=body,
        ).execute()

    @with_retry()
    def clear(self) -> None:
        """
        Clear all values in the worksheet.

        Example:
            >>> ws.clear()
        """
        logger.info(f"Clearing worksheet: {self._title}")
        self._client.service.spreadsheets().values().clear(
            spreadsheetId=self._spreadsheet_id,
            range=self._title,
            body={},
        ).execute()
