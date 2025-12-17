"""
Gmail API wrapper.

Provides a Pythonic interface for email operations.
"""

import base64
import mimetypes
import os
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from goog.auth import GoogleAuth
from goog.utils import logger, with_retry


class GmailClient:
    """
    Pythonic wrapper for Gmail API.

    Provides intuitive methods for email operations:
    - Send emails with attachments
    - Search and read messages
    - Mark messages as read/unread
    - Download attachments

    Example:
        >>> from goog import GoogleAuth, GmailClient
        >>> auth = GoogleAuth()
        >>> gmail = GmailClient(auth)
        >>> gmail.send_email(
        ...     to="friend@example.com",
        ...     subject="Hello!",
        ...     body="How are you?"
        ... )
    """

    def __init__(self, auth: GoogleAuth):
        """
        Initialize the Gmail client.

        Args:
            auth: GoogleAuth instance for authentication.
        """
        self._auth = auth
        self._service = None

    @property
    def service(self):
        """Lazily initialize and return the Gmail service."""
        if self._service is None:
            self._service = self._auth.build_service("gmail", "v1")
        return self._service

    @with_retry()
    def send_email(
        self,
        to: str | list[str],
        subject: str,
        body: str,
        cc: str | list[str] | None = None,
        bcc: str | list[str] | None = None,
        attachments: list[str | Path] | None = None,
        html: bool = False,
    ) -> str:
        """
        Send an email.

        Args:
            to: Recipient email(s).
            subject: Email subject.
            body: Email body (plain text or HTML).
            cc: Optional CC recipient(s).
            bcc: Optional BCC recipient(s).
            attachments: Optional list of file paths to attach.
            html: If True, body is treated as HTML.

        Returns:
            The sent message ID.

        Example:
            >>> msg_id = gmail.send_email(
            ...     to="friend@example.com",
            ...     subject="Report",
            ...     body="Please see attached.",
            ...     attachments=["report.pdf"]
            ... )
        """
        # Create message
        msg = EmailMessage()
        msg["To"] = ", ".join(to) if isinstance(to, list) else to
        msg["Subject"] = subject

        if cc:
            msg["Cc"] = ", ".join(cc) if isinstance(cc, list) else cc
        if bcc:
            msg["Bcc"] = ", ".join(bcc) if isinstance(bcc, list) else bcc

        # Set body
        if html:
            msg.set_content(body, subtype="html")
        else:
            msg.set_content(body)

        # Add attachments
        if attachments:
            for file_path in attachments:
                file_path = Path(file_path)
                if not file_path.exists():
                    raise FileNotFoundError(f"Attachment not found: {file_path}")

                mime_type = mimetypes.guess_type(str(file_path))[0]
                if mime_type is None:
                    mime_type = "application/octet-stream"

                maintype, subtype = mime_type.split("/", 1)

                with open(file_path, "rb") as f:
                    data = f.read()

                msg.add_attachment(
                    data,
                    maintype=maintype,
                    subtype=subtype,
                    filename=file_path.name,
                )

        # Encode and send
        encoded_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")

        logger.info(f"Sending email to {to}: {subject}")
        result = (
            self.service.users()
            .messages()
            .send(userId="me", body={"raw": encoded_message})
            .execute()
        )

        msg_id = result.get("id")
        logger.debug(f"Sent message with ID: {msg_id}")
        return msg_id

    @with_retry()
    def search_messages(
        self,
        query: str,
        max_results: int = 100,
        include_spam_trash: bool = False,
    ) -> list["GmailMessage"]:
        """
        Search for messages using Gmail query syntax.

        Args:
            query: Gmail search query (e.g., "is:unread from:boss").
            max_results: Maximum messages to return.
            include_spam_trash: Include spam and trash folders.

        Returns:
            List of GmailMessage objects.

        Example:
            >>> messages = gmail.search_messages("is:unread")
            >>> for msg in messages:
            ...     print(msg.subject, msg.sender)
        """
        logger.debug(f"Searching messages: {query}")

        all_messages = []
        page_token = None

        while len(all_messages) < max_results:
            result = (
                self.service.users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    maxResults=min(max_results - len(all_messages), 100),
                    pageToken=page_token,
                    includeSpamTrash=include_spam_trash,
                )
                .execute()
            )

            messages = result.get("messages", [])
            for msg_ref in messages:
                msg = GmailMessage(self, msg_ref["id"])
                all_messages.append(msg)

            page_token = result.get("nextPageToken")
            if not page_token or len(all_messages) >= max_results:
                break

        logger.info(f"Found {len(all_messages)} messages")
        return all_messages

    @with_retry()
    def get_message(self, message_id: str) -> "GmailMessage":
        """
        Get a specific message by ID.

        Args:
            message_id: The message ID.

        Returns:
            GmailMessage object.
        """
        return GmailMessage(self, message_id)

    @with_retry()
    def get_labels(self) -> list[dict]:
        """
        Get all labels in the mailbox.

        Returns:
            List of label dictionaries.
        """
        result = self.service.users().labels().list(userId="me").execute()
        return result.get("labels", [])

    @with_retry()
    def create_label(self, name: str) -> str:
        """
        Create a new label.

        Args:
            name: Label name.

        Returns:
            The label ID.
        """
        logger.info(f"Creating label: {name}")
        result = (
            self.service.users()
            .labels()
            .create(
                userId="me",
                body={
                    "name": name,
                    "labelListVisibility": "labelShow",
                    "messageListVisibility": "show",
                },
            )
            .execute()
        )
        return result.get("id")


class GmailMessage:
    """
    Represents a Gmail message with convenient accessors.

    Provides easy access to message properties and methods
    for common operations like marking as read or downloading attachments.
    """

    def __init__(self, client: GmailClient, message_id: str):
        """
        Initialize a GmailMessage.

        Args:
            client: The GmailClient for API calls.
            message_id: The message ID.
        """
        self._client = client
        self._id = message_id
        self._data: dict | None = None

    @property
    def id(self) -> str:
        """The message ID."""
        return self._id

    def _load_data(self) -> dict:
        """Load full message data on first access."""
        if self._data is None:
            self._data = (
                self._client.service.users()
                .messages()
                .get(userId="me", id=self._id, format="full")
                .execute()
            )
        return self._data

    def _get_header(self, name: str) -> str | None:
        """Get a header value by name."""
        data = self._load_data()
        headers = data.get("payload", {}).get("headers", [])
        for header in headers:
            if header.get("name", "").lower() == name.lower():
                return header.get("value")
        return None

    @property
    def subject(self) -> str:
        """Email subject."""
        return self._get_header("Subject") or ""

    @property
    def sender(self) -> str:
        """Email sender (From header)."""
        return self._get_header("From") or ""

    @property
    def to(self) -> str:
        """Email recipient (To header)."""
        return self._get_header("To") or ""

    @property
    def date(self) -> str:
        """Email date."""
        return self._get_header("Date") or ""

    @property
    def snippet(self) -> str:
        """Short preview of the message."""
        return self._load_data().get("snippet", "")

    @property
    def labels(self) -> list[str]:
        """List of label IDs on this message."""
        return self._load_data().get("labelIds", [])

    @property
    def is_unread(self) -> bool:
        """Whether the message is unread."""
        return "UNREAD" in self.labels

    def get_body(self, prefer_html: bool = False) -> str:
        """
        Get the message body.

        Args:
            prefer_html: If True, return HTML version if available.

        Returns:
            Message body text.
        """
        data = self._load_data()
        payload = data.get("payload", {})

        def find_body(part: dict, content_type: str) -> str | None:
            """Recursively find body with given content type."""
            part_mime = part.get("mimeType", "")

            if part_mime == content_type:
                body_data = part.get("body", {}).get("data")
                if body_data:
                    return base64.urlsafe_b64decode(body_data).decode("utf-8")

            # Check parts recursively
            for subpart in part.get("parts", []):
                result = find_body(subpart, content_type)
                if result:
                    return result
            return None

        # Try to find preferred content type first
        if prefer_html:
            html = find_body(payload, "text/html")
            if html:
                return html

        # Try plain text
        plain = find_body(payload, "text/plain")
        if plain:
            return plain

        # Fall back to HTML if no plain text
        html = find_body(payload, "text/html")
        if html:
            return html

        return ""

    @with_retry()
    def mark_read(self) -> None:
        """Mark the message as read."""
        logger.debug(f"Marking message as read: {self._id}")
        self._client.service.users().messages().modify(
            userId="me",
            id=self._id,
            body={"removeLabelIds": ["UNREAD"]},
        ).execute()

    @with_retry()
    def mark_unread(self) -> None:
        """Mark the message as unread."""
        logger.debug(f"Marking message as unread: {self._id}")
        self._client.service.users().messages().modify(
            userId="me",
            id=self._id,
            body={"addLabelIds": ["UNREAD"]},
        ).execute()

    @with_retry()
    def trash(self) -> None:
        """Move the message to trash."""
        logger.info(f"Trashing message: {self._id}")
        self._client.service.users().messages().trash(
            userId="me",
            id=self._id,
        ).execute()

    @with_retry()
    def add_label(self, label_id: str) -> None:
        """
        Add a label to the message.

        Args:
            label_id: The label ID to add.
        """
        self._client.service.users().messages().modify(
            userId="me",
            id=self._id,
            body={"addLabelIds": [label_id]},
        ).execute()

    @with_retry()
    def remove_label(self, label_id: str) -> None:
        """
        Remove a label from the message.

        Args:
            label_id: The label ID to remove.
        """
        self._client.service.users().messages().modify(
            userId="me",
            id=self._id,
            body={"removeLabelIds": [label_id]},
        ).execute()

    def get_attachments(self) -> list[dict]:
        """
        Get list of attachments.

        Returns:
            List of attachment info dicts with 'filename', 'mimeType', 'size'.
        """
        data = self._load_data()
        attachments = []

        def find_attachments(part: dict) -> None:
            """Recursively find attachments in message parts."""
            filename = part.get("filename")
            if filename and part.get("body", {}).get("attachmentId"):
                attachments.append(
                    {
                        "filename": filename,
                        "mimeType": part.get("mimeType", ""),
                        "size": part.get("body", {}).get("size", 0),
                        "attachmentId": part["body"]["attachmentId"],
                    }
                )

            for subpart in part.get("parts", []):
                find_attachments(subpart)

        find_attachments(data.get("payload", {}))
        return attachments

    @with_retry()
    def download_attachment(
        self,
        filename: str,
        save_dir: str | Path = ".",
    ) -> Path:
        """
        Download a specific attachment by filename.

        Args:
            filename: Name of the attachment to download.
            save_dir: Directory to save the file.

        Returns:
            Path to the downloaded file.

        Raises:
            FileNotFoundError: If attachment not found.
        """
        attachments = self.get_attachments()
        attachment = None

        for att in attachments:
            if att["filename"] == filename:
                attachment = att
                break

        if not attachment:
            raise FileNotFoundError(f"Attachment not found: {filename}")

        # Download attachment data
        logger.info(f"Downloading attachment: {filename}")
        result = (
            self._client.service.users()
            .messages()
            .attachments()
            .get(
                userId="me",
                messageId=self._id,
                id=attachment["attachmentId"],
            )
            .execute()
        )

        data = base64.urlsafe_b64decode(result["data"])

        # Save to file
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / filename

        with open(save_path, "wb") as f:
            f.write(data)

        logger.debug(f"Saved attachment to: {save_path}")
        return save_path

    def download_all_attachments(self, save_dir: str | Path = ".") -> list[Path]:
        """
        Download all attachments.

        Args:
            save_dir: Directory to save files.

        Returns:
            List of paths to downloaded files.
        """
        attachments = self.get_attachments()
        paths = []

        for att in attachments:
            path = self.download_attachment(att["filename"], save_dir)
            paths.append(path)

        return paths

    def __repr__(self) -> str:
        return f"GmailMessage(id='{self._id}', subject='{self.subject[:30]}...')"
