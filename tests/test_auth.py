"""Unit tests for mygooglib.auth module."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from mygooglib.auth import SCOPES, get_auth_paths, get_creds


class TestGetAuthPaths:
    """Tests for get_auth_paths function."""

    def test_returns_tuple_of_paths(self):
        """Should return a tuple of two Path objects."""
        creds_path, token_path = get_auth_paths()
        assert isinstance(creds_path, Path)
        assert isinstance(token_path, Path)
        assert creds_path.name == "credentials.json"
        assert token_path.name == "token.json"

    def test_respects_mygooglib_credentials_path_env(self, tmp_path, monkeypatch):
        """Should use MYGOOGLIB_CREDENTIALS_PATH if set."""
        custom_path = tmp_path / "custom_creds.json"
        monkeypatch.setenv("MYGOOGLIB_CREDENTIALS_PATH", str(custom_path))
        creds_path, _ = get_auth_paths()
        assert creds_path == custom_path

    def test_respects_mygooglib_token_path_env(self, tmp_path, monkeypatch):
        """Should use MYGOOGLIB_TOKEN_PATH if set."""
        custom_path = tmp_path / "custom_token.json"
        monkeypatch.setenv("MYGOOGLIB_TOKEN_PATH", str(custom_path))
        _, token_path = get_auth_paths()
        assert token_path == custom_path


class TestGetCreds:
    """Tests for get_creds function."""

    def test_raises_file_not_found_if_no_token_and_no_credentials(
        self, tmp_path, monkeypatch
    ):
        """Should raise FileNotFoundError if credentials.json is missing."""
        monkeypatch.setenv("MYGOOGLIB_CREDENTIALS_PATH", str(tmp_path / "missing.json"))
        monkeypatch.setenv("MYGOOGLIB_TOKEN_PATH", str(tmp_path / "token.json"))

        with pytest.raises(FileNotFoundError, match="OAuth client file not found"):
            get_creds()

    def test_returns_valid_cached_credentials(self, tmp_path, monkeypatch):
        """Should return cached credentials if token is valid."""
        # Create a mock token file
        token_path = tmp_path / "token.json"
        mock_token = {
            "token": "mock_access_token",
            "refresh_token": "mock_refresh_token",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": "mock_client_id",
            "client_secret": "mock_client_secret",
            "scopes": SCOPES,
        }
        token_path.write_text(json.dumps(mock_token), encoding="utf-8")

        monkeypatch.setenv("MYGOOGLIB_TOKEN_PATH", str(token_path))
        monkeypatch.setenv("MYGOOGLIB_CREDENTIALS_PATH", str(tmp_path / "creds.json"))

        # Mock the Credentials to appear valid
        with patch(
            "mygooglib.auth.Credentials.from_authorized_user_file"
        ) as mock_from_file:
            mock_creds = MagicMock()
            mock_creds.valid = True
            mock_creds.expired = False
            mock_from_file.return_value = mock_creds

            result = get_creds()
            assert result == mock_creds
            mock_from_file.assert_called_once()

    def test_refreshes_expired_token(self, tmp_path, monkeypatch):
        """Should refresh token if expired but has refresh_token."""
        token_path = tmp_path / "token.json"
        mock_token = {
            "token": "expired_token",
            "refresh_token": "valid_refresh",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": "mock_client_id",
            "client_secret": "mock_client_secret",
            "scopes": SCOPES,
        }
        token_path.write_text(json.dumps(mock_token), encoding="utf-8")

        monkeypatch.setenv("MYGOOGLIB_TOKEN_PATH", str(token_path))
        monkeypatch.setenv("MYGOOGLIB_CREDENTIALS_PATH", str(tmp_path / "creds.json"))

        with patch(
            "mygooglib.auth.Credentials.from_authorized_user_file"
        ) as mock_from_file:
            mock_creds = MagicMock()
            mock_creds.valid = False
            mock_creds.expired = True
            mock_creds.refresh_token = "valid_refresh"
            mock_creds.to_json.return_value = '{"refreshed": true}'
            mock_from_file.return_value = mock_creds

            with patch("mygooglib.auth.Request"):
                result = get_creds()

                mock_creds.refresh.assert_called_once()
                assert result == mock_creds


class TestScopes:
    """Tests for SCOPES constant."""

    def test_scopes_is_list(self):
        """SCOPES should be a list of strings."""
        assert isinstance(SCOPES, list)
        assert all(isinstance(s, str) for s in SCOPES)

    def test_scopes_contains_required_apis(self):
        """SCOPES should include Drive, Sheets, Gmail, Calendar, Tasks."""
        scope_prefixes = [s.split("/")[-1] for s in SCOPES]
        required = ["drive", "spreadsheets", "gmail.send", "calendar", "tasks"]
        for req in required:
            assert any(req in s for s in scope_prefixes), f"Missing scope for {req}"
