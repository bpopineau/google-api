# Testing & Validation

This document describes how to verify the functionality of `mygooglib`.

## 1. Automated Tests

The repo uses `pytest` for unit and integration tests.

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=mygooglib

# Run a specific test file
uv run pytest tests/test_workflow_search.py
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
from mygooglib.services.drive import list_files

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
mgui
```

---

## 4. VCR Cassette Recording (Integration Tests)

The project uses [pytest-recording](https://pypi.org/project/pytest-recording/) to record and replay HTTP interactions.

### Recording Modes

| Mode | Command | Use Case |
|------|---------|----------|
| `none` | `--record-mode=none` | CI/default - replay only |
| `once` | `--record-mode=once` | Record new cassettes |
| `rewrite` | `--record-mode=rewrite` | Refresh outdated cassettes |

### Running VCR Tests

```bash
# Replay from cassettes (default for CI)
uv run pytest tests/test_vcr_integration.py --record-mode=none

# Record new cassettes
uv run pytest tests/test_vcr_integration.py --record-mode=once
```

### Writing VCR Tests

```python
import pytest

@pytest.mark.vcr
def test_api_call():
    """Test with recorded HTTP interactions."""
    import urllib.request
    response = urllib.request.urlopen("https://api.example.com")
    assert response.status == 200
```

### Security

Cassettes are automatically sanitized:
- `Authorization` headers → `<ACCESS_TOKEN>`
- Email addresses → `<REDACTED_EMAIL>`
- OAuth tokens → `<REFRESH_TOKEN>`

Configuration: `tests/conftest.py`

### Refreshing Cassettes

```bash
rm tests/cassettes/test_my_api.yaml
uv run pytest tests/test_my_api.py --record-mode=once
git add tests/cassettes/
```
