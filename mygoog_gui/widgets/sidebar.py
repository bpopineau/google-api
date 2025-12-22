"""Navigation sidebar widget."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class SidebarButton(QPushButton):
    """A checkable button for sidebar navigation."""

    def __init__(self, icon: str, text: str, parent: QWidget | None = None) -> None:
        super().__init__(f"{icon}  {text}", parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)


class Sidebar(QFrame):
    """Navigation sidebar with icon buttons for each service.

    Signals:
        page_changed: Emitted with the page name when a button is clicked.
    """

    page_changed = Signal(str)

    # Page definitions: (name, icon, label)
    PAGES = [
        ("home", "🏠", "Home"),
        ("drive", "📂", "Drive"),
        ("gmail", "📧", "Gmail"),
        ("tasks", "✅", "Tasks"),
        ("calendar", "📅", "Calendar"),
        ("sheets", "📊", "Sheets"),
    ]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(200)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build the sidebar layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(8)

        # App title
        title = QLabel("🤖 MyGoog")
        title.setObjectName("header")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 8px;")
        layout.addWidget(title)

        layout.addSpacing(20)

        # Button group for exclusive selection
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.buttons: dict[str, SidebarButton] = {}

        for name, icon, label in self.PAGES:
            btn = SidebarButton(icon, label)
            btn.clicked.connect(lambda checked, n=name: self._on_button_clicked(n))
            self.button_group.addButton(btn)
            self.buttons[name] = btn
            layout.addWidget(btn)

        # Spacer to push everything up
        layout.addStretch()

        # Settings button at bottom
        settings_btn = SidebarButton("⚙️", "Settings")
        settings_btn.clicked.connect(lambda: self._on_button_clicked("settings"))
        self.buttons["settings"] = settings_btn
        layout.addWidget(settings_btn)

    def _on_button_clicked(self, name: str) -> None:
        """Handle button click."""
        self.page_changed.emit(name)

    def select_page(self, name: str) -> None:
        """Programmatically select a page."""
        if name in self.buttons:
            self.buttons[name].setChecked(True)

