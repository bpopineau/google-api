"""Minimal smoke tests for mygooglib.

This script is intentionally conservative:
- It does not make API calls unless you pass explicit flags.
- It never prints tokens/credentials.

Examples:
  # Show available options
  python scripts/smoke_test.py --help

    # Drive: sync a local folder into a Drive folder
    python scripts/smoke_test.py drive-sync --local-path "C:\\path\\to\\folder" --drive-folder-id "<FOLDER_ID>"

  # Gmail: send an email to yourself
  python scripts/smoke_test.py gmail-send --to you@example.com --subject "Test" --body "Hello"

  # Gmail: search and (optionally) mark the first result as read
  python scripts/smoke_test.py gmail-search --query "newer_than:1d" --max 5
  python scripts/smoke_test.py gmail-search --query "is:unread newer_than:7d" --max 1 --mark-read

  # Sheets: read a range
    python scripts/smoke_test.py sheets-get --identifier <ID_OR_TITLE_OR_URL> --range "Sheet1!A1:C3"

  # Sheets: append a row
    python scripts/smoke_test.py sheets-append --identifier <ID_OR_TITLE_OR_URL> --sheet "Sheet1" --values "a" "b" "c"
"""

from __future__ import annotations

import argparse
from typing import Any

from mygooglib import get_clients
from mygooglib.drive import sync_folder
from mygooglib.gmail import mark_read, search_messages, send_email
from mygooglib.sheets import (
    append_row,
    get_range,
    open_by_title,
    resolve_spreadsheet,
    update_range,
)


def _print_jsonable(obj: Any) -> None:
    # Keep output small and readable; avoid printing huge payloads.
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        print(obj)
        return
    if isinstance(obj, list):
        print(f"list[{len(obj)}]")
        for i, item in enumerate(obj[:10]):
            print(f"  [{i}] {item}")
        if len(obj) > 10:
            print("  ...")
        return
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        print(f"dict[{len(keys)}] keys={keys}")
        # print a few important keys if present
        for k in ("id", "threadId", "updatedRange", "updatedRows", "updatedCells"):
            if k in obj:
                print(f"  {k}: {obj.get(k)}")
        return
    print(repr(obj))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Smoke tests for mygooglib")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_drive_sync = sub.add_parser(
        "drive-sync",
        help="Sync a local folder into a Drive folder (upload/update only; no deletes)",
    )
    p_drive_sync.add_argument(
        "--local-path",
        required=True,
        help="Local folder path to sync",
    )
    p_drive_sync.add_argument(
        "--drive-folder-id",
        required=True,
        help="Destination Drive folder id",
    )

    p_send = sub.add_parser("gmail-send", help="Send a test email")
    p_send.add_argument("--to", required=True, help="Recipient email")
    p_send.add_argument("--subject", required=True, help="Subject")
    p_send.add_argument("--body", required=True, help="Plain text body")
    p_send.add_argument("--cc", default=None, help="CC email(s), comma-separated")
    p_send.add_argument("--bcc", default=None, help="BCC email(s), comma-separated")
    p_send.add_argument(
        "--attach", action="append", default=[], help="Attachment path (repeatable)"
    )

    p_search = sub.add_parser("gmail-search", help="Search messages")
    p_search.add_argument("--query", required=True, help="Gmail search query")
    p_search.add_argument("--max", type=int, default=5, help="Max results (default 5)")
    p_search.add_argument(
        "--mark-read",
        action="store_true",
        help="Mark the first returned message as read",
    )

    p_get = sub.add_parser("sheets-get", help="Read a range from Sheets")
    p_get.add_argument(
        "--identifier",
        required=True,
        help="Spreadsheet id, title, or full URL",
    )
    p_get.add_argument("--range", required=True, help='A1 range, e.g. "Sheet1!A1:C3"')
    p_get.add_argument(
        "--parent-id",
        default=None,
        help="Optional Drive folder id to scope title lookup",
    )
    p_get.add_argument(
        "--allow-multiple",
        action="store_true",
        help="Allow multiple title matches (returns the first)",
    )

    p_append = sub.add_parser("sheets-append", help="Append a row to a sheet")
    p_append.add_argument(
        "--identifier",
        required=True,
        help="Spreadsheet id, title, or full URL",
    )
    p_append.add_argument("--sheet", required=True, help="Sheet/tab name")
    p_append.add_argument("--values", nargs="+", required=True, help="Row values")
    p_append.add_argument(
        "--parent-id",
        default=None,
        help="Optional Drive folder id to scope title lookup",
    )
    p_append.add_argument(
        "--allow-multiple",
        action="store_true",
        help="Allow multiple title matches (returns the first)",
    )

    p_update = sub.add_parser("sheets-update", help="Update a range in Sheets")
    p_update.add_argument(
        "--identifier",
        required=True,
        help="Spreadsheet id, title, or full URL",
    )
    p_update.add_argument(
        "--range",
        required=True,
        help='A1 range, e.g. "Sheet1!A1:C3"',
    )
    p_update.add_argument(
        "--row",
        action="append",
        required=True,
        help=(
            "Row values, comma-separated (repeat for multiple rows). "
            "Example: --row a,b,c --row 1,2,3"
        ),
    )
    p_update.add_argument(
        "--user-entered",
        action="store_true",
        help="Use USER_ENTERED (default is RAW)",
    )
    p_update.add_argument(
        "--parent-id",
        default=None,
        help="Optional Drive folder id to scope title lookup",
    )
    p_update.add_argument(
        "--allow-multiple",
        action="store_true",
        help="Allow multiple title matches (returns the first)",
    )

    p_open = sub.add_parser(
        "sheets-open-by-title", help="Resolve spreadsheet id by title"
    )
    p_open.add_argument("--title", required=True, help="Exact spreadsheet title")
    p_open.add_argument(
        "--parent-id",
        default=None,
        help="Optional Drive folder id to scope the search",
    )
    p_open.add_argument(
        "--allow-multiple",
        action="store_true",
        help="Allow multiple matches (returns the first)",
    )

    p_resolve = sub.add_parser(
        "sheets-resolve",
        help="Resolve a spreadsheet ID/title/URL to an id",
    )
    p_resolve.add_argument(
        "--identifier",
        required=True,
        help="Spreadsheet id, title, or full URL",
    )
    p_resolve.add_argument(
        "--parent-id",
        default=None,
        help="Optional Drive folder id to scope title lookup",
    )
    p_resolve.add_argument(
        "--allow-multiple",
        action="store_true",
        help="Allow multiple title matches (returns the first)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    clients = get_clients()

    if args.cmd == "drive-sync":
        summary = sync_folder(
            clients.drive,
            args.local_path,
            args.drive_folder_id,
        )
        _print_jsonable(summary)
        return 0

    if args.cmd == "gmail-send":
        cc = [s.strip() for s in (args.cc or "").split(",") if s.strip()] or None
        bcc = [s.strip() for s in (args.bcc or "").split(",") if s.strip()] or None
        message_id = send_email(
            clients.gmail,
            to=args.to,
            subject=args.subject,
            body=args.body,
            attachments=args.attach or None,
            cc=cc,
            bcc=bcc,
        )
        print("sent message id:")
        _print_jsonable(message_id)
        return 0

    if args.cmd == "gmail-search":
        results = search_messages(clients.gmail, args.query, max_results=args.max)
        _print_jsonable(results)
        if args.mark_read and results:
            msg_id = results[0].get("id")
            if msg_id:
                mark_read(clients.gmail, msg_id)
                print(f"marked read: {msg_id}")
        return 0

    if args.cmd == "sheets-get":
        values = get_range(
            clients.sheets,
            args.identifier,
            args.range,
            drive=clients.drive,
            parent_id=args.parent_id,
            allow_multiple=args.allow_multiple,
        )
        _print_jsonable(values)
        return 0

    if args.cmd == "sheets-append":
        result = append_row(
            clients.sheets,
            args.identifier,
            args.sheet,
            args.values,
            drive=clients.drive,
            parent_id=args.parent_id,
            allow_multiple=args.allow_multiple,
        )
        _print_jsonable(result)
        return 0

    if args.cmd == "sheets-update":
        values = [row.split(",") for row in args.row]
        result = update_range(
            clients.sheets,
            args.identifier,
            args.range,
            values,
            value_input_option="USER_ENTERED" if args.user_entered else "RAW",
            drive=clients.drive,
            parent_id=args.parent_id,
            allow_multiple=args.allow_multiple,
        )
        _print_jsonable(result)
        return 0

    if args.cmd == "sheets-open-by-title":
        sheet_id = open_by_title(
            clients.drive,
            args.title,
            parent_id=args.parent_id,
            allow_multiple=args.allow_multiple,
        )
        print("spreadsheet id:")
        _print_jsonable(sheet_id)
        return 0

    if args.cmd == "sheets-resolve":
        sheet_id = resolve_spreadsheet(
            clients.drive,
            args.identifier,
            parent_id=args.parent_id,
            allow_multiple=args.allow_multiple,
        )
        print("spreadsheet id:")
        _print_jsonable(sheet_id)
        return 0

    raise AssertionError(f"Unhandled command: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
