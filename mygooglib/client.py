"""Client factory — build all service wrappers from a single set of credentials."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from googleapiclient.discovery import build

from mygooglib.auth import get_creds
from mygooglib.calendar import CalendarClient
from mygooglib.docs import DocsClient
from mygooglib.drive import DriveClient
from mygooglib.gmail import GmailClient
from mygooglib.sheets import SheetsClient
from mygooglib.tasks import TasksClient
from mygooglib.utils.logging import configure_from_env

if TYPE_CHECKING:
    from google.oauth2.credentials import Credentials


@dataclass
class Clients:
    """Container holding all Google API service wrappers."""

    drive: DriveClient
    sheets: SheetsClient
    docs: DocsClient
    calendar: CalendarClient
    tasks: TasksClient
    gmail: GmailClient


_DEFAULT_CLIENTS: Clients | None = None


def get_clients(
    creds: "Credentials | None" = None,
    *,
    use_cache: bool = True,
    scopes: list[str] | None = None,
) -> Clients:
    """Build and return all Google API service objects.

    Args:
        creds: Optional pre-loaded credentials. If None, calls get_creds().
        use_cache: If True (default) and creds is None, cache and reuse the
            built service objects within the current Python process.
        scopes: Optional list of scopes to request if creds is None.

    Returns:
        Clients dataclass with .drive, .sheets, .gmail, etc.
    """
    global _DEFAULT_CLIENTS

    # Opt-in debug logging via env vars.
    configure_from_env()

    is_default_creds = creds is None

    if is_default_creds and use_cache and _DEFAULT_CLIENTS is not None:
        return _DEFAULT_CLIENTS

    if creds is None:
        creds = get_creds(scopes=scopes)

    drive_service = build("drive", "v3", credentials=creds)
    sheets_service = build("sheets", "v4", credentials=creds)
    docs_service = build("docs", "v1", credentials=creds)
    gmail_service = build("gmail", "v1", credentials=creds)
    calendar_service = build("calendar", "v3", credentials=creds)
    tasks_service = build("tasks", "v1", credentials=creds)

    clients = Clients(
        drive=DriveClient(drive_service),
        sheets=SheetsClient(sheets_service, drive=drive_service),
        docs=DocsClient(docs_service, drive=drive_service),
        calendar=CalendarClient(calendar_service),
        tasks=TasksClient(tasks_service),
        gmail=GmailClient(gmail_service),
    )

    if use_cache and is_default_creds:
        _DEFAULT_CLIENTS = clients

    return clients
