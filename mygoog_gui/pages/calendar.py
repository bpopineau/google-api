"""Calendar page - visual calendar with event list."""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QColor, QTextCharFormat
from PySide6.QtWidgets import (
    QCalendarWidget,
    QDateTimeEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from mygoog_gui.styles import COLORS
from mygoog_gui.workers import ApiWorker

if TYPE_CHECKING:
    from mygooglib.core.client import Clients
    from mygoog_gui.widgets.activity import ActivityModel


class AddEventDialog(QDialog):
    """Dialog for adding a new calendar event."""

    def __init__(
        self, parent: QWidget | None = None, start_date: dt.date | None = None
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Add Event")
        self.setMinimumWidth(400)
        self._start_date = start_date or dt.date.today()
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Event title")
        form.addRow("Title:", self.title_input)

        # Default start time: selected date at 9:00 AM
        start_dt = dt.datetime.combine(self._start_date, dt.time(9, 0))
        self.start_input = QDateTimeEdit()
        self.start_input.setDateTime(start_dt)
        self.start_input.setCalendarPopup(True)
        form.addRow("Start:", self.start_input)

        end_dt = dt.datetime.combine(self._start_date, dt.time(10, 0))
        self.end_input = QDateTimeEdit()
        self.end_input.setDateTime(end_dt)
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


class EventCard(QFrame):
    """Card widget displaying a single event."""

    def __init__(
        self,
        event: dict,
        on_delete: callable,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._event = event
        self._on_delete = on_delete
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setStyleSheet(f"""
            EventCard {{
                background-color: {COLORS["bg_secondary"]};
                border: 1px solid {COLORS["border"]};
                border-left: 4px solid {COLORS["accent"]};
                border-radius: 6px;
                padding: 12px;
            }}
            EventCard:hover {{
                background-color: {COLORS["bg_tertiary"]};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        # Title
        title = self._event.get("summary", "No Title")
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        layout.addWidget(title_label)

        # Time
        start = self._event.get("start", {})
        start_str = start.get("dateTime", start.get("date", ""))
        if "T" in start_str:
            # Parse and format nicely
            time_part = start_str.split("T")[1][:5]  # HH:MM
            time_label = QLabel(f"🕐 {time_part}")
        else:
            time_label = QLabel("📅 All day")
        time_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(time_label)

        # Location (if any)
        location = self._event.get("location", "")
        if location:
            loc_label = QLabel(f"📍 {location}")
            loc_label.setStyleSheet(
                f"color: {COLORS['text_secondary']}; font-size: 12px;"
            )
            layout.addWidget(loc_label)

        # Context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_menu)

    def _show_menu(self, pos) -> None:
        menu = QMenu(self)
        delete_action = menu.addAction("🗑️ Delete")
        action = menu.exec(self.mapToGlobal(pos))
        if action == delete_action:
            self._on_delete(self._event)


class CalendarPage(QWidget):
    """Google Calendar with visual calendar view."""

    def __init__(self, clients: "Clients", parent: QWidget | None = None, activity_model: ActivityModel | None = None) -> None:
        super().__init__(parent)
        self.clients = clients
        self.activity_model = activity_model
        self._workers: list[ApiWorker] = []
        self._events: list[dict] = []
        self._events_by_date: dict[str, list[dict]] = {}
        self._setup_ui()
        self._load_events()

    def _setup_ui(self) -> None:
        """Build the calendar page layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

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

        # Split view: Calendar + Events
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Left: Calendar widget
        calendar_container = QWidget()
        calendar_container.setMinimumWidth(280)
        calendar_layout = QVBoxLayout(calendar_container)
        calendar_layout.setContentsMargins(0, 0, 0, 0)
        calendar_layout.setSpacing(8)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        self.calendar.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.calendar.setMinimumSize(320, 320)  # Square minimum size
        self.calendar.clicked.connect(self._on_date_selected)
        self.calendar.setStyleSheet(f"""
            QCalendarWidget {{
                background-color: {COLORS["bg_secondary"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 8px;
            }}
            QCalendarWidget QToolButton {{
                color: {COLORS["text_primary"]};
                background-color: transparent;
                padding: 6px;
            }}
            QCalendarWidget QToolButton:hover {{
                background-color: {COLORS["bg_tertiary"]};
                border-radius: 4px;
            }}
            QCalendarWidget QMenu {{
                background-color: {COLORS["bg_secondary"]};
            }}
            QCalendarWidget QSpinBox {{
                background-color: {COLORS["bg_tertiary"]};
                color: {COLORS["text_primary"]};
            }}
            QCalendarWidget QTableView {{
                selection-background-color: {COLORS["accent"]};
                selection-color: white;
            }}
        """)
        calendar_layout.addWidget(self.calendar, 1)  # Calendar expands

        # Today button
        today_btn = QPushButton("📍 Today")
        today_btn.clicked.connect(
            lambda: self.calendar.setSelectedDate(QDate.currentDate())
        )
        calendar_layout.addWidget(today_btn)

        splitter.addWidget(calendar_container)

        # Right: Event list for selected date
        event_panel = QWidget()
        event_panel.setMinimumWidth(240)  # Narrower to give calendar more room
        event_layout = QVBoxLayout(event_panel)
        event_layout.setContentsMargins(12, 0, 0, 0)
        event_layout.setSpacing(8)

        self.date_header = QLabel("")
        self.date_header.setStyleSheet("font-size: 18px; font-weight: 600;")
        event_layout.addWidget(self.date_header)

        # Scroll area for events
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.events_container = QWidget()
        self.events_layout = QVBoxLayout(self.events_container)
        self.events_layout.setContentsMargins(0, 8, 0, 8)
        self.events_layout.setSpacing(8)
        self.events_layout.addStretch()

        scroll.setWidget(self.events_container)
        event_layout.addWidget(scroll, 1)  # Scroll area expands

        splitter.addWidget(event_panel)
        splitter.setStretchFactor(0, 3)  # Calendar side gets 3 parts (wider)
        splitter.setStretchFactor(1, 2)  # Events side gets 2 parts (narrower)

        layout.addWidget(splitter, 1)  # Splitter stretches to fill available space

        # Status
        self.status = QLabel("Loading...")
        self.status.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(self.status)

        # Initialize date header
        self._on_date_selected(QDate.currentDate())

    def _load_events(self) -> None:
        """Load upcoming events for the current month."""
        self.status.setText("Loading...")

        def fetch():
            # Get events for 60 days from today
            now = dt.datetime.now(dt.timezone.utc)
            return self.clients.calendar.list_events(time_min=now, max_results=100)

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_events_loaded)
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_events_loaded(self, events: list[dict]) -> None:
        """Handle loaded events and update calendar."""
        self._events = events
        self._events_by_date.clear()

        # Group events by date
        for event in events:
            start = event.get("start", {})
            date_str = start.get("dateTime", start.get("date", ""))
            if "T" in date_str:
                date_key = date_str.split("T")[0]
            else:
                date_key = date_str

            if date_key:
                if date_key not in self._events_by_date:
                    self._events_by_date[date_key] = []
                self._events_by_date[date_key].append(event)

        # Highlight dates with events on calendar
        self._update_calendar_highlights()

        # Refresh the current day's event list
        self._on_date_selected(self.calendar.selectedDate())

        self.status.setText(f"{len(events)} events loaded")

    def _update_calendar_highlights(self) -> None:
        """Highlight dates that have events."""
        # Reset all dates to default format
        QTextCharFormat()

        # Highlight format for dates with events
        event_format = QTextCharFormat()
        event_format.setBackground(QColor(COLORS["accent"]))
        event_format.setForeground(QColor("white"))

        for date_str in self._events_by_date:
            try:
                year, month, day = map(int, date_str.split("-"))
                qdate = QDate(year, month, day)
                self.calendar.setDateTextFormat(qdate, event_format)
            except (ValueError, IndexError):
                pass

    def _on_date_selected(self, date: QDate) -> None:
        """Handle date selection - show events for that day."""
        date_str = date.toString("yyyy-MM-dd")
        display_date = date.toString("dddd, MMMM d, yyyy")
        self.date_header.setText(display_date)

        # Clear existing event cards
        while self.events_layout.count() > 1:  # Keep the stretch
            item = self.events_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Get events for this date
        events = self._events_by_date.get(date_str, [])

        if not events:
            no_events = QLabel("No events scheduled")
            no_events.setStyleSheet(f"color: {COLORS['text_muted']}; padding: 16px;")
            self.events_layout.insertWidget(0, no_events)
        else:
            for i, event in enumerate(events):
                card = EventCard(event, self._delete_event)
                self.events_layout.insertWidget(i, card)

    def _on_error(self, e: Exception) -> None:
        """Handle API error."""
        self.status.setText(f"Error: {e}")

    def _on_add_event(self) -> None:
        """Open add event dialog with selected date."""
        selected_date = self.calendar.selectedDate().toPython()
        dialog = AddEventDialog(self, start_date=selected_date)
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

