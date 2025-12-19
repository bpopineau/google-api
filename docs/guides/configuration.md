# Configuration & Authentication

This guide covers how to set up Google OAuth credentials and configure the `mygoog` application.

## 1. Google OAuth Credentials

`mygoog` uses **OAuth 2.0 (Desktop Flow)** to access your personal Google Workspace data securely.

### Quick Setup

1.  **Download Credentials**: Get your `credentials.json` from the Google Cloud Console (OAuth Client ID > Desktop App).
2.  **Launch App**: Run `mygoog`.
3.  **Sign In**: The app will launch your browser. Approve access.
4.  **Done**: Your access tokens are securely saved for future use.

> **Note**: Tokens are stored in:
> - **Windows**: `%LOCALAPPDATA%\mygooglib\`
> - **macOS/Linux**: `~/.config/mygooglib/`

## 2. Application Settings

The Desktop Application stores your preferences (Theme, Window Size, etc.) in a JSON file:

- **Path**: `~/.mygooglib/config.json`
- **Format**:
  ```json
  {
      "theme": "dark",
      "window_geometry": [100, 100, 1200, 800],
      "default_view": "home",
      "log_level": "INFO"
  }
  ```

You can modify these settings via the **Settings Page** in the app or by editing this file directly.

## 3. Environment Variables (Advanced)

For developers or advanced users, you can override paths and behaviors using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `MYGOOGLIB_CREDENTIALS_PATH` | Path to `credentials.json` | `%LOCALAPPDATA%\mygooglib\credentials.json` |
| `MYGOOGLIB_TOKEN_PATH` | Path to `token.json` | `%LOCALAPPDATA%\mygooglib\token.json` |
| `MYGOOGLIB_LOG_LEVEL` | Logging verbosity | `INFO` |
| `MYGOOGLIB_DEBUG` | Enable debug mode (verbose logs) | `0` |

## 4. Retry Policy

The library automatically handles transient errors (like "Rate Limit Exceeded"). This is largely internal but configurable via environment variables:

- `MYGOOGLIB_RETRY_ENABLED`: `1` (default)
- `MYGOOGLIB_RETRY_ATTEMPTS_READ`: `4` (default)
