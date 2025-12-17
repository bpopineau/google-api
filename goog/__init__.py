"""
goog - A Pythonic wrapper for Google APIs.

This library provides intuitive, high-level interfaces for:
- Google Drive (file upload, download, management)
- Google Sheets (spreadsheet reading and writing)
- Google Docs (document creation and editing)
- Google Calendar (event management)
- Google Tasks (to-do list management)
- Gmail (sending and searching emails)
"""

from goog.auth import GoogleAuth
from goog.calendar_client import CalendarClient
from goog.docs import DocsClient
from goog.drive import DriveClient
from goog.gmail import GmailClient
from goog.sheets import SheetsClient
from goog.tasks import TasksClient

__version__ = "0.1.0"

__all__ = [
    "GoogleAuth",
    "DriveClient",
    "SheetsClient",
    "DocsClient",
    "CalendarClient",
    "TasksClient",
    "GmailClient",
    "create_clients",
]


def create_clients(
    credentials_path: str = "credentials.json",
    token_path: str = "token.json",
    scopes: list[str] | None = None,
) -> dict:
    """
    Factory function to create all Google API clients at once.

    Args:
        credentials_path: Path to OAuth credentials JSON file.
        token_path: Path to store/load OAuth tokens.
        scopes: Optional list of API scopes. If None, uses default scopes for all services.

    Returns:
        Dictionary with keys: 'drive', 'sheets', 'docs', 'calendar', 'tasks', 'gmail'
    """
    auth = GoogleAuth(
        credentials_path=credentials_path,
        token_path=token_path,
        scopes=scopes,
    )

    return {
        "drive": DriveClient(auth),
        "sheets": SheetsClient(auth),
        "docs": DocsClient(auth),
        "calendar": CalendarClient(auth),
        "tasks": TasksClient(auth),
        "gmail": GmailClient(auth),
    }
