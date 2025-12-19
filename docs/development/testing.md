# Testing & Validation

This document describes how to verify the functionality of `mygooglib`.

## 1. Automated Tests

The repo uses `pytest` for unit and integration tests.

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=mygooglib
```

## 2. Smoke Test Runner

`scripts/smoke_test.py` provides a CLI for quick manual checks.

```bash
# See all available smoke tests
python scripts/smoke_test.py --help

# Run all read-only checks
python scripts/smoke_test.py all

# Run all checks including writes (Gmail send + Sheets write)
python scripts/smoke_test.py all --write
```

## 3. Manual Smoke Checklist

Run these once after OAuth setup or any time you want a quick confidence check.

### Authentication
Confirm token refresh works (no re-consent prompt expected):
```bash
python scripts/check_token_refresh.py
```

### Drive
List a few files:
```python
from mygooglib import get_clients
from mygooglib.drive import list_files

clients = get_clients()
files = list_files(clients.drive, page_size=5)
for f in files:
    print(f["id"], f["name"])
```

### Sheets
Read a small range:
```bash
python scripts/smoke_test.py sheets-get --identifier "<ID_OR_TITLE_OR_URL>" --range "Sheet1!A1:C3"
```

### Gmail
Send to yourself + verify via search:
```bash
python scripts/smoke_test.py gmail-send --subject "mygooglib smoke" --body "Hello"
python scripts/smoke_test.py gmail-search --query "subject:mygooglib smoke newer_than:1d" --max 3
```

### Drive Sync
Sync a local folder into a Drive folder:
```bash
python scripts/smoke_test.py drive-sync --local-path "C:\path\to\folder" --drive-folder-id "<FOLDER_ID>"
```

### Desktop GUI
Verify the application launches and renders (requires display):
```bash
mygoog gui run
```
