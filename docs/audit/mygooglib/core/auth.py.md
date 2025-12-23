# Audit Report: mygooglib/core/auth.py

## Purpose
- Centralizes OAuth2 credential management, including path resolution for `credentials.json` and `token.json`, initial authentication via `InstalledAppFlow`, and automated token refresh.

## Main Exports
- `get_auth_paths()`: Returns a tuple of (credentials_path, token_path).
- `get_creds(...)`: Main entry point to get authorized `google.oauth2.credentials.Credentials`.
- `verify_creds_exist()`: Non-blocking check for token existence.

## Findings
- **Paths:** Uses `LOCALAPPDATA` on Windows and `~/.mygoog` elsewhere. Supports environment variable overrides (`MYGOOGLIB_CREDENTIALS_PATH`, `MYGOOGLIB_TOKEN_PATH`).
- **Robustness:** Handles token refresh failures with clear error messages pointing to `oauth_setup.py`.
- **Refactors:** Redundant `token_path.parent.mkdir` calls were consolidated during audit (planned).
- **Type Safety:** Well-typed with `Credentials` and `Path` throughout.

## TODOs
- [ ] [Major] Consider implementing a Service Account flow for non-interactive server environments.
- [ ] [Technical Debt] The `_get_paths` logic could be slightly simplified by using `secrets_dir` more consistently.

## Quality Checklist
- [x] Docstrings follow project style
- [x] Type hints are complete and modern
- [x] Unused code removed
- [x] Logically verified for edge cases
