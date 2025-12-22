"""Sheets page - spreadsheet viewer/editor."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from mygoog_gui.styles import COLORS
from mygoog_gui.workers import ApiWorker

if TYPE_CHECKING:
    from mygooglib.core.client import Clients
    from mygoog_gui.widgets.activity import ActivityModel


class SheetsPage(QWidget):
    """Google Sheets browser."""

    def __init__(self, clients: "Clients", parent: QWidget | None = None, activity_model: ActivityModel | None = None) -> None:
        super().__init__(parent)
        self.clients = clients
        self.activity_model = activity_model
        self._workers: list[ApiWorker] = []
        self._current_sheet_id: str | None = None
        self._current_range: str | None = None
        self._data: list[list] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build the sheets page layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel("📊 Sheets")
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(header)

        # Input row
        input_row = QHBoxLayout()

        self.sheet_input = QLineEdit()
        self.sheet_input.setPlaceholderText("Spreadsheet ID or URL...")
        input_row.addWidget(self.sheet_input, stretch=2)

        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText("Range (e.g., Sheet1!A1:Z100)")
        self.range_input.setText("Sheet1!A1:Z100")
        input_row.addWidget(self.range_input, stretch=1)

        load_btn = QPushButton("📥 Load")
        load_btn.clicked.connect(self._on_load)
        input_row.addWidget(load_btn)

        layout.addLayout(input_row)

        # Data table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # Action row
        action_row = QHBoxLayout()

        export_btn = QPushButton("💾 Export CSV")
        export_btn.clicked.connect(self._on_export)
        action_row.addWidget(export_btn)

        action_row.addStretch()

        self.status = QLabel("Enter a spreadsheet ID and range to load data")
        self.status.setStyleSheet(f"color: {COLORS['text_secondary']};")
        action_row.addWidget(self.status)

        layout.addLayout(action_row)

    def _parse_sheet_id(self, input_text: str) -> str:
        """Extract sheet ID from URL or return as-is."""
        input_text = input_text.strip()
        if "/spreadsheets/d/" in input_text:
            # Extract ID from URL
            start = input_text.find("/spreadsheets/d/") + len("/spreadsheets/d/")
            end = input_text.find("/", start)
            if end == -1:
                end = len(input_text)
            return input_text[start:end]
        return input_text

    def _on_load(self) -> None:
        """Load data from the spreadsheet."""
        sheet_id = self._parse_sheet_id(self.sheet_input.text())
        range_name = self.range_input.text().strip()

        if not sheet_id:
            self.status.setText("Error: Please enter a spreadsheet ID")
            return

        if not range_name:
            self.status.setText("Error: Please enter a range")
            return

        self._current_sheet_id = sheet_id
        self._current_range = range_name
        self.status.setText("Loading...")

        def fetch():
            return self.clients.sheets.read(sheet_id, range_name)

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_data_loaded)
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_data_loaded(self, data: list[list]) -> None:
        """Handle loaded data."""
        self._data = data

        if not data:
            self.status.setText("No data found in range")
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        # Determine dimensions
        num_rows = len(data)
        num_cols = max(len(row) for row in data) if data else 0

        self.table.setRowCount(num_rows)
        self.table.setColumnCount(num_cols)

        # Set column headers (A, B, C, ...)
        headers = [
            chr(ord("A") + i) if i < 26 else f"Col{i + 1}" for i in range(num_cols)
        ]
        self.table.setHorizontalHeaderLabels(headers)

        # Populate data
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)

        self.status.setText(f"Loaded {num_rows} rows × {num_cols} columns")

    def _on_error(self, e: Exception) -> None:
        """Handle API error."""
        self.status.setText(f"Error: {e}")

    def _on_export(self) -> None:
        """Export data to CSV."""
        if not self._data:
            self.status.setText("No data to export")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export CSV",
            "export.csv",
            "CSV Files (*.csv)",
        )

        if not file_path:
            return

        try:
            import csv

            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(self._data)

            self.status.setText(f"Exported to {file_path}")
        except Exception as e:
            self.status.setText(f"Export error: {e}")

