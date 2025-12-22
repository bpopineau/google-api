"""Drive file tree widget."""

from __future__ import annotations

import typing

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHeaderView, QTreeWidget, QTreeWidgetItem


class FileTreeWidget(QTreeWidget):
    """Tree widget for displaying Drive files and folders."""

    # Signal emitted when a folder needs to be loaded
    # Arguments: item (QTreeWidgetItem), folder_id (str)
    folder_expanded = Signal(QTreeWidgetItem, str)

    # Signal emitted when a file/folder is acted upon (e.g. double click)
    file_activated = Signal(dict)  # Passes the file metadata

    def __init__(self, parent: typing.Optional[typing.Any] = None) -> None:
        super().__init__(parent)
        self.setColumnCount(3)
        self.setHeaderLabels(["Name", "Type", "ID"])

        # Configure header
        header = self.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        self.setAlternatingRowColors(True)
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self.itemExpanded.connect(self._on_item_expanded)
        self.itemDoubleClicked.connect(self._on_item_double_clicked)

        # Store file data by item ID (memory address) to avoid circular refs or complex lookups
        self._item_data: dict[int, dict] = {}

    def add_file_item(
        self, file_data: dict, parent_item: QTreeWidgetItem | None = None
    ) -> QTreeWidgetItem:
        """Add a file/folder item to the tree."""
        name = file_data.get("name", "Unknown")
        mime = file_data.get("mimeType", "")
        file_id = file_data.get("id", "")

        # Determine icon and type string
        icon = "📄"
        type_str = "File"
        is_folder = "folder" in mime

        if is_folder:
            icon = "📁"
            type_str = "Folder"
        elif "spreadsheet" in mime:
            icon = "📊"
            type_str = "Sheet"
        elif "document" in mime:
            icon = "📝"
            type_str = "Doc"
        elif "image" in mime:
            icon = "🖼️"
            type_str = "Image"
        elif "pdf" in mime:
            icon = "📕"
            type_str = "PDF"

        display_name = f"{icon} {name}"

        item = QTreeWidgetItem([display_name, type_str, file_id])

        # Store metadata
        item.setData(0, Qt.ItemDataRole.UserRole, file_id)
        self._item_data[id(item)] = file_data

        if parent_item:
            parent_item.addChild(item)
        else:
            self.addTopLevelItem(item)

        # If it's a folder, add a dummy item to make it expandable
        if is_folder:
            dummy = QTreeWidgetItem(["Loading..."])
            dummy.setData(0, Qt.ItemDataRole.UserRole, "dummy")
            item.addChild(dummy)
            item.setChildIndicatorPolicy(
                QTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator
            )

        return item

    def clear(self) -> None:
        """Clear the tree and internal data."""
        super().clear()
        self._item_data.clear()

    def get_file_data(self, item: QTreeWidgetItem) -> dict | None:
        """Get the file metadata associated with an item."""
        return self._item_data.get(id(item))

    def _on_item_expanded(self, item: QTreeWidgetItem) -> None:
        """Handle item expansion to trigger lazy loading."""
        # Check if it has a dummy child
        if item.childCount() == 1:
            child = item.child(0)
            if child.data(0, Qt.ItemDataRole.UserRole) == "dummy":
                # It's a folder that needs loading
                file_id = item.data(0, Qt.ItemDataRole.UserRole)
                self.folder_expanded.emit(item, file_id)

    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        """Handle double click."""
        data = self.get_file_data(item)
        if data:
            self.file_activated.emit(data)

    def populate_folder(
        self, parent_item: QTreeWidgetItem | None, files: list[dict]
    ) -> None:
        """Populate a folder (root or subfolder) with files."""
        # If parent_item is None, we are populating root
        # If parent_item is set, we are populating a subfolder

        if parent_item:
            # Remove the dummy item
            if parent_item.childCount() > 0:
                # We assume the first child is the dummy if it exists and hasn't been populated yet
                # But to be safe, let's just clear all children before adding new ones
                # This also handles "Refresh" logic nicely
                parent_item.takeChildren()
        else:
            self.clear()

        for f in files:
            self.add_file_item(f, parent_item)
