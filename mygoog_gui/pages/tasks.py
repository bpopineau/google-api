"""Tasks page - task manager with checkable list."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from mygoog_gui.styles import COLORS
from mygoog_gui.workers import ApiWorker

if TYPE_CHECKING:
    from mygoog_gui.widgets.activity import ActivityModel
    from mygooglib import Clients


class TasksPage(QWidget):
    """Google Tasks manager."""

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
        self._tasks: list[dict] = []
        self._task_list_id: str = "@default"
        self._setup_ui()
        self._load_task_lists()

    def _setup_ui(self) -> None:
        """Build the tasks page layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel("✅ Tasks")
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(header)

        # Task list selector row
        list_row = QHBoxLayout()
        list_lbl = QLabel("📝 List:")
        list_lbl.setStyleSheet("font-weight: 600;")
        list_row.addWidget(list_lbl)

        self.list_combo = QComboBox()
        self.list_combo.setMinimumWidth(200)
        self.list_combo.currentIndexChanged.connect(self._on_list_changed)
        list_row.addWidget(self.list_combo)
        list_row.addStretch()
        layout.addLayout(list_row)

        # Quick add row
        add_row = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Add a new task...")
        self.task_input.returnPressed.connect(self._on_add_task)
        add_row.addWidget(self.task_input)

        add_btn = QPushButton("➕ Add")
        add_btn.clicked.connect(self._on_add_task)
        add_row.addWidget(add_btn)

        refresh_btn = QPushButton("🔄")
        refresh_btn.clicked.connect(self._load_tasks)
        add_row.addWidget(refresh_btn)

        layout.addLayout(add_row)

        # Task list
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(4)
        self.list_widget.itemChanged.connect(self._on_item_changed)
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self.list_widget)

        # Show completed toggle
        toggle_row = QHBoxLayout()
        self.show_completed = False
        self.toggle_btn = QPushButton("Show Completed")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.toggled.connect(self._on_toggle_completed)
        toggle_row.addWidget(self.toggle_btn)
        toggle_row.addStretch()

        self.status = QLabel("")
        self.status.setStyleSheet(f"color: {COLORS['text_secondary']};")
        toggle_row.addWidget(self.status)

        layout.addLayout(toggle_row)

    def _load_task_lists(self) -> None:
        """Load available task lists."""
        self.status.setText("Loading lists...")

        def fetch():
            return self.clients.tasks.list_tasklists()

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_task_lists_loaded)
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_task_lists_loaded(self, lists: list[dict]) -> None:
        """Populate the task list dropdown."""
        self.list_combo.blockSignals(True)
        self.list_combo.clear()

        for task_list in lists:
            name = task_list.get("title", "Untitled")
            list_id = task_list.get("id", "")
            self.list_combo.addItem(name, list_id)

        self.list_combo.blockSignals(False)

        # Set default and load tasks
        if lists:
            self._task_list_id = lists[0].get("id", "@default")
        self._load_tasks()

    def _on_list_changed(self, index: int) -> None:
        """Handle task list selection change."""
        list_id = self.list_combo.currentData()
        if list_id:
            self._task_list_id = list_id
            self._load_tasks()

    def _load_tasks(self) -> None:
        """Load tasks from API."""
        self.status.setText("Loading...")

        def fetch():
            return self.clients.tasks.list_tasks(
                tasklist_id=self._task_list_id,
                show_completed=self.show_completed,
                max_results=100,
            )

        worker = ApiWorker(fetch)
        worker.finished.connect(self._on_tasks_loaded)
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_tasks_loaded(self, tasks: list[dict]) -> None:
        """Handle loaded tasks."""
        self._tasks = tasks
        self.list_widget.blockSignals(True)
        self.list_widget.clear()

        for task in tasks:
            title = task.get("title", "Untitled")
            status = task.get("status", "needsAction")
            is_completed = status == "completed"

            item = QListWidgetItem(title)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked if is_completed else Qt.CheckState.Unchecked
            )
            item.setData(Qt.ItemDataRole.UserRole, task.get("id"))

            if is_completed:
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(Qt.GlobalColor.gray)

            self.list_widget.addItem(item)

        self.list_widget.blockSignals(False)
        self.status.setText(f"{len(tasks)} tasks")

    def _on_error(self, e: Exception) -> None:
        """Handle API error."""
        self.status.setText(f"Error: {e}")

    def _on_add_task(self) -> None:
        """Add a new task."""
        title = self.task_input.text().strip()
        if not title:
            return

        self.task_input.clear()
        self.status.setText("Adding task...")

        def add():
            return self.clients.tasks.add_task(title=title)

        worker = ApiWorker(add)
        worker.finished.connect(lambda _: self._load_tasks())
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        """Handle checkbox state change."""
        task_id = item.data(Qt.ItemDataRole.UserRole)
        is_completed = item.checkState() == Qt.CheckState.Checked

        self.status.setText("Updating...")

        def update():
            if is_completed:
                return self.clients.tasks.complete_task(task_id)
            else:
                # Uncomplete by updating status
                return self.clients.tasks.update_task(task_id, status="needsAction")

        worker = ApiWorker(update)
        worker.finished.connect(lambda _: self._load_tasks())
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()

    def _on_toggle_completed(self, checked: bool) -> None:
        """Toggle showing completed tasks."""
        self.show_completed = checked
        self._load_tasks()

    def _show_context_menu(self, pos) -> None:
        """Show right-click context menu."""
        item = self.list_widget.itemAt(pos)
        if not item:
            return

        task_id = item.data(Qt.ItemDataRole.UserRole)
        menu = QMenu(self)

        delete_action = menu.addAction("🗑️ Delete")

        action = menu.exec(self.list_widget.mapToGlobal(pos))

        if action == delete_action:
            self._delete_task(task_id, item.text())

    def _delete_task(self, task_id: str, title: str) -> None:
        """Delete a task."""
        self.status.setText(f"Deleting {title}...")

        def delete():
            return self.clients.tasks.delete_task(task_id)

        worker = ApiWorker(delete)
        worker.finished.connect(lambda _: self._load_tasks())
        worker.error.connect(self._on_error)
        self._workers.append(worker)
        worker.start()
