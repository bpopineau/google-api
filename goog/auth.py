"""
Authentication module for Google APIs.

Handles OAuth2 flow, token persistence, and service creation.
"""

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build

from goog.utils import logger

# Default scopes for all supported services
DEFAULT_SCOPES = [
    # Drive - full access to files
    "https://www.googleapis.com/auth/drive",
    # Sheets - full access to spreadsheets
    "https://www.googleapis.com/auth/spreadsheets",
    # Docs - full access to documents
    "https://www.googleapis.com/auth/documents",
    # Calendar - full access to calendar
    "https://www.googleapis.com/auth/calendar",
    # Tasks - full access to tasks
    "https://www.googleapis.com/auth/tasks",
    # Gmail - full access (send, read, modify)
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
]


class GoogleAuth:
    """
    Handles OAuth2 authentication for Google APIs.

    This class manages the OAuth flow, token persistence, and creation
    of authorized Google API service objects.

    Example:
        >>> auth = GoogleAuth()
        >>> drive_service = auth.build_service("drive", "v3")
        >>> # Now use drive_service to make API calls
    """

    def __init__(
        self,
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
        scopes: list[str] | None = None,
    ):
        """
        Initialize the authentication handler.

        Args:
            credentials_path: Path to the OAuth credentials JSON file
                             downloaded from Google Cloud Console.
            token_path: Path where the OAuth token will be saved/loaded.
            scopes: List of API scopes to request. If None, uses default
                   scopes for all supported services.
        """
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)
        self.scopes = scopes or DEFAULT_SCOPES
        self._credentials: Credentials | None = None
        self._services: dict[str, Resource] = {}

    def get_credentials(self) -> Credentials:
        """
        Get valid OAuth credentials, running the auth flow if needed.

        This method:
        1. Loads existing token from token_path if available
        2. Refreshes expired tokens automatically
        3. Runs the browser-based OAuth flow for new authentication

        Returns:
            Valid Google OAuth2 credentials.

        Raises:
            FileNotFoundError: If credentials.json is not found and
                              no valid token exists.
        """
        if self._credentials and self._credentials.valid:
            return self._credentials

        creds = None

        # Load existing token if available
        if self.token_path.exists():
            logger.debug(f"Loading existing token from {self.token_path}")
            creds = Credentials.from_authorized_user_file(
                str(self.token_path), self.scopes
            )

        # Refresh or run new auth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing expired token")
                creds.refresh(Request())
            else:
                if not self.credentials_path.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}\n"
                        "Please download OAuth credentials from Google Cloud Console."
                    )

                logger.info("Running OAuth flow - browser will open for authorization")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), self.scopes
                )
                creds = flow.run_local_server(port=0)

            # Save token for future use
            self._save_token(creds)

        self._credentials = creds
        return creds

    def _save_token(self, creds: Credentials) -> None:
        """Save credentials to token file."""
        logger.debug(f"Saving token to {self.token_path}")
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.token_path, "w") as token_file:
            token_file.write(creds.to_json())

    def build_service(self, api: str, version: str) -> Resource:
        """
        Build an authorized Google API service object.

        Service objects are cached, so calling this multiple times
        with the same arguments returns the same object.

        Args:
            api: The API name (e.g., 'drive', 'sheets', 'gmail').
            version: The API version (e.g., 'v3', 'v4', 'v1').

        Returns:
            An authorized Google API service object.

        Example:
            >>> auth = GoogleAuth()
            >>> drive = auth.build_service("drive", "v3")
            >>> sheets = auth.build_service("sheets", "v4")
        """
        cache_key = f"{api}:{version}"

        if cache_key not in self._services:
            creds = self.get_credentials()
            logger.debug(f"Building service for {api} {version}")
            self._services[cache_key] = build(api, version, credentials=creds)

        return self._services[cache_key]

    def revoke(self) -> None:
        """
        Revoke current credentials and delete token file.

        Call this to force re-authentication on next use.
        """
        if self.token_path.exists():
            os.remove(self.token_path)
            logger.info(f"Removed token file: {self.token_path}")

        self._credentials = None
        self._services.clear()
