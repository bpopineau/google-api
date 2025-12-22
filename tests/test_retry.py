"""Unit tests for mygooglib.core.utils.retry module."""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest
from googleapiclient.errors import HttpError


class TestExecuteWithRetry:
    """Tests for execute_with_retry_http_error function."""

    def test_successful_request_returns_result(self):
        """A successful request should return the result without retrying."""
        from mygooglib.core.utils.retry import execute_with_retry_http_error

        mock_request = MagicMock()
        mock_request.execute.return_value = {"status": "ok"}

        result = execute_with_retry_http_error(mock_request)

        assert result == {"status": "ok"}
        assert mock_request.execute.call_count == 1

    def test_retries_on_429_status(self):
        """Should retry on 429 (rate limit) errors."""
        from mygooglib.core.utils.retry import execute_with_retry_http_error

        mock_request = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status = 429

        # First call raises 429, second succeeds
        mock_request.execute.side_effect = [
            HttpError(resp=mock_resp, content=b"Rate limited"),
            {"status": "ok"},
        ]

        with patch("mygooglib.core.utils.retry.time.sleep"):
            result = execute_with_retry_http_error(mock_request, attempts=2)

        assert result == {"status": "ok"}
        assert mock_request.execute.call_count == 2

    def test_retries_on_500_status(self):
        """Should retry on 500 (server error) errors."""
        from mygooglib.core.utils.retry import execute_with_retry_http_error

        mock_request = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status = 500

        mock_request.execute.side_effect = [
            HttpError(resp=mock_resp, content=b"Server error"),
            {"status": "ok"},
        ]

        with patch("mygooglib.core.utils.retry.time.sleep"):
            result = execute_with_retry_http_error(mock_request, attempts=2)

        assert result == {"status": "ok"}
        assert mock_request.execute.call_count == 2

    def test_no_retry_on_400_status(self):
        """Should NOT retry on 400 (client error) - not in retry_statuses."""
        from mygooglib.core.utils.retry import execute_with_retry_http_error

        mock_request = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status = 400

        mock_request.execute.side_effect = HttpError(
            resp=mock_resp, content=b"Bad request"
        )

        with pytest.raises(HttpError):
            execute_with_retry_http_error(mock_request, attempts=3)

        # Should only attempt once since 400 is not retryable
        assert mock_request.execute.call_count == 1

    def test_write_operations_default_to_one_attempt(self):
        """Write operations should default to 1 attempt to prevent duplicates."""
        from mygooglib.core.utils.retry import execute_with_retry_http_error

        mock_request = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status = 429

        mock_request.execute.side_effect = HttpError(
            resp=mock_resp, content=b"Rate limited"
        )

        with pytest.raises(HttpError):
            execute_with_retry_http_error(mock_request, is_write=True)

        # Default write attempts is 1, so no retry
        assert mock_request.execute.call_count == 1

    def test_exhausted_retries_raises_error(self):
        """Should raise the error after exhausting all retries."""
        from mygooglib.core.utils.retry import execute_with_retry_http_error

        mock_request = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status = 503

        mock_request.execute.side_effect = HttpError(
            resp=mock_resp, content=b"Service unavailable"
        )

        with patch("mygooglib.core.utils.retry.time.sleep"):
            with pytest.raises(HttpError):
                execute_with_retry_http_error(mock_request, attempts=3)

        assert mock_request.execute.call_count == 3


class TestRetryAfterHeader:
    """Tests for Retry-After header parsing."""

    def test_respects_retry_after_header(self):
        """Should use Retry-After header value for backoff when present."""
        from mygooglib.core.utils.retry import execute_with_retry_http_error

        mock_request = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status = 429
        mock_resp.get = MagicMock(return_value="5")  # 5 seconds

        mock_request.execute.side_effect = [
            HttpError(resp=mock_resp, content=b"Rate limited"),
            {"status": "ok"},
        ]

        with patch("mygooglib.core.utils.retry.time.sleep") as mock_sleep:
            result = execute_with_retry_http_error(mock_request, attempts=2)

        assert result == {"status": "ok"}
        # Sleep should be called with a value based on 5 seconds (with jitter)
        sleep_call = mock_sleep.call_args[0][0]
        assert 4.0 < sleep_call < 6.0  # Expecting ~5s with jitter


class TestEnvConfiguration:
    """Tests for environment variable configuration."""

    def test_retry_disabled_via_env(self):
        """MYGOOGLIB_RETRY_ENABLED=0 should disable retries."""
        from mygooglib.core.utils.retry import execute_with_retry_http_error

        mock_request = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status = 429

        mock_request.execute.side_effect = HttpError(
            resp=mock_resp, content=b"Rate limited"
        )

        with patch.dict(os.environ, {"MYGOOGLIB_RETRY_ENABLED": "0"}):
            with pytest.raises(HttpError):
                execute_with_retry_http_error(mock_request)

        # With retry disabled, only 1 attempt
        assert mock_request.execute.call_count == 1


class TestEnvHelpers:
    """Tests for environment variable helper functions."""

    def test_env_bool_true_values(self):
        """_env_bool should recognize various true values."""
        from mygooglib.core.utils.retry import _env_bool

        with patch.dict(os.environ, {"TEST_VAR": "1"}):
            assert _env_bool("TEST_VAR", False) is True

        with patch.dict(os.environ, {"TEST_VAR": "true"}):
            assert _env_bool("TEST_VAR", False) is True

        with patch.dict(os.environ, {"TEST_VAR": "yes"}):
            assert _env_bool("TEST_VAR", False) is True

    def test_env_bool_false_values(self):
        """_env_bool should return default for unset or false values."""
        from mygooglib.core.utils.retry import _env_bool

        with patch.dict(os.environ, {"TEST_VAR": "0"}):
            assert _env_bool("TEST_VAR", True) is False

        with patch.dict(os.environ, {}, clear=False):
            # Unset variable returns default
            result = _env_bool("UNSET_VAR_12345", True)
            assert result is True

    def test_env_int_valid(self):
        """_env_int should parse valid integers."""
        from mygooglib.core.utils.retry import _env_int

        with patch.dict(os.environ, {"TEST_INT": "42"}):
            assert _env_int("TEST_INT", 0) == 42

    def test_env_int_invalid_returns_default(self):
        """_env_int should return default for invalid values."""
        from mygooglib.core.utils.retry import _env_int

        with patch.dict(os.environ, {"TEST_INT": "not_a_number"}):
            assert _env_int("TEST_INT", 99) == 99

    def test_env_float_valid(self):
        """_env_float should parse valid floats."""
        from mygooglib.core.utils.retry import _env_float

        with patch.dict(os.environ, {"TEST_FLOAT": "3.14"}):
            assert _env_float("TEST_FLOAT", 0.0) == 3.14


