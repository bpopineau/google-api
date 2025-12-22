"""Google Contacts (People API) wrapper.

Provides simple methods to list and search contacts.
"""

from __future__ import annotations

from typing import Any

from mygooglib.core.utils.base import BaseClient
from mygooglib.core.utils.retry import api_call, execute_with_retry_http_error


@api_call("Contacts list", is_write=False)
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
    return [_flatten_person(p) for p in response.get("connections", [])]


@api_call("Contacts search", is_write=False)
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
    request = people_service.people().searchContacts(
        query=query,
        readMask="names,emailAddresses,phoneNumbers",
    )
    response = execute_with_retry_http_error(request, is_write=False)
    results = response.get("results", [])
    return [_flatten_person(r.get("person", {})) for r in results]


@api_call("Contacts get", is_write=False)
def get_contact_by_resource_name(
    people_service: Any,
    resource_name: str,
) -> dict:
    """Get a single contact by resource name (e.g., 'people/c123...')."""
    request = people_service.people().get(
        resourceName=resource_name,
        personFields="names,emailAddresses,phoneNumbers",
    )
    response = execute_with_retry_http_error(request, is_write=False)
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


@api_call("Contacts create", is_write=True)
def create_contact(
    people_service: Any,
    *,
    given_name: str,
    family_name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
) -> dict:
    """Create a new contact.

    Args:
        people_service: People API Resource
        given_name: First name (required)
        family_name: Last name (optional)
        email: Email address (optional)
        phone: Phone number (optional)

    Returns:
        Created contact dict with resourceName.
    """
    person_body: dict[str, Any] = {
        "names": [{"givenName": given_name, "familyName": family_name or ""}],
    }
    if email:
        person_body["emailAddresses"] = [{"value": email}]
    if phone:
        person_body["phoneNumbers"] = [{"value": phone}]

    request = people_service.people().createContact(body=person_body)
    response = execute_with_retry_http_error(request, is_write=True)
    return _flatten_person(response)


@api_call("Contacts update (get)", is_write=False)
def _get_existing_contact(people_service: Any, resource_name: str) -> dict:
    """Get existing contact for update (internal helper)."""
    get_request = people_service.people().get(
        resourceName=resource_name,
        personFields="names,emailAddresses,phoneNumbers",
    )
    return execute_with_retry_http_error(get_request, is_write=False)  # type: ignore[no-any-return]


@api_call("Contacts update", is_write=True)
def update_contact(
    people_service: Any,
    resource_name: str,
    *,
    given_name: str | None = None,
    family_name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
) -> dict:
    """Update an existing contact.

    Args:
        people_service: People API Resource
        resource_name: Contact resource name (e.g., 'people/c123...')
        given_name: New first name (optional)
        family_name: New last name (optional)
        email: New email (optional)
        phone: New phone (optional)

    Returns:
        Updated contact dict.

    Note:
        At least one field must be provided to update.
    """
    existing = _get_existing_contact(people_service, resource_name)

    update_person_fields: list[str] = []
    person_body: dict[str, Any] = {"etag": existing.get("etag")}

    if given_name is not None or family_name is not None:
        names = existing.get("names", [{}])
        name_entry = names[0] if names else {}
        if given_name is not None:
            name_entry["givenName"] = given_name
        if family_name is not None:
            name_entry["familyName"] = family_name
        person_body["names"] = [name_entry]
        update_person_fields.append("names")

    if email is not None:
        person_body["emailAddresses"] = [{"value": email}]
        update_person_fields.append("emailAddresses")

    if phone is not None:
        person_body["phoneNumbers"] = [{"value": phone}]
        update_person_fields.append("phoneNumbers")

    if not update_person_fields:
        raise ValueError("At least one field must be provided to update")

    request = people_service.people().updateContact(
        resourceName=resource_name,
        body=person_body,
        updatePersonFields=",".join(update_person_fields),
    )
    response = execute_with_retry_http_error(request, is_write=True)
    return _flatten_person(response)


@api_call("Contacts delete", is_write=True)
def delete_contact(
    people_service: Any,
    resource_name: str,
) -> None:
    """Delete a contact.

    Args:
        people_service: People API Resource
        resource_name: Contact resource name (e.g., 'people/c123...')
    """
    request = people_service.people().deleteContact(resourceName=resource_name)
    execute_with_retry_http_error(request, is_write=True)


class ContactsClient(BaseClient):
    """Simplified Google Contacts (People API) wrapper."""

    def list_contacts(
        self,
        *,
        page_size: int = 30,
        sort_order: str = "FIRST_NAME_ASCENDING",
    ) -> list[dict]:
        """List contacts."""
        return list_contacts(self.service, page_size=page_size, sort_order=sort_order)  # type: ignore[no-any-return]

    def search_contacts(self, query: str) -> list[dict]:
        """Search contacts."""
        return search_contacts(self.service, query)  # type: ignore[no-any-return]

    def get_contact(self, resource_name: str) -> dict:
        """Get a specific contact."""
        return get_contact_by_resource_name(self.service, resource_name)  # type: ignore[no-any-return]

    def create_contact(
        self,
        *,
        given_name: str,
        family_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> dict:
        """Create a new contact."""
        return create_contact(  # type: ignore[no-any-return]
            self.service,
            given_name=given_name,
            family_name=family_name,
            email=email,
            phone=phone,
        )

    def update_contact(
        self,
        resource_name: str,
        *,
        given_name: str | None = None,
        family_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> dict:
        """Update an existing contact."""
        return update_contact(  # type: ignore[no-any-return]
            self.service,
            resource_name,
            given_name=given_name,
            family_name=family_name,
            email=email,
            phone=phone,
        )

    def delete_contact(self, resource_name: str) -> None:
        """Delete a contact."""
        delete_contact(self.service, resource_name)
