"""Settings page for the MyGoog GUI."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from mygooglib.core.config import AppConfig

if TYPE_CHECKING:
    from mygooglib.core.client import Clients


class SettingsPage(QWidget):
    """Configuration and settings page."""

    def __init__(self, clients: "Clients | None") -> None:
        super().__init__()
        self.clients = clients
        self.config = AppConfig()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build the settings layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Header
        header = QLabel("Settings")
        header.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(header)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Theme Section
        self._add_section_header(layout, "Appearance")

        theme_layout = QHBoxLayout()
        theme_lbl = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        self.theme_combo.setCurrentText(self.config.theme)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)

        theme_layout.addWidget(theme_lbl)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        # Account Section
        layout.addSpacing(20)
        self._add_section_header(layout, "Account")

        # Credentials Info
        creds_info = QLabel("Signed in using: token.json")
        creds_info.setStyleSheet("color: #888;")
        layout.addWidget(creds_info)

        # Logout Button
        logout_btn = QPushButton("Sign Out (Clear Credentials)")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)
        logout_btn.setFixedWidth(250)
        logout_btn.clicked.connect(self._on_logout)
        layout.addWidget(logout_btn)

        layout.addStretch()

    def _add_section_header(self, layout: QVBoxLayout, text: str) -> None:
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        layout.addWidget(lbl)

    def _on_theme_changed(self, text: str) -> None:
        self.config.theme = text
        # Note: Theme change usually requires app restart or complex reload logic.
        # For now, we save it and notify.
        QMessageBox.information(
            self,
            "Theme Changed",
            f"Theme set to '{text}'. Please restart the application for changes to take effect.",
        )

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
        # 1. Delete token file
        # We need to compute path again potentially, or use auth helper
        # For simplicity, let's assume standard path for now or import it
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
            # 2. Quit App
            from PySide6.QtWidgets import QApplication

            QApplication.quit()

        except OSError as e:
            QMessageBox.critical(self, "Error", f"Failed to delete credentials: {e}")

