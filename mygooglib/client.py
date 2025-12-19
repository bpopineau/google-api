"""Client factory — build all service wrappers from a single set of credentials."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from googleapiclient.discovery import build

from mygooglib.auth import get_creds
from mygooglib.calendar import CalendarClient
from mygooglib.contacts import ContactsClient
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

    _creds: "Credentials"
    _drive: DriveClient | None = None
    _sheets: SheetsClient | None = None
    _docs: DocsClient | None = None
    _calendar: CalendarClient | None = None
    _tasks: TasksClient | None = None
    _gmail: GmailClient | None = None
    _contacts: ContactsClient | None = None

    @property
    def drive(self) -> DriveClient:
        if self._drive is None:
            service = build("drive", "v3", credentials=self._creds)
            self._drive = DriveClient(service)
        return self._drive

    @property
    def sheets(self) -> SheetsClient:
        if self._sheets is None:
            # Note: Sheets client needs the raw drive service for some operations
            drive_service = build("drive", "v3", credentials=self._creds)
            service = build("sheets", "v4", credentials=self._creds)
            self._sheets = SheetsClient(service, drive=drive_service)
        return self._sheets

    @property
    def docs(self) -> DocsClient:
        if self._docs is None:
            drive_service = build("drive", "v3", credentials=self._creds)
            service = build("docs", "v1", credentials=self._creds)
            self._docs = DocsClient(service, drive=drive_service)
        return self._docs

    @property
    def calendar(self) -> CalendarClient:
        if self._calendar is None:
            service = build("calendar", "v3", credentials=self._creds)
            self._calendar = CalendarClient(service)
        return self._calendar

    @property
    def tasks(self) -> TasksClient:
        if self._tasks is None:
            service = build("tasks", "v1", credentials=self._creds)
            self._tasks = TasksClient(service)
        return self._tasks

    @property
    def gmail(self) -> GmailClient:
        if self._gmail is None:
            service = build("gmail", "v1", credentials=self._creds)
            self._gmail = GmailClient(service)
        return self._gmail

    @property
    def contacts(self) -> ContactsClient:
        if self._contacts is None:
            service = build("people", "v1", credentials=self._creds)
            self._contacts = ContactsClient(service)
        return self._contacts


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

    # Prevent indefinite hangs on network/auth issues
    import socket

    socket.setdefaulttimeout(60)

    is_default_creds = creds is None

    if is_default_creds and use_cache and _DEFAULT_CLIENTS is not None:
        return _DEFAULT_CLIENTS

    if creds is None:
        creds = get_creds(scopes=scopes)

    clients = Clients(_creds=creds)

    if use_cache and is_default_creds:
        _DEFAULT_CLIENTS = clients

    return clients
