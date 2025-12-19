"""Activity dashboard widgets and models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from PySide6.QtCore import QAbstractListModel, QModelIndex, QRect, QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import (
    QLabel,
    QListView,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QVBoxLayout,
    QWidget,
)


class ActivityStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class ActivityItem:
    id: str
    title: str
    status: ActivityStatus = ActivityStatus.PENDING
    details: str = ""


class ActivityModel(QAbstractListModel):
    """Model to store and manage activity items."""

    TitleRole = Qt.ItemDataRole.UserRole + 1
    StatusRole = Qt.ItemDataRole.UserRole + 2
    DetailsRole = Qt.ItemDataRole.UserRole + 3

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._activities: list[ActivityItem] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._activities)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= len(self._activities):
            return None

        activity = self._activities[index.row()]

        if role == Qt.ItemDataRole.DisplayRole or role == self.TitleRole:
            return activity.title
        elif role == self.StatusRole:
            return activity.status
        elif role == self.DetailsRole:
            return activity.details

        return None

    def add_activity(self, activity: ActivityItem) -> None:
        """Add a new activity to the list."""
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._activities.append(activity)
        self.endInsertRows()

    def update_status(
        self, activity_id: str, status: ActivityStatus, details: str | None = None
    ) -> None:
        """Update the status of an existing activity."""
        for i, activity in enumerate(self._activities):
            if activity.id == activity_id:
                activity.status = status
                if details is not None:
                    activity.details = details
                index = self.index(i)
                self.dataChanged.emit(index, index, [self.StatusRole, self.DetailsRole])
                break


class ActivityDelegate(QStyledItemDelegate):
    """Delegate to custom paint activity items."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.status_icons = {
            ActivityStatus.PENDING: "⏳",
            ActivityStatus.RUNNING: "🔄",
            ActivityStatus.SUCCESS: "✅",
            ActivityStatus.ERROR: "❌",
        }
        self.status_colors = {
            ActivityStatus.PENDING: "#6e7681",  # text_muted
            ActivityStatus.RUNNING: "#d29922",  # warning (amber)
            ActivityStatus.SUCCESS: "#3fb950",  # success (green)
            ActivityStatus.ERROR: "#f85149",  # error (red)
        }

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        if not index.isValid():
            return

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw selection background
        # Use QStyle.State.State_Selected (PySide6)
        if option.state & QStyle.State.State_Selected:
            painter.fillRect(option.rect, QColor("#2d333b"))  # bg_tertiary

        rect = option.rect
        margin = 10

        # Data
        title = index.data(ActivityModel.TitleRole)
        status = index.data(ActivityModel.StatusRole)
        details = index.data(ActivityModel.DetailsRole)
        icon = self.status_icons.get(status, "?")
        status_color = self.status_colors.get(status, "#ffffff")

        # Draw Icon
        icon_font = QFont()
        icon_font.setPixelSize(18)
        painter.setFont(icon_font)
        icon_rect = QRect(
            rect.left() + margin, rect.top() + margin, 30, rect.height() - 2 * margin
        )
        painter.drawText(icon_rect, Qt.AlignmentFlag.AlignCenter, icon)

        # Draw Title
        title_font = QFont()
        title_font.setPixelSize(13)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.setPen(QColor("#f0f6fc"))  # text_primary
        title_rect = QRect(
            rect.left() + margin + 40,
            rect.top() + margin,
            rect.width() - margin * 2 - 40,
            20,
        )
        painter.drawText(
            title_rect,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            title,
        )

        # Draw Details/Status
        details_font = QFont()
        details_font.setPixelSize(12)
        painter.setFont(details_font)
        painter.setPen(QColor(status_color))
        details_rect = QRect(
            rect.left() + margin + 40,
            rect.top() + margin + 20,
            rect.width() - margin * 2 - 40,
            20,
        )
        display_text = f"{status.value.upper()}"
        if details:
            display_text += f": {details}"
        painter.drawText(
            details_rect,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            display_text,
        )

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return QSize(option.rect.width(), 60)


class ActivityWidget(QWidget):
    """Widget to display the list of activities."""

    def __init__(self, model: ActivityModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.model = model
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        header = QLabel("Recent Activity")
        header.setObjectName("subheader")
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)

        self.view = QListView()
        self.view.setModel(self.model)
        self.view.setItemDelegate(ActivityDelegate(self))
        self.view.setSelectionMode(QListView.SelectionMode.NoSelection)
        self.view.setStyleSheet("background-color: transparent; border: none;")
        layout.addWidget(self.view)