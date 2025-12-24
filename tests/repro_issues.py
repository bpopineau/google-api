import os
import sys

import pytest

sys.path.append(os.getcwd())

from tests.factories.gmail import MessageFactory, ThreadFactory


def test_message_factory_nested_override():
    """Attempt to override a nested field (payload) in MessageFactory."""
    # User expects to be able to override fields within the nested payload
    # Or at least replace the payload.

    # Case 1: Replace entire payload
    custom_payload = {
        "mimeType": "application/json",
        "partId": "99",
        "filename": "test.json",
        "body": {"size": 10},
        "parts": [],
    }
    msg_replaced = MessageFactory.build(payload=custom_payload)

    # If this fails (ignores override), msg_replaced['payload']['mimeType'] will be "text/plain" (default)
    print(f"\nDEBUG: Replaced Payload MimeType: {msg_replaced['payload']['mimeType']}")
    assert msg_replaced["payload"]["mimeType"] == "application/json", (
        "Failed to replace payload"
    )


def test_thread_factory_list_generation():
    """Attempt to generate a ThreadDict with messages list."""
    # User reports TypeError or failure to generate list
    try:
        thread = ThreadFactory.build()
        print(f"\nDEBUG: Thread Messages Type: {type(thread['messages'])}")
        print(f"DEBUG: Thread Messages Content: {thread['messages']}")

        assert isinstance(thread["messages"], list), "Messages should be a list"
        assert len(thread["messages"]) > 0, "Messages list should not be empty"
        assert "id" in thread["messages"][0], "Message in list should have an id"
    except Exception as e:
        pytest.fail(f"ThreadFactory.build() failed: {e}")


if __name__ == "__main__":
    # Manually run if executed as script
    try:
        test_message_factory_nested_override()
        print("test_message_factory_nested_override PASSED")
    except AssertionError as e:
        print(f"test_message_factory_nested_override FAILED: {e}")

    try:
        test_thread_factory_list_generation()
        print("test_thread_factory_list_generation PASSED")
    except Exception as e:
        print(f"test_thread_factory_list_generation FAILED: {e}")
