"""Home page - dashboard overview."""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from mygooglib.gui.styles import COLORS
from mygooglib.gui.widgets.cards import ItemCard, StatCard
from mygooglib.gui.workers import ApiWorker

if TYPE_CHECKING:
    from mygooglib.client import Clients


class HomePage(QScrollArea):
    """Dashboard home page with overview of all services."""

    def __init__(self, clients: "Clients", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.clients = clients
        self._workers: list[ApiWorker] = []
        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        """Build the home page layout."""
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        # Header
        header = QLabel("🏠 Dashboard")
        header.setObjectName("header")
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(header)

        subtitle = QLabel("Welcome to your Google Workspace command center")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        layout.addWidget(subtitle)

        layout.addSpacing(16)

        # Stats row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        self.calendar_stat = StatCard("📅", "...", "Upcoming Events")
        self.tasks_stat = StatCard("✅", "...", "Pending Tasks")
        self.gmail_stat = StatCard("📧", "...", "Recent Emails")
        self.drive_stat = StatCard("📂", "...", "Drive Files")

        stats_layout.addWidget(self.calendar_stat)
        stats_layout.addWidget(self.tasks_stat)
        stats_layout.addWidget(self.gmail_stat)
        stats_layout.addWidget(self.drive_stat)

        layout.addLayout(stats_layout)

        # Calendar section
        calendar_header = QLabel("📅 Upcoming Events")
        calendar_header.setStyleSheet(
            "font-size: 18px; font-weight: 600; margin-top: 16px;"
        )
        layout.addWidget(calendar_header)

        self.calendar_list = QVBoxLayout()
        self.calendar_list.setSpacing(8)
        layout.addLayout(self.calendar_list)

        # Tasks section
        tasks_header = QLabel("✅ Pending Tasks")
        tasks_header.setStyleSheet(
            "font-size: 18px; font-weight: 600; margin-top: 16px;"
        )
        layout.addWidget(tasks_header)

        self.tasks_list = QVBoxLayout()
        self.tasks_list.setSpacing(8)
        layout.addLayout(self.tasks_list)

        # Drive section
        drive_header = QLabel("📂 Recent Files")
        drive_header.setStyleSheet(
            "font-size: 18px; font-weight: 600; margin-top: 16px;"
        )
        layout.addWidget(drive_header)

        self.drive_list = QVBoxLayout()
        self.drive_list.setSpacing(8)
        layout.addLayout(self.drive_list)

        layout.addStretch()
        self.setWidget(container)

    def _load_data(self) -> None:
        """Load data from all services asynchronously."""
        # Calendar events
        self._load_calendar()
        self._load_tasks()
        self._load_drive()

    def _load_calendar(self) -> None:
        """Load upcoming calendar events."""

        def fetch():
            now = dt.datetime.now(dt.timezone.utc)
            return self.clients.calendar.list_events(time_min=now, max_results=5)

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_calendar_loaded)
        worker.error.connect(lambda e: self.calendar_stat.set_value("!"))
        self._workers.append(worker)
        worker.start()

    def _on_calendar_loaded(self, events: list) -> None:
        """Handle loaded calendar events."""
        self.calendar_stat.set_value(str(len(events)))

        # Clear existing items
        while self.calendar_list.count():
            item = self.calendar_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for event in events:
            start = event.get("start", {}).get(
                "dateTime", event.get("start", {}).get("date", "")
            )
            title = event.get("summary", "No Title")
            card = ItemCard("📅", title, start[:16] if start else "")
            self.calendar_list.addWidget(card)

    def _load_tasks(self) -> None:
        """Load pending tasks."""

        def fetch():
            return self.clients.tasks.list_tasks(show_completed=False, max_results=5)

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_tasks_loaded)
        worker.error.connect(lambda e: self.tasks_stat.set_value("!"))
        self._workers.append(worker)
        worker.start()

    def _on_tasks_loaded(self, tasks: list) -> None:
        """Handle loaded tasks."""
        self.tasks_stat.set_value(str(len(tasks)))

        while self.tasks_list.count():
            item = self.tasks_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for task in tasks:
            title = task.get("title", "Untitled")
            due = task.get("due", "")
            card = ItemCard(
                "☐", title, due[:10] if due else "", actions=[("complete", "Done")]
            )
            self.tasks_list.addWidget(card)

    def _load_drive(self) -> None:
        """Load recent drive files."""

        def fetch():
            return self.clients.drive.list_files(page_size=5)

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_drive_loaded)
        worker.error.connect(lambda e: self.drive_stat.set_value("!"))
        self._workers.append(worker)
        worker.start()

    def _on_drive_loaded(self, files: list) -> None:
        """Handle loaded drive files."""
        self.drive_stat.set_value(str(len(files)))

        while self.drive_list.count():
            item = self.drive_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for f in files:
            name = f.get("name", "Untitled")
            mime = f.get("mimeType", "")
            icon = "📄"
            if "folder" in mime:
                icon = "📁"
            elif "spreadsheet" in mime:
                icon = "📊"
            elif "document" in mime:
                icon = "📝"
            card = ItemCard(icon, name, mime.split(".")[-1] if "." in mime else "")
            self.drive_list.addWidget(card)

        # Also set gmail stat (just a placeholder count)
        self.gmail_stat.set_value("—")
