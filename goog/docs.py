"""
Google Docs API wrapper.

Provides a Pythonic interface for document operations.
"""

from goog.auth import GoogleAuth
from goog.utils import logger, with_retry


class DocsClient:
    """
    Pythonic wrapper for Google Docs API.

    Provides intuitive methods for document creation and editing:
    - Create documents
    - Read text content
    - Insert text at start/end
    - Find and replace text

    Example:
        >>> from goog import GoogleAuth, DocsClient
        >>> auth = GoogleAuth()
        >>> docs = DocsClient(auth)
        >>> doc_id = docs.create_document("My Report")
        >>> docs.insert_text(doc_id, "Hello World!")
    """

    def __init__(self, auth: GoogleAuth):
        """
        Initialize the Docs client.

        Args:
            auth: GoogleAuth instance for authentication.
        """
        self._auth = auth
        self._service = None

    @property
    def service(self):
        """Lazily initialize and return the Docs service."""
        if self._service is None:
            self._service = self._auth.build_service("docs", "v1")
        return self._service

    @with_retry()
    def create_document(self, title: str) -> str:
        """
        Create a new Google Doc.

        Args:
            title: Title for the new document.

        Returns:
            The document ID.

        Example:
            >>> doc_id = docs.create_document("Meeting Notes")
        """
        logger.info(f"Creating document: {title}")
        body = {"title": title}
        result = self.service.documents().create(body=body).execute()
        doc_id = result.get("documentId")
        logger.debug(f"Created document with ID: {doc_id}")
        return doc_id

    @with_retry()
    def get_document(self, document_id: str) -> dict:
        """
        Get full document metadata and content structure.

        Args:
            document_id: The document ID.

        Returns:
            Document metadata dictionary.
        """
        return self.service.documents().get(documentId=document_id).execute()

    @with_retry()
    def get_text(self, document_id: str) -> str:
        """
        Get plain text content of a document.

        Args:
            document_id: The document ID.

        Returns:
            The document's text content.

        Example:
            >>> text = docs.get_text("1abc...")
            >>> print(text)
        """
        doc = self.get_document(document_id)
        content = doc.get("body", {}).get("content", [])

        text_parts = []
        for element in content:
            if "paragraph" in element:
                para = element["paragraph"]
                for elem in para.get("elements", []):
                    if "textRun" in elem:
                        text_parts.append(elem["textRun"].get("content", ""))

        return "".join(text_parts)

    @with_retry()
    def insert_text(
        self,
        document_id: str,
        text: str,
        location: str = "end",
        index: int | None = None,
    ) -> None:
        """
        Insert text into a document.

        Args:
            document_id: The document ID.
            text: The text to insert.
            location: Where to insert - "start" or "end".
                     Ignored if index is provided.
            index: Specific index to insert at (1-based).

        Example:
            >>> docs.insert_text(doc_id, "Title\\n", location="start")
            >>> docs.insert_text(doc_id, "More content...", location="end")
        """
        if index is not None:
            insert_index = index
        elif location == "start":
            insert_index = 1
        else:  # end
            doc = self.get_document(document_id)
            # Get the end index (subtract 1 because endIndex is exclusive)
            content = doc.get("body", {}).get("content", [])
            if content:
                insert_index = content[-1].get("endIndex", 1) - 1
            else:
                insert_index = 1

        requests = [
            {
                "insertText": {
                    "location": {"index": insert_index},
                    "text": text,
                }
            }
        ]

        logger.debug(f"Inserting text at index {insert_index}")
        self.service.documents().batchUpdate(
            documentId=document_id,
            body={"requests": requests},
        ).execute()

    @with_retry()
    def find_replace(
        self,
        document_id: str,
        find: str,
        replace: str,
        match_case: bool = True,
    ) -> int:
        """
        Find and replace all occurrences of text.

        Args:
            document_id: The document ID.
            find: Text to search for.
            replace: Text to replace with.
            match_case: Whether to match case.

        Returns:
            Number of replacements made.

        Example:
            >>> count = docs.find_replace(doc_id, "{{DATE}}", "2024-01-15")
            >>> print(f"Replaced {count} occurrences")
        """
        requests = [
            {
                "replaceAllText": {
                    "containsText": {
                        "text": find,
                        "matchCase": match_case,
                    },
                    "replaceText": replace,
                }
            }
        ]

        logger.info(f"Replacing '{find}' with '{replace}' in document")
        result = (
            self.service.documents()
            .batchUpdate(
                documentId=document_id,
                body={"requests": requests},
            )
            .execute()
        )

        # Extract the count from the response
        replies = result.get("replies", [])
        if replies and "replaceAllText" in replies[0]:
            count = replies[0]["replaceAllText"].get("occurrencesChanged", 0)
        else:
            count = 0

        logger.debug(f"Replaced {count} occurrences")
        return count

    @with_retry()
    def append_paragraph(
        self,
        document_id: str,
        text: str,
    ) -> None:
        """
        Append a new paragraph at the end of the document.

        This is a convenience method that adds text followed by a newline.

        Args:
            document_id: The document ID.
            text: The paragraph text.

        Example:
            >>> docs.append_paragraph(doc_id, "This is a new paragraph.")
        """
        self.insert_text(document_id, text + "\n", location="end")

    @with_retry()
    def get_title(self, document_id: str) -> str:
        """
        Get the document title.

        Args:
            document_id: The document ID.

        Returns:
            The document title.
        """
        doc = self.get_document(document_id)
        return doc.get("title", "")

    @with_retry()
    def update_title(self, document_id: str, new_title: str) -> None:
        """
        Update the document title.

        Args:
            document_id: The document ID.
            new_title: The new title.

        Note:
            This uses the Drive API under the hood since Docs API
            doesn't support title updates directly.
        """
        # Title updates require the Drive API
        drive_service = self._auth.build_service("drive", "v3")
        logger.info(f"Updating document title to: {new_title}")
        drive_service.files().update(
            fileId=document_id,
            body={"name": new_title},
        ).execute()
