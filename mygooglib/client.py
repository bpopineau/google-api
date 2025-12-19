"""Client factory — build all service wrappers from a single set of credentials."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from googleapiclient.discovery import build

from mygooglib.appscript import AppScriptClient
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
    """Container holding all Google API service wrappers.

    All clients are lazily loaded on first access for performance.
    """

    _creds: "Credentials"

    def _get_or_build(
        self,
        attr_name: str,
        api_name: str,
        version: str,
        client_class: type,
        needs_drive: bool = False,
    ):
        """Helper to lazily build and cache a client."""
        cached = getattr(self, f"_{attr_name}", None)
        if cached is None:
            service = build(api_name, version, credentials=self._creds)
            if needs_drive:
                drive_service = build("drive", "v3", credentials=self._creds)
                cached = client_class(service, drive=drive_service)
            else:
                cached = client_class(service)
            object.__setattr__(self, f"_{attr_name}", cached)
        return cached

    @property
    def drive(self) -> DriveClient:
        return self._get_or_build("drive", "drive", "v3", DriveClient)

    @property
    def sheets(self) -> SheetsClient:
        return self._get_or_build(
            "sheets", "sheets", "v4", SheetsClient, needs_drive=True
        )

    @property
    def docs(self) -> DocsClient:
        return self._get_or_build("docs", "docs", "v1", DocsClient, needs_drive=True)

    @property
    def calendar(self) -> CalendarClient:
        return self._get_or_build("calendar", "calendar", "v3", CalendarClient)

    @property
    def tasks(self) -> TasksClient:
        return self._get_or_build("tasks", "tasks", "v1", TasksClient)

    @property
    def gmail(self) -> GmailClient:
        return self._get_or_build("gmail", "gmail", "v1", GmailClient)

    @property
    def contacts(self) -> ContactsClient:
        return self._get_or_build("contacts", "people", "v1", ContactsClient)

    @property
    def appscript(self) -> AppScriptClient:
        return self._get_or_build("appscript", "script", "v1", AppScriptClient)


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
