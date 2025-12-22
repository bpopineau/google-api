"""Example: Batch update multiple ranges in a spreadsheet.

Demonstrates using batch_update for efficient multi-range updates.
"""

from mygooglib import get_clients


def main():
    clients = get_clients()

    # Replace with your spreadsheet ID
    SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"

    # Prepare multiple range updates
    updates = [
        {
            "range": "Sheet1!A1:B2",
            "values": [
                ["Name", "Score"],
                ["Alice", 95],
            ],
        },
        {
            "range": "Sheet1!A3:B4",
            "values": [
                ["Bob", 87],
                ["Charlie", 92],
            ],
        },
    ]

    # Batch update - single API call for all ranges
    result = clients.sheets.batch_update(
        SPREADSHEET_ID,
        updates,
        value_input_option="USER_ENTERED",  # Allows formulas, auto-format
    )

    print(f"Updated {result['totalUpdatedCells']} cells")
    print(f"Updated {result['totalUpdatedRows']} rows")

    # You can also use the BatchUpdater context manager for cleaner syntax:
    with clients.sheets.batch(SPREADSHEET_ID) as batch:
        batch.update("Sheet1!D1:E2", [["Grade", "Pass"], ["A", "Yes"]])
        batch.update("Sheet1!D3:E4", [["B", "Yes"], ["A", "Yes"]])
        batch.append("Sheet1", ["New Row Added"])
    # All updates are committed when exiting the context


if __name__ == "__main__":
    main()


