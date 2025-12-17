"""Client factory — build all service wrappers from a single set of credentials."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from googleapiclient.discovery import Resource, build

from mygooglib.auth import get_creds

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


def get_clients(creds: "Credentials | None" = None) -> Clients:
    """Build and return all Google API service objects.

    Args:
        creds: Optional pre-loaded credentials. If None, calls get_creds().

    Returns:
        Clients dataclass with .drive, .sheets, .gmail, etc.
    """
    if creds is None:
        creds = get_creds()

    return Clients(
        drive=build("drive", "v3", credentials=creds),
        sheets=build("sheets", "v4", credentials=creds),
        gmail=build("gmail", "v1", credentials=creds),
    )
