# Configuration & Authentication

This guide covers how to set up Google OAuth credentials and configure `mygooglib`.

## 1. Google OAuth Credentials (Personal Use)

This project uses **OAuth (Desktop app)** to access Google Workspace APIs for a single user (you).
You will create two local secret files:

- `credentials.json` (OAuth client ID/secret downloaded from Google Cloud)
- `token.json` (OAuth access + refresh token generated after you approve access once)

These files must **never** be committed to git.

### Step-by-Step Setup

1. **Create a Google Cloud Project**:
    - Go to [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project.
2. **Configure OAuth Consent Screen**:
    - Choose **External**.
    - Add yourself as a **Test user**.
3. **Enable APIs**:
    - Enable Drive, Sheets, Docs, Calendar, Tasks, and Gmail APIs in the Library.
4. **Create Credentials**:
    - Create an **OAuth client ID** of type **Desktop app**.
    - Download the JSON and rename it to `credentials.json`.

## 2. Shared Secrets Storage

By default, `mygooglib` looks for these files in your user's local app data directory to keep them out of the project folder:

- **Windows**: `%LOCALAPPDATA%\mygooglib\`
- **macOS/Linux**: `~/.config/mygooglib/`

### Environment Variables

You can override these default paths using the following environment variables:

- `MYGOOGLIB_CREDENTIALS_PATH`: Full path to `credentials.json`.
- `MYGOOGLIB_TOKEN_PATH`: Full path to `token.json`.

## 3. One-Time Setup

Run the following script to initiate the OAuth flow and generate `token.json`:

```bash
python scripts/oauth_setup.py
```

## 4. Logging & Debugging

You can control the library's verbosity via environment variables:

- `MYGOOGLIB_DEBUG=1`: Sets log level to `DEBUG`.
- `MYGOOGLIB_LOG_LEVEL`: Explicitly set level (`INFO`, `DEBUG`, `WARNING`).

## 5. Retry Policy

`mygooglib` retries transient errors for **read** requests by default. Write retries are disabled by default to prevent duplicate actions (like sending an email twice).

- `MYGOOGLIB_RETRY_ENABLED`: `0` or `1` (default `1`).
- `MYGOOGLIB_RETRY_ATTEMPTS_READ`: default `4`.
- `MYGOOGLIB_RETRY_ATTEMPTS_WRITE`: default `1`.
