"""Example: List and search Google Contacts.

Demonstrates using the ContactsClient to list and search contacts.
"""

from mygooglib import get_clients


def main():
    clients = get_clients()

    # List first 10 contacts
    print("=== First 10 Contacts ===")
    contacts = clients.contacts.list_contacts(page_size=10)
    for contact in contacts:
        name = contact.get("name") or "(no name)"
        email = contact.get("email") or "(no email)"
        print(f"  • {name}: {email}")

    # Search for a contact
    print("\n=== Search for 'john' ===")
    results = clients.contacts.search_contacts("john")
    if results:
        for contact in results[:5]:
            name = contact.get("name") or "(no name)"
            email = contact.get("email") or "(no email)"
            print(f"  • {name}: {email}")
    else:
        print("  No results found")


if __name__ == "__main__":
    main()
