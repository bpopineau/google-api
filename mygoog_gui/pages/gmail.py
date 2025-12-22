"""Gmail page - inbox viewer and composer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
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

from mygoog_gui.styles import COLORS
from mygoog_gui.workers import ApiWorker

if TYPE_CHECKING:
    from mygooglib.core.client import Clients
    from mygoog_gui.widgets.activity import ActivityModel


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

    def __init__(
        self,
        clients: "Clients",
        parent: QWidget | None = None,
        activity_model: ActivityModel | None = None,
    ) -> None:
        super().__init__(parent)
        self.clients = clients
        self.activity_model = activity_model
        self._workers: list[ApiWorker] = []
        self._messages: list[dict] = []
        self._current_query: str = "in:inbox"
        self._selected_message_id: str | None = None
        self._setup_ui()
        self._load_labels()
        self._load_messages()

    def _setup_ui(self) -> None:
        """Build the Gmail page layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

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

        # Label selector row
        label_row = QHBoxLayout()
        label_lbl = QLabel("📁 Folder:")
        label_lbl.setStyleSheet("font-weight: 600;")
        label_row.addWidget(label_lbl)

        self.label_combo = QComboBox()
        self.label_combo.setMinimumWidth(200)
        self.label_combo.currentIndexChanged.connect(self._on_label_changed)
        label_row.addWidget(self.label_combo)

        label_row.addStretch()
        layout.addLayout(label_row)

        # Search bar
        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search within current folder (or enter full query)"
        )
        self.search_input.returnPressed.connect(self._on_search)
        search_row.addWidget(self.search_input)

        search_btn = QPushButton("🔍")
        search_btn.clicked.connect(self._on_search)
        search_row.addWidget(search_btn)

        layout.addLayout(search_row)

        # Split view: list + preview
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Message list
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["", "From", "Subject", "Date"])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Fixed
        )
        self.table.setColumnWidth(0, 30)  # Narrow indicator column
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setMinimumWidth(350)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        splitter.addWidget(self.table)

        # Preview panel
        preview_widget = QWidget()
        preview_widget.setMinimumWidth(300)
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(12, 0, 0, 0)
        preview_layout.setSpacing(8)

        self.preview_subject = QLabel("Select an email to preview")
        self.preview_subject.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.preview_subject.setWordWrap(True)
        preview_layout.addWidget(self.preview_subject)

        self.preview_from = QLabel("")
        self.preview_from.setStyleSheet(f"color: {COLORS['text_secondary']};")
        preview_layout.addWidget(self.preview_from)

        # Action buttons
        action_row = QHBoxLayout()
        self.mark_read_btn = QPushButton("📖 Mark Read")
        self.mark_read_btn.clicked.connect(self._on_mark_read)
        self.mark_read_btn.setEnabled(False)
        action_row.addWidget(self.mark_read_btn)

        self.archive_btn = QPushButton("📦 Archive")
        self.archive_btn.clicked.connect(self._on_archive)
        self.archive_btn.setEnabled(False)
        action_row.addWidget(self.archive_btn)

        self.trash_btn = QPushButton("🗑️ Trash")
        self.trash_btn.clicked.connect(self._on_trash)
        self.trash_btn.setEnabled(False)
        action_row.addWidget(self.trash_btn)

        action_row.addStretch()
        preview_layout.addLayout(action_row)

        self.preview_body = QTextEdit()
        self.preview_body.setReadOnly(True)
        preview_layout.addWidget(self.preview_body)

        splitter.addWidget(preview_widget)
        splitter.setStretchFactor(0, 2)  # Message list gets 2 parts
        splitter.setStretchFactor(1, 3)  # Preview gets 3 parts

        layout.addWidget(splitter, 1)  # Splitter stretches to fill available space

        # Status
        self.status = QLabel("Loading...")
        self.status.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(self.status)

    def _load_labels(self) -> None:
        """Load labels from Gmail."""

        def fetch():
            return self.clients.gmail.list_labels()

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_labels_loaded)
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_labels_loaded(self, labels: list[dict]) -> None:
        """Populate the label dropdown."""
        self.label_combo.blockSignals(True)
        self.label_combo.clear()

        # Add common system labels with nice names
        label_map = {
            "INBOX": ("📥 Inbox", "in:inbox"),
            "STARRED": ("⭐ Starred", "is:starred"),
            "SENT": ("📤 Sent", "in:sent"),
            "DRAFT": ("📝 Drafts", "in:drafts"),
            "IMPORTANT": ("❗ Important", "is:important"),
            "TRASH": ("🗑️ Trash", "in:trash"),
            "SPAM": ("⚠️ Spam", "in:spam"),
        }

        # Add system labels (in preferred order)
        preferred_order = ["INBOX", "STARRED", "SENT", "DRAFT", "IMPORTANT"]
        for label_id in preferred_order:
            if label_id in label_map:
                display_name, query = label_map[label_id]
                self.label_combo.addItem(display_name, query)

        # Separator
        self.label_combo.insertSeparator(self.label_combo.count())

        # Add user labels
        for label in labels:
            if label.get("type") == "user":
                name = label.get("name", "")
                label_id = label.get("id", "")
                if name and label_id:
                    self.label_combo.addItem(f"🏷️ {name}", f"label:{label_id}")

        self.label_combo.blockSignals(False)

    def _on_label_changed(self, index: int) -> None:
        """Handle label selection change."""
        query = self.label_combo.currentData()
        if query:
            self._current_query = query
            self.search_input.clear()
            self._load_messages(query)

    def _load_messages(self, query: str | None = None) -> None:
        """Load messages from Gmail."""
        if query is None:
            query = self._current_query
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
            # Unread indicator
            label_ids = msg.get("labelIds", [])
            is_unread = "UNREAD" in label_ids
            has_attachment = msg.get("has_attachment", False)

            indicator = ""
            if is_unread:
                indicator = "●"  # Unread dot
            if has_attachment:
                indicator += "📎"  # Attachment icon

            indicator_item = QTableWidgetItem(indicator)
            if is_unread:
                font = indicator_item.font()
                font.setBold(True)
                indicator_item.setFont(font)
            self.table.setItem(row, 0, indicator_item)

            # search_messages returns flat dict with subject/from/date keys (lowercase)
            from_addr = (msg.get("from") or "Unknown")[:40]
            subject = (msg.get("subject") or "(No Subject)")[:60]
            date = (msg.get("date") or "")[:20]

            from_item = QTableWidgetItem(from_addr)
            subject_item = QTableWidgetItem(subject)
            date_item = QTableWidgetItem(date)

            # Bold unread messages
            if is_unread:
                for item in [from_item, subject_item, date_item]:
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)

            self.table.setItem(row, 1, from_item)
            self.table.setItem(row, 2, subject_item)
            self.table.setItem(row, 3, date_item)

        self.status.setText(f"{len(messages)} messages loaded")

    def _on_error(self, e: Exception) -> None:
        """Handle API error."""
        self.status.setText(f"Error: {e}")

    def _on_search(self) -> None:
        """Handle search action."""
        search_text = self.search_input.text().strip()
        if search_text:
            # If search has Gmail operators, use as-is; otherwise combine with label
            if any(
                op in search_text
                for op in [":", "is:", "in:", "label:", "from:", "to:"]
            ):
                query = search_text
            else:
                # Search within current label
                query = f"{self._current_query} {search_text}"
        else:
            query = self._current_query
        self._load_messages(query)

    def _on_selection_changed(self) -> None:
        """Handle message selection - load full message body."""
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            self._enable_actions(False)
            return

        row = rows[0].row()
        if row >= len(self._messages):
            return

        msg = self._messages[row]
        self._selected_message_id = msg.get("id")
        self._enable_actions(True)

        # Show snippet immediately, then load full body
        self.preview_subject.setText(msg.get("subject") or "(No Subject)")
        self.preview_from.setText(f"From: {msg.get('from') or 'Unknown'}")
        self.preview_body.setPlainText(
            msg.get("snippet", "") + "\n\nLoading full message..."
        )

        # Load full message body
        def fetch_full():
            return self.clients.gmail.get_message(self._selected_message_id)

        worker = ApiWorker(fetch_full)
        worker.finished.connect(self._on_full_message_loaded)
        worker.error.connect(
            lambda e: self.preview_body.setPlainText(f"Error loading: {e}")
        )
        self._workers.append(worker)
        worker.start()

    def _on_full_message_loaded(self, msg: dict) -> None:
        """Handle full message loaded."""
        if msg.get("id") != self._selected_message_id:
            return  # User selected a different message

        self.preview_subject.setText(msg.get("subject") or "(No Subject)")
        self.preview_from.setText(f"From: {msg.get('from') or 'Unknown'}")
        body = msg.get("body", msg.get("snippet", ""))
        self.preview_body.setPlainText(body)

    def _enable_actions(self, enabled: bool) -> None:
        """Enable or disable action buttons."""
        self.mark_read_btn.setEnabled(enabled)
        self.archive_btn.setEnabled(enabled)
        self.trash_btn.setEnabled(enabled)

    def _on_mark_read(self) -> None:
        """Mark selected message as read."""
        if not self._selected_message_id:
            return
        self.status.setText("Marking as read...")

        def mark():
            return self.clients.gmail.mark_read(self._selected_message_id)

        worker = ApiWorker(mark)
        worker.finished.connect(lambda _: self._on_action_complete("Marked as read"))
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_archive(self) -> None:
        """Archive selected message."""
        if not self._selected_message_id:
            return
        self.status.setText("Archiving...")

        def archive():
            return self.clients.gmail.archive_message(self._selected_message_id)

        worker = ApiWorker(archive)
        worker.finished.connect(lambda _: self._on_action_complete("Archived"))
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_trash(self) -> None:
        """Trash selected message."""
        if not self._selected_message_id:
            return
        self.status.setText("Moving to trash...")

        def trash():
            return self.clients.gmail.trash_message(self._selected_message_id)

        worker = ApiWorker(trash)
        worker.finished.connect(lambda _: self._on_action_complete("Moved to trash"))
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_action_complete(self, message: str) -> None:
        """Handle action completion and refresh."""
        self.status.setText(message)
        self._load_messages()

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
