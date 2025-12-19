"""Main application window for the PySide6 GUI."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from mygooglib.gui.styles import STYLESHEET
from mygooglib.gui.widgets.sidebar import Sidebar

if TYPE_CHECKING:
    from mygooglib.client import Clients


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation."""

    def __init__(self, clients: "Clients") -> None:
        super().__init__()
        self.clients = clients
        self.setWindowTitle("MyGoog - Google Workspace Manager")
        self.setMinimumSize(1200, 800)
        self._pages: dict[str, QWidget] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build the main window layout."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._on_page_changed)
        layout.addWidget(self.sidebar)

        # Content area with stacked pages
        self.stack = QStackedWidget()
        self.stack.setObjectName("content")
        layout.addWidget(self.stack)

        # Create pages lazily
        self._create_pages()

        # Select home by default
        self.sidebar.select_page("home")
        self._on_page_changed("home")

    def _create_pages(self) -> None:
        """Create all page widgets."""
        # Import pages here to avoid circular imports
        from mygooglib.gui.pages.calendar import CalendarPage
        from mygooglib.gui.pages.drive import DrivePage
        from mygooglib.gui.pages.gmail import GmailPage
        from mygooglib.gui.pages.home import HomePage
        from mygooglib.gui.pages.sheets import SheetsPage
        from mygooglib.gui.pages.tasks import TasksPage

        self._pages["home"] = HomePage(self.clients)
        self._pages["drive"] = DrivePage(self.clients)
        self._pages["gmail"] = GmailPage(self.clients)
        self._pages["tasks"] = TasksPage(self.clients)
        self._pages["calendar"] = CalendarPage(self.clients)
        self._pages["sheets"] = SheetsPage(self.clients)
        self._pages["settings"] = self._create_settings_page()

        for page in self._pages.values():
            self.stack.addWidget(page)

    def _create_settings_page(self) -> QWidget:
        """Create a placeholder settings page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)

        header = QLabel("⚙️ Settings")
        header.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(header)

        info = QLabel("Settings page coming soon...")
        layout.addWidget(info)

        layout.addStretch()
        return page

    def _on_page_changed(self, name: str) -> None:
        """Handle page navigation."""
        if name in self._pages:
            self.stack.setCurrentWidget(self._pages[name])


def run_app() -> None:
    """Run the PySide6 application."""
    # Import here to avoid import errors when PySide6 isn't installed
    from mygooglib import get_clients

    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)

    # Authenticate
    try:
        clients = get_clients()
    except Exception as e:
        QMessageBox.critical(
            None,
            "Authentication Error",
            f"Failed to authenticate with Google:\n\n{e}",
        )
        sys.exit(1)

    # Create and show main window
    window = MainWindow(clients)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
