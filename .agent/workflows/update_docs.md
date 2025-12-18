---
description: Meticulously update documentation to ensure accuracy and consistency
---

1. Audit Changes
   - **Action**: Review recent code changes (`git diff main...HEAD` or `git log -p`).
   - **Goal**: Identify modified public APIs, changed signatures, or new features.

2. Verify API Reference
   - **Check**: Do docstrings match the actual implementation?
   - **Action**: Run `python -m pydoc mygooglib.module_name` for changed modules to see the rendered output.
   - **Update**: Update `docs/reference/*.md` if manual, or ensure docstrings are pristine.

3. Update Guides and Examples
   - **Check**: Do the `examples/` scripts still run?
   - **Action**: Run relevant scripts in `examples/` or `scripts/` to verify they don't crash.
   - **Update**: Update `docs/guides/*.md` to reflect new best practices or workflows.

4. maintain Consistency
   - **Check**: Does `README.md` still accurately reflect the "Quick Start"?
   - **Check**: Is `AUTOMATION_GOALS.md` up to date with what's actually built?
   - **Action**: specialized checks:
     - `ruff check docs/` (if configured for docs)
     - spell check (manual or tool)

5. Final Review
   - **Action**: Read the changed docs as a new user.
   - **Question**: "If I only read this, would I be able to use the feature correctly?"
