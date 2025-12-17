"""Client factory — build all service wrappers from a single set of credentials."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from googleapiclient.discovery import Resource, build

from mygooglib.auth import get_creds
from mygooglib.utils.logging import configure_from_env

if TYPE_CHECKING:
    from google.oauth2.credentials import Credentials


@dataclass
class Clients:
    """Container holding all Google API service wrappers."""

    drive: Resource
    sheets: Resource
    # docs: Resource  # TODO: add when Docs wrapper is implemented
    # calendar: Resource
    # tasks: Resource
    gmail: Resource


_DEFAULT_CLIENTS: Clients | None = None


def get_clients(
    creds: "Credentials | None" = None, *, use_cache: bool = True
) -> Clients:
    """Build and return all Google API service objects.

    Args:
        creds: Optional pre-loaded credentials. If None, calls get_creds().
        use_cache: If True (default) and creds is None, cache and reuse the
            built service objects within the current Python process.

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
        creds = get_creds()

    clients = Clients(
        drive=build("drive", "v3", credentials=creds),
        sheets=build("sheets", "v4", credentials=creds),
        gmail=build("gmail", "v1", credentials=creds),
    )

    if use_cache and is_default_creds:
        _DEFAULT_CLIENTS = clients

    return clients
