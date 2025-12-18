"""Google Contacts (People API) wrapper.

Provides simple methods to list and search contacts.
"""

from __future__ import annotations

from typing import Any

from googleapiclient.errors import HttpError

from mygooglib.exceptions import raise_for_http_error
from mygooglib.utils.retry import execute_with_retry_http_error


def list_contacts(
    people_service: Any,
    *,
    page_size: int = 30,
    sort_order: str = "FIRST_NAME_ASCENDING",
) -> list[dict]:
    """List contacts from the user's connection.

    Args:
        people_service: People API Resource from get_clients().contacts
        page_size: Number of contacts to fetch
        sort_order: 'FIRST_NAME_ASCENDING' or 'LAST_NAME_ASCENDING'

    Returns:
        List of contact dicts with flattened names and emails.
    """
    try:
        request = (
            people_service.people()
            .connections()
            .list(
                resourceName="people/me",
                pageSize=page_size,
                personFields="names,emailAddresses,phoneNumbers",
                sortOrder=sort_order,
            )
        )
        response = execute_with_retry_http_error(request, is_write=False)
    except HttpError as e:
        raise_for_http_error(e, context="Contacts list")
        raise

    return [_flatten_person(p) for p in response.get("connections", [])]


def search_contacts(
    people_service: Any,
    query: str,
) -> list[dict]:
    """Search contacts by query.

    Args:
        people_service: People API Resource
        query: Search string

    Returns:
        List of matching contact dicts.
    """
    try:
        request = people_service.people().searchContacts(
            query=query,
            readMask="names,emailAddresses,phoneNumbers",
        )
        response = execute_with_retry_http_error(request, is_write=False)
    except HttpError as e:
        raise_for_http_error(e, context="Contacts search")
        raise

    # searchContacts returns 'results' -> 'person'
    results = response.get("results", [])
    return [_flatten_person(r.get("person", {})) for r in results]


def get_contact_by_resource_name(
    people_service: Any,
    resource_name: str,
) -> dict:
    """Get a single contact by resource name (e.g., 'people/c123...')."""
    try:
        request = people_service.people().get(
            resourceName=resource_name,
            personFields="names,emailAddresses,phoneNumbers",
        )
        response = execute_with_retry_http_error(request, is_write=False)
    except HttpError as e:
        raise_for_http_error(e, context="Contacts get")
        raise

    return _flatten_person(response)


def _flatten_person(person: dict) -> dict:
    """Helper: Flatten complex People API person object to simple dict."""
    names = person.get("names", [])
    emails = person.get("emailAddresses", [])
    phones = person.get("phoneNumbers", [])

    return {
        "resourceName": person.get("resourceName"),
        "name": names[0].get("displayName") if names else None,
        "email": emails[0].get("value") if emails else None,
        "phone": phones[0].get("value") if phones else None,
        "etag": person.get("etag"),
    }


class ContactsClient:
    """Simplified Google Contacts (People API) wrapper."""

    def __init__(self, service: Any):
        self.service = service

    def list_contacts(
        self,
        *,
        page_size: int = 30,
        sort_order: str = "FIRST_NAME_ASCENDING",
    ) -> list[dict]:
        """List contacts."""
        return list_contacts(self.service, page_size=page_size, sort_order=sort_order)

    def search_contacts(self, query: str) -> list[dict]:
        """Search contacts."""
        return search_contacts(self.service, query)

    def get_contact(self, resource_name: str) -> dict:
        """Get a specific contact."""
        return get_contact_by_resource_name(self.service, resource_name)
