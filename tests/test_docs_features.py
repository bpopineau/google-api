import unittest
from unittest.mock import MagicMock

from mygooglib.services.docs import find_replace


class TestDocsFindReplace(unittest.TestCase):
    def test_find_replace_calls_batch_update(self):
        # Setup mock
        mock_docs = MagicMock()
        mock_docs.documents().batchUpdate.return_value.execute.return_value = {
            "replies": [
                {"replaceAllText": {"occurrencesChanged": 2}},
                {"replaceAllText": {"occurrencesChanged": 3}},
            ]
        }

        # Call function
        count = find_replace(
            mock_docs, "doc-123", {"old1": "new1", "old2": "new2"}, match_case=False
        )

        # Verify result
        self.assertEqual(count, 5)

        # Verify API call structure
        mock_docs.documents().batchUpdate.assert_called_once()
        call_kwargs = mock_docs.documents().batchUpdate.call_args[1]
        self.assertEqual(call_kwargs["documentId"], "doc-123")

        requests = call_kwargs["body"]["requests"]
        self.assertEqual(len(requests), 2)

        # Check first replacement logic
        req1 = requests[0]["replaceAllText"]
        self.assertEqual(req1["containsText"]["text"], "old1")
        self.assertEqual(req1["containsText"]["matchCase"], False)
        self.assertEqual(req1["replaceText"], "new1")

    def test_find_replace_empty_does_nothing(self):
        mock_docs = MagicMock()
        count = find_replace(mock_docs, "doc-123", {})
        self.assertEqual(count, 0)
        mock_docs.documents().batchUpdate.assert_not_called()


if __name__ == "__main__":
    unittest.main()
