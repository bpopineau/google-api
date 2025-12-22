"""Unit tests for Contacts, Sheets Batch, and Idempotency features."""

from __future__ import annotations

from unittest.mock import MagicMock, patch


class TestContactsCRUD:
    """Tests for Contacts create, update, delete operations."""

    def test_create_contact_builds_correct_request(self):
        """create_contact should build a valid People API request."""
        from mygooglib.services.contacts import create_contact

        mock_service = MagicMock()
        mock_service.people().createContact().execute.return_value = {
            "resourceName": "people/c123",
            "names": [{"displayName": "John Doe", "givenName": "John"}],
            "emailAddresses": [{"value": "john@example.com"}],
        }

        with patch(
            "mygooglib.services.contacts.execute_with_retry_http_error",
            return_value={
                "resourceName": "people/c123",
                "names": [{"displayName": "John Doe"}],
            },
        ):
            result = create_contact(
                mock_service,
                given_name="John",
                family_name="Doe",
                email="john@example.com",
            )

        assert result["resourceName"] == "people/c123"
        assert result["name"] == "John Doe"

    def test_delete_contact_calls_api(self):
        """delete_contact should call the People API deleteContact."""
        from mygooglib.services.contacts import delete_contact

        mock_service = MagicMock()

        with patch(
            "mygooglib.services.contacts.execute_with_retry_http_error", return_value={}
        ):
            delete_contact(mock_service, "people/c123")

        mock_service.people().deleteContact.assert_called_once()


class TestSheetsBatch:
    """Tests for Sheets batch operations."""

    def test_batch_get_multiple_ranges(self):
        """batch_get should return a dict mapping ranges to values."""
        from mygooglib.services.sheets import batch_get

        mock_service = MagicMock()
        mock_response = {
            "valueRanges": [
                {"range": "Sheet1!A1:B2", "values": [[1, 2], [3, 4]]},
                {"range": "Sheet1!C1:D2", "values": [[5, 6], [7, 8]]},
            ]
        }

        with patch(
            "mygooglib.services.sheets.execute_with_retry_http_error",
            return_value=mock_response,
        ):
            result = batch_get(
                mock_service,
                "test_spreadsheet_id_12345678901234567890",
                ["Sheet1!A1:B2", "Sheet1!C1:D2"],
            )

        assert "Sheet1!A1:B2" in result
        assert result["Sheet1!A1:B2"] == [[1, 2], [3, 4]]
        assert "Sheet1!C1:D2" in result

    def test_batch_update_multiple_ranges(self):
        """batch_update should send multiple range updates in one call."""
        from mygooglib.services.sheets import batch_update

        mock_service = MagicMock()
        mock_response = {
            "spreadsheetId": "test_id",
            "totalUpdatedRows": 4,
            "totalUpdatedColumns": 4,
            "totalUpdatedCells": 8,
            "totalUpdatedSheets": 1,
        }

        with patch(
            "mygooglib.services.sheets.execute_with_retry_http_error",
            return_value=mock_response,
        ):
            result = batch_update(
                mock_service,
                "test_spreadsheet_id_12345678901234567890",
                [
                    {"range": "A1:B2", "values": [[1, 2], [3, 4]]},
                    {"range": "C1:D2", "values": [[5, 6], [7, 8]]},
                ],
            )

        assert result["totalUpdatedCells"] == 8
        assert result["totalUpdatedRows"] == 4


class TestIdempotencyStore:
    """Tests for IdempotencyStore and Gmail integration."""

    def test_store_check_and_add(self, tmp_path):
        """IdempotencyStore should track processed keys."""
        from mygooglib.core.utils.idempotency import IdempotencyStore

        db_path = tmp_path / "test_idem.db"
        store = IdempotencyStore(db_path)

        assert store.check("key1") is False
        store.add("key1")
        assert store.check("key1") is True

    def test_store_check_and_add_atomic(self, tmp_path):
        """check_and_add should be atomic."""
        from mygooglib.core.utils.idempotency import IdempotencyStore

        db_path = tmp_path / "test_idem.db"
        store = IdempotencyStore(db_path)

        # First call: item is new
        assert store.check_and_add("key2") is True
        # Second call: item already exists
        assert store.check_and_add("key2") is False

    def test_send_email_with_idempotency_key_skips_duplicate(self, tmp_path):
        """send_email should skip if idempotency_key was already used."""
        from mygooglib.services.gmail import send_email
        from mygooglib.core.utils.idempotency import IdempotencyStore

        # Set up a store with a pre-existing key
        db_path = tmp_path / "test_idem.db"
        store = IdempotencyStore(db_path)
        store.add("existing_key")

        mock_service = MagicMock()

        # Patch the IdempotencyStore at the import location inside gmail.send_email
        with patch(
            "mygooglib.core.utils.idempotency.IdempotencyStore", return_value=store
        ):
            result = send_email(
                mock_service,
                to="test@example.com",
                subject="Test",
                body="Test body",
                idempotency_key="existing_key",
            )

        # Should return None without calling API
        assert result is None
        mock_service.users().messages().send.assert_not_called()
