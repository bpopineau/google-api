"""Example: Send email with idempotency key to prevent duplicates.

Demonstrates using idempotency_key to prevent duplicate emails
when a script is run multiple times.
"""

from datetime import date

from mygooglib import get_clients


def main():
    clients = get_clients()

    # Create a unique key based on the purpose and date
    # This ensures the email is only sent once per day
    today = date.today().isoformat()
    idempotency_key = f"daily-report-{today}"

    # Try to send the email
    result = clients.gmail.send_email(
        to="team@example.com",
        subject=f"Daily Report - {today}",
        body=f"This is the automated daily report for {today}.\n\nBest regards,\nAutomation",
        idempotency_key=idempotency_key,
    )

    if result is None:
        print(f"Email already sent today (key: {idempotency_key})")
    else:
        print(f"Email sent successfully! Message ID: {result}")


def using_idempotency_store_directly():
    """Alternative: Use IdempotencyStore directly for custom logic."""
    from mygooglib.core.utils.idempotency import IdempotencyStore

    store = IdempotencyStore()

    # Check if already processed
    key = "process-customer-123"
    if store.check(key):
        print("Already processed, skipping...")
        return

    # Do your work here
    print("Processing customer 123...")

    # Mark as processed
    store.add(key, metadata='{"customer_id": 123, "action": "processed"}')
    print("Done!")


if __name__ == "__main__":
    main()
    print("\n--- Direct store usage ---")
    using_idempotency_store_directly()
