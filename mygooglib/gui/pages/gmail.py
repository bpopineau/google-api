"""Gmail page - inbox viewer and composer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from mygooglib.gui.styles import COLORS
from mygooglib.gui.workers import ApiWorker

if TYPE_CHECKING:
    from mygooglib.client import Clients


class ComposeDialog(QDialog):
    """Email compose dialog."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Compose Email")
        self.setMinimumSize(500, 400)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.to_input = QLineEdit()
        self.to_input.setPlaceholderText("recipient@example.com")
        form.addRow("To:", self.to_input)

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Subject")
        form.addRow("Subject:", self.subject_input)

        layout.addLayout(form)

        self.body_input = QPlainTextEdit()
        self.body_input.setPlaceholderText("Write your message...")
        layout.addWidget(self.body_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Send")
        layout.addWidget(buttons)

    def get_email_data(self) -> dict:
        """Return the composed email data."""
        return {
            "to": self.to_input.text().strip(),
            "subject": self.subject_input.text().strip(),
            "body": self.body_input.toPlainText(),
        }


class GmailPage(QWidget):
    """Gmail inbox viewer and composer."""

    def __init__(self, clients: "Clients", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.clients = clients
        self._workers: list[ApiWorker] = []
        self._messages: list[dict] = []
        self._setup_ui()
        self._load_messages()

    def _setup_ui(self) -> None:
        """Build the Gmail page layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header_row = QHBoxLayout()
        header = QLabel("📧 Gmail")
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        header_row.addWidget(header)
        header_row.addStretch()

        compose_btn = QPushButton("✉️ Compose")
        compose_btn.clicked.connect(self._on_compose)
        header_row.addWidget(compose_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self._load_messages)
        header_row.addWidget(refresh_btn)

        layout.addLayout(header_row)

        # Search bar
        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search emails (e.g., from:someone@example.com)"
        )
        self.search_input.returnPressed.connect(self._on_search)
        search_row.addWidget(self.search_input)

        search_btn = QPushButton("🔍")
        search_btn.clicked.connect(self._on_search)
        search_row.addWidget(search_btn)

        layout.addLayout(search_row)

        # Split view: list + preview
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Message list
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["From", "Subject", "Date"])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        splitter.addWidget(self.table)

        # Preview panel
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(16, 0, 0, 0)

        self.preview_subject = QLabel("Select an email to preview")
        self.preview_subject.setStyleSheet("font-size: 16px; font-weight: bold;")
        preview_layout.addWidget(self.preview_subject)

        self.preview_from = QLabel("")
        self.preview_from.setStyleSheet(f"color: {COLORS['text_secondary']};")
        preview_layout.addWidget(self.preview_from)

        self.preview_body = QTextEdit()
        self.preview_body.setReadOnly(True)
        preview_layout.addWidget(self.preview_body)

        splitter.addWidget(preview_widget)
        splitter.setSizes([400, 600])

        layout.addWidget(splitter)

        # Status
        self.status = QLabel("Loading...")
        self.status.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(self.status)

    def _load_messages(self, query: str = "in:inbox") -> None:
        """Load messages from Gmail."""
        self.status.setText("Loading...")

        def fetch():
            return self.clients.gmail.search_messages(query=query, max_results=20)

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_messages_loaded)
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_messages_loaded(self, messages: list[dict]) -> None:
        """Handle loaded messages."""
        self._messages = messages
        self.table.setRowCount(len(messages))

        for row, msg in enumerate(messages):
            headers = {
                h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])
            }
            from_addr = headers.get("From", "Unknown")[:40]
            subject = headers.get("Subject", "(No Subject)")[:60]
            date = headers.get("Date", "")[:20]

            self.table.setItem(row, 0, QTableWidgetItem(from_addr))
            self.table.setItem(row, 1, QTableWidgetItem(subject))
            self.table.setItem(row, 2, QTableWidgetItem(date))

        self.status.setText(f"{len(messages)} messages loaded")

    def _on_error(self, e: Exception) -> None:
        """Handle API error."""
        self.status.setText(f"Error: {e}")

    def _on_search(self) -> None:
        """Handle search action."""
        query = self.search_input.text().strip() or "in:inbox"
        self._load_messages(query)

    def _on_selection_changed(self) -> None:
        """Handle message selection."""
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return

        row = rows[0].row()
        if row >= len(self._messages):
            return

        msg = self._messages[row]
        headers = {
            h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])
        }

        self.preview_subject.setText(headers.get("Subject", "(No Subject)"))
        self.preview_from.setText(f"From: {headers.get('From', 'Unknown')}")

        # Get body (simplified - just shows snippet for now)
        snippet = msg.get("snippet", "")
        self.preview_body.setPlainText(snippet)

    def _on_compose(self) -> None:
        """Open compose dialog."""
        dialog = ComposeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_email_data()
            if not data["to"]:
                self.status.setText("Error: Recipient required")
                return

            self._send_email(data)

    def _send_email(self, data: dict) -> None:
        """Send an email."""
        self.status.setText("Sending...")

        def send():
            return self.clients.gmail.send_email(
                to=data["to"],
                subject=data["subject"],
                body=data["body"],
            )

        worker = ApiWorker(send)
        worker.finished.connect(self._on_email_sent)
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_email_sent(self, _) -> None:
        """Handle email sent successfully."""
        self.status.setText("Email sent!")
        # Auto-refresh to update the message list
        self._load_messages()
