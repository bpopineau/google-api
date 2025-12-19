"""Calendar page - event list and quick add."""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDateTimeEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from mygooglib.gui.styles import COLORS
from mygooglib.gui.workers import ApiWorker

if TYPE_CHECKING:
    from mygooglib.client import Clients


class AddEventDialog(QDialog):
    """Dialog for adding a new calendar event."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Add Event")
        self.setMinimumWidth(400)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Event title")
        form.addRow("Title:", self.title_input)

        self.start_input = QDateTimeEdit()
        self.start_input.setDateTime(dt.datetime.now() + dt.timedelta(hours=1))
        self.start_input.setCalendarPopup(True)
        form.addRow("Start:", self.start_input)

        self.end_input = QDateTimeEdit()
        self.end_input.setDateTime(dt.datetime.now() + dt.timedelta(hours=2))
        self.end_input.setCalendarPopup(True)
        form.addRow("End:", self.end_input)

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Optional location")
        form.addRow("Location:", self.location_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_event_data(self) -> dict:
        """Return the event data."""
        return {
            "summary": self.title_input.text().strip(),
            "start": self.start_input.dateTime().toPython(),
            "end": self.end_input.dateTime().toPython(),
            "location": self.location_input.text().strip() or None,
        }


class CalendarPage(QWidget):
    """Google Calendar event viewer."""

    def __init__(self, clients: "Clients", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.clients = clients
        self._workers: list[ApiWorker] = []
        self._events: list[dict] = []
        self._setup_ui()
        self._load_events()

    def _setup_ui(self) -> None:
        """Build the calendar page layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header_row = QHBoxLayout()
        header = QLabel("📅 Calendar")
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        header_row.addWidget(header)
        header_row.addStretch()

        add_btn = QPushButton("➕ Add Event")
        add_btn.clicked.connect(self._on_add_event)
        header_row.addWidget(add_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self._load_events)
        header_row.addWidget(refresh_btn)

        layout.addLayout(header_row)

        # Event table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Start", "End", "Location"])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self.table)

        # Status
        self.status = QLabel("Loading...")
        self.status.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(self.status)

    def _load_events(self) -> None:
        """Load upcoming events."""
        self.status.setText("Loading...")

        def fetch():
            now = dt.datetime.now(dt.timezone.utc)
            return self.clients.calendar.list_events(time_min=now, max_results=50)

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_events_loaded)
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_events_loaded(self, events: list[dict]) -> None:
        """Handle loaded events."""
        self._events = events
        self.table.setRowCount(len(events))

        for row, event in enumerate(events):
            title = event.get("summary", "No Title")
            start = event.get("start", {}).get(
                "dateTime", event.get("start", {}).get("date", "")
            )
            end = event.get("end", {}).get(
                "dateTime", event.get("end", {}).get("date", "")
            )
            location = event.get("location", "")

            # Format datetime strings
            if "T" in start:
                start = start[:16].replace("T", " ")
            if "T" in end:
                end = end[:16].replace("T", " ")

            self.table.setItem(row, 0, QTableWidgetItem(title))
            self.table.setItem(row, 1, QTableWidgetItem(start))
            self.table.setItem(row, 2, QTableWidgetItem(end))
            self.table.setItem(row, 3, QTableWidgetItem(location))

        self.status.setText(f"{len(events)} upcoming events")

    def _on_error(self, e: Exception) -> None:
        """Handle API error."""
        self.status.setText(f"Error: {e}")

    def _on_add_event(self) -> None:
        """Open add event dialog."""
        dialog = AddEventDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_event_data()
            if not data["summary"]:
                self.status.setText("Error: Title required")
                return

            self._create_event(data)

    def _create_event(self, data: dict) -> None:
        """Create a new event."""
        self.status.setText("Creating event...")

        def create():
            return self.clients.calendar.add_event(
                summary=data["summary"],
                start=data["start"],
                end=data["end"],
                location=data["location"],
            )

        worker = ApiWorker(create)
        worker.finished.connect(lambda _: self._load_events())
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _show_context_menu(self, pos) -> None:
        """Show right-click context menu."""
        row = self.table.rowAt(pos.y())
        if row < 0 or row >= len(self._events):
            return

        event = self._events[row]
        menu = QMenu(self)

        delete_action = menu.addAction("🗑️ Delete")

        action = menu.exec(self.table.mapToGlobal(pos))

        if action == delete_action:
            self._delete_event(event)

    def _delete_event(self, event: dict) -> None:
        """Delete an event."""
        event_id = event.get("id")
        title = event.get("summary", "event")
        self.status.setText(f"Deleting {title}...")

        def delete():
            return self.clients.calendar.delete_event(event_id)

        worker = ApiWorker(delete)
        worker.finished.connect(lambda _: self._load_events())
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()
