"""Drive page - file browser with upload/download."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMenu,
    QMessageBox,
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


class DrivePage(QWidget):
    """Google Drive file browser."""

    def __init__(self, clients: "Clients", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.clients = clients
        self._workers: list[ApiWorker] = []
        self._files: list[dict] = []
        self._setup_ui()
        self._load_files()

    def _setup_ui(self) -> None:
        """Build the drive page layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel("📂 Google Drive")
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(header)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search files...")
        self.search_input.returnPressed.connect(self._on_search)
        toolbar.addWidget(self.search_input, stretch=1)

        search_btn = QPushButton("🔍 Search")
        search_btn.clicked.connect(self._on_search)
        toolbar.addWidget(search_btn)

        upload_btn = QPushButton("⬆️ Upload")
        upload_btn.clicked.connect(self._on_upload)
        toolbar.addWidget(upload_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self._load_files)
        toolbar.addWidget(refresh_btn)

        layout.addLayout(toolbar)

        # File table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "ID"])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # Status bar
        self.status = QLabel("Loading...")
        self.status.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(self.status)

    def _load_files(self, query: str | None = None) -> None:
        """Load files from Drive."""
        self.status.setText("Loading...")

        def fetch():
            q_str = f"name contains '{query}'" if query else None
            return self.clients.drive.list_files(query=q_str, page_size=50)

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_files_loaded)
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_files_loaded(self, files: list[dict]) -> None:
        """Handle loaded files."""
        self._files = files
        self.table.setRowCount(len(files))

        for row, f in enumerate(files):
            name = f.get("name", "")
            mime = f.get("mimeType", "")
            file_id = f.get("id", "")

            # Determine icon
            icon = "📄"
            if "folder" in mime:
                icon = "📁"
            elif "spreadsheet" in mime:
                icon = "📊"
            elif "document" in mime:
                icon = "📝"
            elif "image" in mime:
                icon = "🖼️"

            name_item = QTableWidgetItem(f"{icon} {name}")
            type_item = QTableWidgetItem(
                mime.split(".")[-1] if "." in mime else mime[:20]
            )
            id_item = QTableWidgetItem(file_id[:12] + "...")

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, type_item)
            self.table.setItem(row, 2, id_item)

        self.status.setText(f"{len(files)} files loaded")

    def _on_error(self, e: Exception) -> None:
        """Handle API error."""
        self.status.setText(f"Error: {e}")

    def _on_search(self) -> None:
        """Handle search action."""
        query = self.search_input.text().strip()
        self._load_files(query if query else None)

    def _on_upload(self) -> None:
        """Handle upload action."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file to upload")
        if not file_path:
            return

        self.status.setText(f"Uploading {Path(file_path).name}...")

        def upload():
            return self.clients.drive.upload_file(file_path)

        worker = ApiWorker(upload)
        worker.finished.connect(
            lambda fid: self._on_upload_complete(fid, Path(file_path).name)
        )
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_upload_complete(self, file_id: str, name: str) -> None:
        """Handle upload completion."""
        self.status.setText(f"Uploaded: {name} (ID: {file_id[:12]}...)")
        self._load_files()  # Refresh list

    def _show_context_menu(self, pos) -> None:
        """Show right-click context menu."""
        row = self.table.rowAt(pos.y())
        if row < 0 or row >= len(self._files):
            return

        file = self._files[row]
        menu = QMenu(self)

        download_action = menu.addAction("⬇️ Download")
        copy_id_action = menu.addAction("📋 Copy ID")
        menu.addSeparator()
        delete_action = menu.addAction("🗑️ Delete")

        action = menu.exec(self.table.mapToGlobal(pos))

        if action == download_action:
            self._download_file(file)
        elif action == copy_id_action:
            from PySide6.QtWidgets import QApplication

            QApplication.clipboard().setText(file.get("id", ""))
            self.status.setText("File ID copied to clipboard")
        elif action == delete_action:
            self._delete_file(file)

    def _download_file(self, file: dict) -> None:
        """Download a file."""
        file_id = file.get("id")
        name = file.get("name", "file")

        save_path, _ = QFileDialog.getSaveFileName(self, "Save file", name)
        if not save_path:
            return

        self.status.setText(f"Downloading {name}...")

        def download():
            return self.clients.drive.download_file(file_id, save_path)

        worker = ApiWorker(download)
        worker.finished.connect(lambda _: self.status.setText(f"Downloaded: {name}"))
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _delete_file(self, file: dict) -> None:
        """Delete a file after confirmation."""
        name = file.get("name", "this file")
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        file_id = file.get("id")
        self.status.setText(f"Deleting {name}...")

        def delete():
            return self.clients.drive.delete_file(file_id)

        worker = ApiWorker(delete)
        worker.finished.connect(lambda _: self._on_delete_complete(name))
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_delete_complete(self, name: str) -> None:
        """Handle delete completion."""
        self.status.setText(f"Deleted: {name}")
        self._load_files()
