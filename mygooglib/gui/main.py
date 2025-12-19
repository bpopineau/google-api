"""Main application window for the PySide6 GUI."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QThread, Signal
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

from mygooglib.auth import verify_creds_exist
from mygooglib.config import AppConfig
from mygooglib.gui.pages.settings import SettingsPage
from mygooglib.gui.styles import STYLESHEET
from mygooglib.gui.widgets.sidebar import Sidebar

if TYPE_CHECKING:
    from mygooglib.client import Clients


class AsyncLoginWorker(QThread):
    """Background worker to handle authentication without freezing UI."""

    finished = Signal(object)  # Emits Clients object on success
    error = Signal(str)  # Emits error message on failure

    def run(self) -> None:
        try:
            # This can block safely here
            from mygooglib import get_clients

            clients = get_clients()
            self.finished.emit(clients)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation."""

    def __init__(self, clients: "Clients | None" = None) -> None:
        super().__init__()
        self.config = AppConfig()
        self.clients = clients

        self.setWindowTitle("MyGoog - Google Workspace Manager")
        self._restore_geometry()

        self._pages: dict[str, QWidget] = {}
        self._setup_ui()

    def _restore_geometry(self) -> None:
        """Apply saved window geometry."""
        geo = self.config.window_geometry
        if len(geo) == 4:
            x, y, w, h = geo
            self.setGeometry(x, y, w, h)
        else:
            self.resize(1200, 800)

    def closeEvent(self, event) -> None:
        """Save geometry on close."""
        rect = self.geometry()
        self.config.window_geometry = [rect.x(), rect.y(), rect.width(), rect.height()]
        super().closeEvent(event)

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

        # If we have clients, load pages. If not, show loading/auth placeholder.
        if self.clients:
            self._init_authenticated_state()
        else:
            self._init_loading_state()

    def _init_authenticated_state(self) -> None:
        """Initialize the full UI once authenticated."""
        self._create_pages()

        # Load default view from config
        default = self.config.default_view
        if default in self._pages:
            self.sidebar.select_page(default)
        else:
            self.sidebar.select_page("home")

    def _init_loading_state(self) -> None:
        """Show a loading placeholder while auth happens."""
        loader = QWidget()
        l_layout = QVBoxLayout(loader)
        l_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel("Authenticating...")
        lbl.setStyleSheet("font-size: 24px; color: #888;")
        l_layout.addWidget(lbl)

        self.stack.addWidget(loader)
        self.stack.setCurrentWidget(loader)

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
        """Create the settings page."""
        return SettingsPage(self.clients)

    def _on_page_changed(self, name: str) -> None:
        """Handle page navigation."""
        if name in self._pages:
            self.stack.setCurrentWidget(self._pages[name])


def run_app() -> None:
    """Run the PySide6 application."""
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)

    # 1. Initial Checks
    verify_creds_exist()

    # 2. Show Window Immediately
    # We start with no clients -> Window shows "Loading..." state
    window = MainWindow(clients=None)
    window.show()

    # 3. Start Background Auth
    worker = AsyncLoginWorker()

    def on_auth_success(clients: "Clients") -> None:
        window.clients = clients
        window._init_authenticated_state()

    def on_auth_error(err: str) -> None:
        QMessageBox.critical(
            window,
            "Authentication Error",
            f"Failed to authenticate:\n\n{err}\n\nPlease check your internet connection.",
        )
        # We might want to show a "Retry" button in the UI instead of closing,
        # but for now, let's keep it simple.

    worker.finished.connect(on_auth_success)
    worker.error.connect(on_auth_error)

    # Keep reference to avoid GC
    window._auth_worker = worker  # type: ignore
    worker.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
