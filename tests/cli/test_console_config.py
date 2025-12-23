
import pytest
from unittest.mock import patch, MagicMock
from mygooglib.core.client import get_clients

def test_get_clients_respects_config_scopes():
    # Mock AppConfig to return custom scopes
    custom_scopes = ["https://www.googleapis.com/auth/drive.readonly"]
    
    with patch("mygooglib.core.auth.AppConfig") as MockAppConfig:
        # Configure the singleton mock
        instance = MockAppConfig.return_value
        instance.scopes = custom_scopes
        
        with patch("mygooglib.core.auth.Credentials") as MockCreds:
            with patch("mygooglib.core.auth._get_paths") as MockPaths:
                with patch("mygooglib.core.auth.Path.exists") as MockExists:
                    # Mock paths and existence of token.json
                    MockPaths.return_value = (MagicMock(), MagicMock())
                    MockExists.return_value = True
                    
                    # Mock Credentials.from_authorized_user_file to return a valid mock
                    mock_creds_instance = MagicMock()
                    mock_creds_instance.valid = True
                    MockCreds.from_authorized_user_file.return_value = mock_creds_instance
                    
                    # Call get_clients()
                    get_clients(use_cache=False)
                    
                    # Verify that Credentials.from_authorized_user_file was called with custom_scopes
                    MockCreds.from_authorized_user_file.assert_called_once()
                    args, kwargs = MockCreds.from_authorized_user_file.call_args
                    assert kwargs["scopes"] == custom_scopes

def test_get_clients_uses_default_scopes_when_config_none():
    from mygooglib.core.auth import SCOPES
    
    with patch("mygooglib.core.auth.AppConfig") as MockAppConfig:
        instance = MockAppConfig.return_value
        instance.scopes = None
        
        with patch("mygooglib.core.auth.Credentials") as MockCreds:
            with patch("mygooglib.core.auth._get_paths") as MockPaths:
                with patch("mygooglib.core.auth.Path.exists") as MockExists:
                    MockPaths.return_value = (MagicMock(), MagicMock())
                    MockExists.return_value = True
                    
                    mock_creds_instance = MagicMock()
                    mock_creds_instance.valid = True
                    MockCreds.from_authorized_user_file.return_value = mock_creds_instance
                    
                    get_clients(use_cache=False)
                    
                    MockCreds.from_authorized_user_file.assert_called_once()
                    args, kwargs = MockCreds.from_authorized_user_file.call_args
                    assert kwargs["scopes"] == SCOPES
