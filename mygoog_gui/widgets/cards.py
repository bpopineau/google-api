"""Reusable card widgets for displaying information."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from mygoog_gui.styles import COLORS


class StatCard(QFrame):
    """A card displaying a statistic with icon, value, and label."""

    def __init__(
        self,
        icon: str,
        value: str,
        label: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setStyleSheet(f"""
            StatCard {{
                background-color: {COLORS["bg_secondary"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        self._setup_ui(icon, value, label)

    def _setup_ui(self, icon: str, value: str, label: str) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Icon and value row
        top_row = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        top_row.addWidget(icon_label)
        top_row.addStretch()

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        top_row.addWidget(self.value_label)

        layout.addLayout(top_row)

        # Description label
        self.label = QLabel(label)
        self.label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(self.label)

    def set_value(self, value: str) -> None:
        """Update the displayed value."""
        self.value_label.setText(value)


class ItemCard(QFrame):
    """A clickable card for displaying an item with title and subtitle.

    Signals:
        clicked: Emitted when the card is clicked.
        action_clicked: Emitted with action name when an action button is clicked.
    """

    clicked = Signal()
    action_clicked = Signal(str)

    def __init__(
        self,
        icon: str,
        title: str,
        subtitle: str = "",
        actions: list[tuple[str, str]] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the item card.

        Args:
            icon: Emoji or icon string.
            title: Main title text.
            subtitle: Secondary text.
            actions: List of (action_name, button_label) tuples.
            parent: Parent widget.
        """
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            ItemCard {{
                background-color: {COLORS["bg_secondary"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 8px;
            }}
            ItemCard:hover {{
                background-color: {COLORS["bg_tertiary"]};
                border-color: {COLORS["accent"]};
            }}
        """)
        self._setup_ui(icon, title, subtitle, actions or [])

    def _setup_ui(
        self,
        icon: str,
        title: str,
        subtitle: str,
        actions: list[tuple[str, str]],
    ) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(icon_label)

        # Text content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: 600;")
        text_layout.addWidget(self.title_label)

        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            self.subtitle_label.setStyleSheet(
                f"color: {COLORS['text_secondary']}; font-size: 12px;"
            )
            text_layout.addWidget(self.subtitle_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        # Action buttons
        for action_name, button_label in actions:
            btn = QPushButton(button_label)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: 1px solid {COLORS["border"]};
                    padding: 4px 8px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS["bg_tertiary"]};
                }}
            """)
            btn.clicked.connect(lambda _, n=action_name: self.action_clicked.emit(n))
            layout.addWidget(btn)

    def mousePressEvent(self, event) -> None:
        """Emit clicked signal on mouse press."""
        self.clicked.emit()
        super().mousePressEvent(event)

    def set_title(self, title: str) -> None:
        """Update the title text."""
        self.title_label.setText(title)
