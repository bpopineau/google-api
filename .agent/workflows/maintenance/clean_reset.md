---
description: Deep clean mygooglib project and reinstall dependencies
---

1. Remove build artifacts and caches
   - `Remove-Item -Recurse -Force dist, build, mygooglib.egg-info, .pytest_cache, .ruff_cache -ErrorAction SilentlyContinue`
   - `Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force`

2. Reinstall mygooglib in editable mode
// turbo
   - `pip install -e ".[dev,cli]"`

3. Verify clean state
// turbo
   - `python -c "from mygooglib import get_clients; print('Import OK')"`

