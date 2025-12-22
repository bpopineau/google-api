---
description: End-to-end workflow from idea to mygooglib implementation
---

1. Define the Feature
// turbo
   - `/propose_features`
   - **Output**: Create `feature_proposal.md` artifact.
   - **Check**: Does this align with `AUTOMATION_GOALS.md` workflows (W1-W6)?

2. Plan the Implementation
   - **Module**: Which `mygooglib/[service].py` does this belong to?
   - **CLI**: Should this be exposed via `mygooglib/cli/[service].py`?
   - **Breaking changes**: Does this modify existing public API?

3. Scaffold the Code
// turbo
   - `/scaffold_new_script`
   - **Goal**: Get a working prototype in `scripts/` or `examples/`.

4. Implement and Test
   - **Write code**: Add method to `mygooglib/[service].py`.
   - **Add test**: Create `tests/test_[service].py::test_new_method`.
// turbo
   - `/development`

5. Add CLI Support (if applicable)
   - **File**: `mygooglib/cli/[service].py`
   - **Pattern**: Follow existing Typer commands in the same file.
   - **Test**: `mg [service] [command] --help`

6. Polish Documentation
// turbo
   - `/write_docstrings`
   - **Target**: New method docstrings.

7. Update Project Docs
// turbo
   - `/update_docs`
   - **Update**:
     - `docs/guides/usage.md` — add usage example
     - `AUTOMATION_GOALS.md` — update if this completes a workflow
     - `docs/development/roadmap.md` — check off if listed

8. Final Verification
// turbo
   - `/ci_local`

