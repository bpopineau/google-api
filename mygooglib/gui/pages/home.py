"""Home page - dashboard overview."""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from mygooglib.gui.styles import COLORS
from mygooglib.gui.widgets.cards import ItemCard, StatCard
from mygooglib.gui.workers import ApiWorker

if TYPE_CHECKING:
    from mygooglib.client import Clients


class HomePage(QScrollArea):
    """Dashboard home page with Global Search."""

    def __init__(self, clients: "Clients", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.clients = clients
        self._workers: list[ApiWorker] = []
        self._setup_ui()
        self._load_dashboard_data()

        # Optional periodic refresh (60 seconds)
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._load_dashboard_data)
        self._refresh_timer.start(60_000)  # 60 seconds

    def _setup_ui(self) -> None:
        """Build the home page layout."""
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)

        # Main wrapper
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(24, 24, 24, 24)
        wrapper_layout.setSpacing(24)

        # --- Search Bar ---
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Drive & Gmail...")
        self.search_input.setStyleSheet("padding: 10px; font-size: 14px;")
        self.search_input.returnPressed.connect(self._on_search)

        search_btn = QPushButton("🔍 Search")
        search_btn.clicked.connect(self._on_search)
        search_btn.setStyleSheet("padding: 10px 20px;")

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        wrapper_layout.addLayout(search_layout)

        # --- Content Stack (Dashboard vs Results) ---
        self.stack = QStackedWidget()
        wrapper_layout.addWidget(self.stack)

        # 1. Dashboard View
        self.dashboard_view = QWidget()
        self._setup_dashboard_view(self.dashboard_view)
        self.stack.addWidget(self.dashboard_view)

        # 2. Results View
        self.results_view = QWidget()
        self._setup_results_view(self.results_view)
        self.stack.addWidget(self.results_view)

        wrapper_layout.addStretch()
        self.setWidget(wrapper)

    def _setup_dashboard_view(self, parent: QWidget) -> None:
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)

        # Header
        header = QLabel("🏠 Dashboard")
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

        # Sections
        self._add_section(layout, "📅 Upcoming Events", "calendar_list")
        self._add_section(layout, "✅ Pending Tasks", "tasks_list")
        self._add_section(layout, "📂 Recent Files", "drive_list")

    def _setup_results_view(self, parent: QWidget) -> None:
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)

        # Back / Header
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back to Dashboard")
        back_btn.setFixedWidth(150)
        back_btn.clicked.connect(self._clear_search)
        header_layout.addWidget(back_btn)

        self.results_header = QLabel("Search Results")
        self.results_header.setStyleSheet(
            "font-size: 24px; font-weight: bold; margin-left: 10px;"
        )
        header_layout.addWidget(self.results_header)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Results Lists
        self._add_section(layout, "📂 Drive Matches", "search_drive_list")
        self._add_section(layout, "📧 Gmail Matches", "search_gmail_list")

    def _add_section(self, layout: QVBoxLayout, title: str, attr_name: str) -> None:
        """Helper to add a headed list section."""
        header = QLabel(title)
        header.setStyleSheet("font-size: 18px; font-weight: 600; margin-top: 16px;")
        layout.addWidget(header)

        list_layout = QVBoxLayout()
        list_layout.setSpacing(8)
        setattr(self, attr_name, list_layout)
        layout.addLayout(list_layout)

    # --- Data Loading (Dashboard) ---

    def _load_dashboard_data(self) -> None:
        """Load data from all services asynchronously."""
        self._load_calendar()
        self._load_tasks()
        self._load_drive()

    def _load_calendar(self) -> None:
        def fetch():
            now = dt.datetime.now(dt.timezone.utc)
            return self.clients.calendar.list_events(time_min=now, max_results=5)

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_calendar_loaded)
        worker.error.connect(lambda e: self.calendar_stat.set_value("!"))
        self._workers.append(worker)
        worker.start()

    def _on_calendar_loaded(self, events: list) -> None:
        self.calendar_stat.set_value(str(len(events)))
        self._clear_layout(self.calendar_list)
        for event in events:
            start = event.get("start", {}).get(
                "dateTime", event.get("start", {}).get("date", "")
            )
            title = event.get("summary", "No Title")
            card = ItemCard("📅", title, start[:16] if start else "")
            self.calendar_list.addWidget(card)

    def _load_tasks(self) -> None:
        def fetch():
            return self.clients.tasks.list_tasks(show_completed=False, max_results=5)

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_tasks_loaded)
        worker.error.connect(lambda e: self.tasks_stat.set_value("!"))
        self._workers.append(worker)
        worker.start()

    def _on_tasks_loaded(self, tasks: list) -> None:
        self.tasks_stat.set_value(str(len(tasks)))
        self._clear_layout(self.tasks_list)
        for task in tasks:
            title = task.get("title", "Untitled")
            due = task.get("due", "")
            card = ItemCard(
                "☐", title, due[:10] if due else "", actions=[("complete", "Done")]
            )
            self.tasks_list.addWidget(card)

    def _load_drive(self) -> None:
        def fetch():
            return self.clients.drive.list_files(page_size=5)

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_drive_loaded)
        worker.error.connect(lambda e: self.drive_stat.set_value("!"))
        self._workers.append(worker)
        worker.start()

    def _on_drive_loaded(self, files: list) -> None:
        self.drive_stat.set_value(str(len(files)))
        self._clear_layout(self.drive_list)
        for f in files:
            self.drive_list.addWidget(self._create_drive_card(f))

        # Placeholder for Gmail stat until search
        self.gmail_stat.set_value("—")

    # --- Global Search Logic ---

    def _on_search(self) -> None:
        query = self.search_input.text().strip()
        if not query:
            self._clear_search()
            return

        self.stack.setCurrentIndex(1)  # Show results
        self.results_header.setText(f"Searching for '{query}'...")
        self._clear_layout(self.search_drive_list)
        self._clear_layout(self.search_gmail_list)

        def fetch_search():
            # Parallel-ish (sequential in worker)
            d_results = self.clients.drive.list_files(
                query=f"name contains '{query}'", page_size=10
            )
            g_results = self.clients.gmail.search_messages(query=query, max_results=10)
            return d_results, g_results

        worker = ApiWorker(fetch_search)
        worker.finished.connect(lambda results: self._on_search_results(results, query))
        worker.error.connect(self._on_search_error)
        self._workers.append(worker)
        worker.start()

    def _on_search_results(self, results: tuple[list, list], query: str) -> None:
        drive_files, gmail_msgs = results
        self.results_header.setText(f"Results for '{query}'")

        # Render Drive
        if not drive_files:
            self.search_drive_list.addWidget(QLabel("No matching files found."))
        else:
            for f in drive_files:
                self.search_drive_list.addWidget(self._create_drive_card(f))

        # Render Gmail
        if not gmail_msgs:
            self.search_gmail_list.addWidget(QLabel("No matching emails found."))
        else:
            for msg in gmail_msgs:
                self.search_gmail_list.addWidget(self._create_gmail_card(msg))

    def _on_search_error(self, e: Exception) -> None:
        self.results_header.setText("Search Error")
        self.search_drive_list.addWidget(QLabel(f"Error: {e}"))

    def _clear_search(self) -> None:
        self.search_input.clear()
        self.stack.setCurrentIndex(0)

    # --- Helpers ---

    def _clear_layout(self, layout: QVBoxLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _create_drive_card(self, f: dict) -> ItemCard:
        name = f.get("name", "Untitled")
        mime = f.get("mimeType", "")
        file_id = f.get("id", "")
        icon = "📄"
        if "folder" in mime:
            icon = "📁"
        elif "spreadsheet" in mime:
            icon = "📊"
        elif "document" in mime:
            icon = "📝"

        card = ItemCard(
            icon,
            name,
            mime.split(".")[-1] if "." in mime else "",
            actions=[("copy_id", "Copy ID")],
        )
        card.action_clicked.connect(
            lambda action: self._on_card_action(action, file_id)
        )
        return card

    def _create_gmail_card(self, msg: dict) -> ItemCard:
        subject = msg.get("subject", "(No Subject)")
        sender = msg.get("from", "Unknown")
        snippet = msg.get("snippet", "")
        msg_id = msg.get("id", "")

        # Clean up sender
        if "<" in sender:
            sender = sender.split("<")[0].strip().replace('"', "")

        card = ItemCard(
            "✉️",
            subject,
            f"{sender} - {snippet[:60]}...",
            actions=[("copy_id", "Copy ID")],
        )
        card.action_clicked.connect(lambda action: self._on_card_action(action, msg_id))
        return card

    def _on_card_action(self, action: str, item_id: str) -> None:
        if action == "copy_id":
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText(item_id)
            # Optional: Show toast/status
            pass
