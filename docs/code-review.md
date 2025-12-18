# Code review report

## Summary
High-level findings from reviewing the current `mygooglib` implementation.

## Findings
1. **Token refresh fails if the config directory is missing.** When an existing token is refreshed, the code writes `token.json` without first creating the parent directory, so first-time refreshes can crash with `FileNotFoundError` if `~/.config/mygooglib/` (or `LOCALAPPDATA` on Windows) does not exist. The initial OAuth flow does create the directory, but refreshes hit this path before that guard. Consider ensuring the directory exists before writing the refreshed token or using `Path.write_text` after `mkdir(parents=True, exist_ok=True)`. 
2. **Default OAuth scopes are very broad.** The library always requests full Drive access, full Sheets access, Gmail send/modify, Calendar, and Tasks scopes by default. That level of access is unnecessary for many use cases and increases blast radius if credentials are compromised. Encouraging narrower, service-specific scopes or allowing callers to specify scopes per client would better align with least-privilege practices.
3. **Gmail search performs one API call per message.** `search_messages` paginates message IDs and then issues an individual `messages().get()` request for each result to fetch metadata. For larger queries this results in `O(n)` extra round-trips (up to 500 per page), which is slow and more likely to hit Gmail quotas. Consider using batch requests or fetching needed metadata directly in the `list()` call (e.g., `format="metadata"` when the API supports it) to reduce API volume.
