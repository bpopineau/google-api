"""Settings page for the MyGoog GUI."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from mygooglib.core.config import AppConfig

from ..theme_manager import ThemeManager

if TYPE_CHECKING:
    from mygooglib.core.client import Clients


class SettingsPage(QWidget):
    """Configuration and settings page with multi-section layout."""

    def __init__(self, clients: "Clients | None") -> None:
        super().__init__()
        self.clients = clients
        self.config = AppConfig()
        self.theme_manager = ThemeManager()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build the settings layout with sidebar navigation."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar navigation
        self.nav_list = QListWidget()
        self.nav_list.setFixedWidth(180)
        self.nav_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                border-right: 1px solid #3d444d;
            }
            QListWidget::item {
                padding: 12px 16px;
                border-radius: 0;
            }
            QListWidget::item:selected {
                background-color: #2d333b;
            }
        """)

        # Add navigation items
        sections = ["Appearance", "General", "Accounts", "Sync"]
        for section in sections:
            item = QListWidgetItem(section)
            self.nav_list.addItem(item)

        self.nav_list.currentRowChanged.connect(self._on_section_changed)
        layout.addWidget(self.nav_list)

        # Content stack
        self.content_stack = QStackedWidget()
        layout.addWidget(self.content_stack, 1)

        # Build sections
        self.content_stack.addWidget(self._build_appearance_section())
        self.content_stack.addWidget(self._build_general_section())
        self.content_stack.addWidget(self._build_accounts_section())
        self.content_stack.addWidget(self._build_sync_section())

        # Select first item
        self.nav_list.setCurrentRow(0)

    def _on_section_changed(self, index: int) -> None:
        """Handle section navigation."""
        self.content_stack.setCurrentIndex(index)

    def _build_section_container(self, title: str) -> tuple[QWidget, QVBoxLayout]:
        """Create a standard section container with header."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Header
        header = QLabel(title)
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(header)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        return container, layout

    def _build_appearance_section(self) -> QWidget:
        """Build the Appearance settings section."""
        container, layout = self._build_section_container("Appearance")

        # Theme setting
        theme_layout = QHBoxLayout()
        theme_lbl = QLabel("Theme:")
        theme_lbl.setFixedWidth(120)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light", "system"])
        self.theme_combo.setCurrentText(self.config.theme)
        self.theme_combo.setFixedWidth(150)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)

        theme_layout.addWidget(theme_lbl)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        # Accent color setting
        accent_layout = QHBoxLayout()
        accent_lbl = QLabel("Accent Color:")
        accent_lbl.setFixedWidth(120)

        self.accent_combo = QComboBox()
        self.accent_combo.addItems(["blue", "green", "purple", "orange"])
        self.accent_combo.setCurrentText(self.config.accent_color)
        self.accent_combo.setFixedWidth(150)
        self.accent_combo.currentTextChanged.connect(self._on_accent_changed)

        accent_layout.addWidget(accent_lbl)
        accent_layout.addWidget(self.accent_combo)
        accent_layout.addStretch()
        layout.addLayout(accent_layout)

        # Info note
        note = QLabel("Changes are applied immediately.")
        note.setStyleSheet("color: #6e7681; font-size: 12px; margin-top: 10px;")
        layout.addWidget(note)

        layout.addStretch()
        return container

    def _build_general_section(self) -> QWidget:
        """Build the General settings section."""
        container, layout = self._build_section_container("General")

        # Default view
        view_layout = QHBoxLayout()
        view_lbl = QLabel("Default View:")
        view_lbl.setFixedWidth(120)

        view_combo = QComboBox()
        view_combo.addItems(["home", "mail", "drive", "calendar", "tasks"])
        view_combo.setCurrentText(self.config.default_view)
        view_combo.setFixedWidth(150)
        view_combo.currentTextChanged.connect(self._on_default_view_changed)

        view_layout.addWidget(view_lbl)
        view_layout.addWidget(view_combo)
        view_layout.addStretch()
        layout.addLayout(view_layout)

        layout.addStretch()
        return container

    def _build_accounts_section(self) -> QWidget:
        """Build the Accounts settings section."""
        container, layout = self._build_section_container("Accounts")

        # Credentials Info
        creds_info = QLabel("Signed in using: token.json")
        creds_info.setStyleSheet("color: #9198a1;")
        layout.addWidget(creds_info)

        # Logout Button
        logout_btn = QPushButton("Sign Out (Clear Credentials)")
        logout_btn.setObjectName("danger_button")
        logout_btn.setStyleSheet("""
            QPushButton#danger_button {
                background-color: #d32f2f;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton#danger_button:hover {
                background-color: #b71c1c;
            }
        """)
        logout_btn.setFixedWidth(250)
        logout_btn.clicked.connect(self._on_logout)
        layout.addWidget(logout_btn)

        layout.addStretch()
        return container

    def _build_sync_section(self) -> QWidget:
        """Build the Sync settings section."""
        container, layout = self._build_section_container("Sync")

        # Placeholder content
        placeholder = QLabel("Sync settings coming soon.")
        placeholder.setStyleSheet("color: #6e7681;")
        layout.addWidget(placeholder)

        layout.addStretch()
        return container

    def _on_theme_changed(self, theme: str) -> None:
        """Handle theme selection change."""
        self.theme_manager.set_theme(theme)

    def _on_accent_changed(self, accent: str) -> None:
        """Handle accent color change."""
        self.theme_manager.set_accent_color(accent)

    def _on_default_view_changed(self, view: str) -> None:
        """Handle default view change."""
        self.config.default_view = view

    def _on_logout(self) -> None:
        """Handle sign out."""
        confirm = QMessageBox.question(
            self,
            "Confirm Sign Out",
            "Are you sure you want to sign out? This will delete your local credentials file.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self._do_sign_out()

    def _do_sign_out(self) -> None:
        """Execute sign out by deleting credentials."""
        from mygooglib.core.auth import _get_paths

        try:
            _, token_path = _get_paths()
            if token_path.exists():
                token_path.unlink()

            QMessageBox.information(
                self,
                "Signed Out",
                "Credentials cleared. The application will now close.",
            )
            # Quit App
            from PySide6.QtWidgets import QApplication

            QApplication.quit()

        except OSError as e:
            QMessageBox.critical(self, "Error", f"Failed to delete credentials: {e}")
