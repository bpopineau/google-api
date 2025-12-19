"""Drive page - file browser with upload/download."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMenu,
    QMessageBox,
    QPushButton,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from mygooglib.gui.styles import COLORS
from mygooglib.gui.widgets.drive_tree import FileTreeWidget
from mygooglib.gui.workers import ApiWorker

if TYPE_CHECKING:
    from mygooglib.client import Clients
    from mygooglib.gui.widgets.activity import ActivityModel


class DrivePage(QWidget):
    """Google Drive file browser."""

    def __init__(self, clients: "Clients", parent: QWidget | None = None, activity_model: ActivityModel | None = None) -> None:
        super().__init__(parent)
        self.clients = clients
        self.activity_model = activity_model
        self._workers: list[ApiWorker] = []
        self._files: list[dict] = []
        self._setup_ui()
        self._load_root()

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

        new_folder_btn = QPushButton("📁 New Folder")
        new_folder_btn.clicked.connect(self._on_new_folder)
        toolbar.addWidget(new_folder_btn)

        upload_btn = QPushButton("⬆️ Upload")
        upload_btn.clicked.connect(self._on_upload)
        toolbar.addWidget(upload_btn)

        sync_btn = QPushButton("🔄 Sync Folder")
        sync_btn.clicked.connect(self._on_sync_folder)
        toolbar.addWidget(sync_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self._load_root)
        toolbar.addWidget(refresh_btn)

        layout.addLayout(toolbar)

        # File tree
        self.tree = FileTreeWidget()
        self.tree.folder_expanded.connect(self._load_folder_contents)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self.tree)

        # Status bar
        self.status = QLabel("Loading...")
        self.status.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(self.status)

    def _load_root(self, query: str | None = None) -> None:
        """Load root files from Drive."""
        self.status.setText("Loading root..." if not query else "Searching...")
        self.tree.clear()

        def fetch():
            # If query is present, we might get a flat list, but that's okay.
            # Tree can handle top-level items.
            q_str = f"name contains '{query}'" if query else "'root' in parents"
            return self.clients.drive.list_files(query=q_str, page_size=100)

        worker = ApiWorker(fetch)
        worker.finished.connect(lambda files: self._on_folder_loaded(None, files))
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _load_folder_contents(self, item: QTreeWidgetItem, folder_id: str) -> None:
        """Load contents of a specific folder."""
        self.status.setText("Loading folder...")

        def fetch():
            # List files in this specific parent folder
            return self.clients.drive.list_files(parent_id=folder_id)

        worker = ApiWorker(fetch)
        worker.finished.connect(lambda files: self._on_folder_loaded(item, files))
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_folder_loaded(
        self, parent_item: QTreeWidgetItem | None, files: list[dict]
    ) -> None:
        """Handle loaded files for a folder."""
        self.tree.populate_folder(parent_item, files)
        self.status.setText(f"{len(files)} items loaded")

    def _on_error(self, e: Exception) -> None:
        """Handle API error."""
        self.status.setText(f"Error: {e}")

    def _on_search(self) -> None:
        """Handle search action."""
        query = self.search_input.text().strip()
        # If searching, we reload "root" with the query.
        # The tree will show them as top-level items.
        self._load_root(query if query else None)

    def _on_upload(self) -> None:
        """Handle upload action."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file to upload")
        if not file_path:
            return

        # Determine parent ID based on selection
        parent_id = "root"
        selected = self.tree.selectedItems()
        if selected:
            data = self.tree.get_file_data(selected[0])
            if data:
                if "folder" in data.get("mimeType", ""):
                    parent_id = data.get("id", "root")
                # If a file is selected, we could upload to its parent,
                # but we don't easily know the parent from the file data in the tree without extra lookup.
                # For now, let's default to root or explicitly selected folder.

        self.status.setText(f"Uploading {Path(file_path).name}...")

        def upload():
            return self.clients.drive.upload_file(
                file_path, parent_id=parent_id if parent_id != "root" else None
            )

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
        # Auto-refresh to show the new file
        self._load_root()

    def _show_context_menu(self, pos) -> None:
        """Show right-click context menu."""
        item = self.tree.itemAt(pos)
        if not item:
            return

        file_data = self.tree.get_file_data(item)
        if not file_data:
            return

        menu = QMenu(self)

        download_action = menu.addAction("⬇️ Download")
        copy_id_action = menu.addAction("📋 Copy ID")
        menu.addSeparator()
        delete_action = menu.addAction("🗑️ Delete")

        action = menu.exec(self.tree.mapToGlobal(pos))

        if action == download_action:
            self._download_file(file_data)
        elif action == copy_id_action:
            from PySide6.QtWidgets import QApplication

            QApplication.clipboard().setText(file_data.get("id", ""))
            self.status.setText("File ID copied to clipboard")
        elif action == delete_action:
            self._delete_file(file_data)

    def _download_file(self, file: dict) -> None:
        """Download a file."""
        file_id = str(file.get("id"))
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

        file_id = str(file.get("id"))
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
        # Auto-refresh to remove the deleted file from view
        self._load_root()

    def _on_new_folder(self) -> None:
        """Create a new folder."""
        # Get selected folder as parent, or use root
        parent_id = "root"
        current_item = self.tree.currentItem()
        if current_item:
            item_type = current_item.data(0, Qt.ItemDataRole.UserRole + 1)
            if item_type == "folder":
                parent_id = current_item.data(0, Qt.ItemDataRole.UserRole)

        # Ask for folder name
        folder_name, ok = QInputDialog.getText(
            self, "New Folder", "Enter folder name:", text="New Folder"
        )

        if not ok or not folder_name.strip():
            return

        folder_name = folder_name.strip()
        self.status.setText(f"Creating folder '{folder_name}'...")

        def create():
            return self.clients.drive.create_folder(folder_name, parent_id=parent_id)

        worker = ApiWorker(create)
        worker.finished.connect(lambda _: self._on_folder_created(folder_name))
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_folder_created(self, name: str) -> None:
        """Handle folder creation completion."""
        self.status.setText(f"Created folder: {name}")
        self._load_root()

    def _on_sync_folder(self) -> None:
        """Handle sync folder to sheets action."""
        if not self.activity_model:
            QMessageBox.warning(self, "Activity Error", "Activity model not initialized")
            return

        # 1. Select local folder
        directory = QFileDialog.getExistingDirectory(self, "Select Folder to Sync")
        if not directory:
            return

        # 2. Select target spreadsheet (simple implementation: ask for ID or use title)
        # For a better UX, we could list sheets, but for now let's ask for ID or title
        spreadsheet_id, ok = QInputDialog.getText(
            self, "Target Spreadsheet", "Enter Spreadsheet ID or Title:", text="Metadata Sync"
        )
        if not ok or not spreadsheet_id.strip():
            return
        
        spreadsheet_id = spreadsheet_id.strip()

        # 3. Start worker
        from uuid import uuid4
        from mygooglib.gui.workers import SyncWorker
        from mygooglib.gui.widgets.activity import ActivityItem, ActivityStatus

        activity_id = str(uuid4())
        activity = ActivityItem(
            id=activity_id,
            title=f"Sync: {Path(directory).name}",
            details="Initializing..."
        )
        self.activity_model.add_activity(activity)

        worker = SyncWorker(self.clients, directory, spreadsheet_id, "Sheet1")
        
        def on_scan():
            self.activity_model.update_status(activity_id, ActivityStatus.RUNNING, "Scanning files...")
        
        def on_upload(count):
            self.activity_model.update_status(activity_id, ActivityStatus.RUNNING, f"Uploading {count} files...")
        
        def on_finished(result):
            rows = result.get("updatedRows", 0)
            self.activity_model.update_status(activity_id, ActivityStatus.SUCCESS, f"Synced {rows} rows")
            self.status.setText(f"Sync complete: {rows} rows")

        def on_error(err):
            self.activity_model.update_status(activity_id, ActivityStatus.ERROR, err)
            QMessageBox.critical(self, "Sync Error", f"Sync failed:\n\n{err}")

        worker.started_scan.connect(on_scan)
        worker.started_upload.connect(on_upload)
        worker.finished.connect(on_finished)
        worker.error.connect(on_error)
        
        self._workers.append(worker)
        worker.start()
