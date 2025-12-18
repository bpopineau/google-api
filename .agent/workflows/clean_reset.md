---
description: Deep clean the project and reinstall dependencies to fix environment issues
---

1. Remove build artifacts and caches
   - `rm -rf dist build *.egg-info .pytest_cache .ruff_cache __pycache__`
   - `find . -type d -name "__pycache__" -exec rm -rf {} +`

2. Reinstall dependencies (Interactive)
   - `/development`
