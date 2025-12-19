---
description: This workflow enforces a simple 3-phase cycle: **PLAN**, **BUILD**, **SHIP**. `task.md` is the source of truth for all progress.
---

# evolve.md 

## 1. PLAN
1.  **Initialize `task.md`**: Create a new task file with the structure below:

### `task.md` Template
```markdown
# Task: [Clear Goal Summary]

- [ ] PLAN
    - [x] Create implementation breakdown
    - [ ] Get user approval
- [ ] BUILD
    - [ ] [Step 1: e.g., Implement core class]
    - [ ] [Step 2: e.g., Update client wrapper]
    - [ ] [Step 3: ...]
    - [ ] Unit Tests
    - [ ] Lint Check (`ruff check . --fix`)
- [ ] SHIP
    - [ ] Smoke Tests (Mandatory)
    - [ ] Documentation Update (Mandatory: Docstrings, README, Guides)
    - [ ] Update CHANGELOG
    - [ ] Commit & Push
```

2.  **Break down the work**:
    - Add specific **implementation steps** under the `BUILD` section in `task.md`.
    - List the specific files you intend to modify.
3.  **Brief the User**: Summarize the plan in chat (Goal, Changes, Verification).
4.  **Get Approval**: **STOP**. Do not proceed to BUILD until the user explicitly approves the plan.

## 2. BUILD
1.  **Execute the plan**: Work through the checklist in `task.md`.
2.  **Test as you go**: Write unit tests for new functionality immediately.
3.  **Quality Check**:
// turbo
    - Run `pytest` to ensure all tests pass.
// turbo
    - Run `ruff check . --fix` to ensure clean code.

4.  **Mark Complete**: Mark items `[x]` in `task.md` **only** after they are verified. Individually verify each and every task has been completed, not just marked complete.

## 3. SHIP
*Mandatory Gate: Do not skip these steps.*

1.  **Smoke Tests**: 
// turbo
Run `python scripts/smoke_test.py` (or relevant service script) to verify end-to-end behavior on the real API.
2.  **Documentation** (Mandatory):
    - **Docstrings**: Ensure new code has Google-style docstrings. Check every function you have added or changed and manually ensure they have docstrings.
    - **README**: Add new features to the main list. 
    - **Guides**: Update or create files in `docs/` if workflows change.
3.  **Changelog**: Add a concise entry to `CHANGELOG.md`.
4.  **Release** (Ask the user if they want to do this step):
    - Bump version in `pyproject.toml` if this is a named release.
5.  **Commit**: 
// turbo
run `git add .` and `git commit -m "type: description"`
6.  **Push**: 
// turbo
run `git push`