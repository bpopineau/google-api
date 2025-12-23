# AI-Friendly Code Standards

> Standards for writing code that is optimally readable and modifiable by AI agents.

## 1. Type Annotations

**Requirement:** All public functions MUST have complete type annotations.

```python
# ✅ Good
def process_data(items: list[str], max_count: int = 10) -> dict[str, int]:
    ...

# ❌ Bad
def process_data(items, max_count=10):
    ...
```

**Enforcement:** `mypy --strict`

---

## 2. Docstrings

**Requirement:** All public functions MUST have a docstring with at least a one-line summary.

```python
# ✅ Good
def send_email(to: str, subject: str) -> str:
    """Send an email and return the message ID."""
    ...

# ❌ Bad
def send_email(to: str, subject: str) -> str:
    ...
```

**Enforcement:** `ruff` rules D100-D107

---

## 3. Directory Manifests

**Requirement:** Every major directory MUST have a `MANIFEST.md` containing:
- Purpose of the directory
- Key files and their roles
- Dependencies (imports from other directories)

**Enforcement:** `scripts/run_arch_lint.py`

---

## 4. Import Boundaries

**Requirement:** Follow the layered architecture:
- `mygooglib.core` → No internal imports
- `mygooglib.services` → May import from `core`
- `mygooglib.workflows` → May import from `services` and `core`
- `mygoog_cli/` and `mygoog_gui/` → May import from `mygooglib`

**Enforcement:** `import-linter`

---

## 5. Error Handling

**Requirement:** Raise specific exceptions, never bare `Exception`.

```python
# ✅ Good
raise ValueError("Invalid spreadsheet ID format")

# ❌ Bad
raise Exception("Something went wrong")
```

---

## 6. Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions | `snake_case` | `get_user_data()` |
| Classes | `PascalCase` | `SheetsClient` |
| Constants | `UPPER_SNAKE` | `MAX_RETRY_COUNT` |
| Private | `_leading_underscore` | `_internal_helper()` |

---

## 7. Context Window Optimization

**Goal:** Minimize files needed to understand any single concept.

- Keep related logic in the same file
- Use explicit imports (avoid `from module import *`)
- Group related functions in logical order
- Place type definitions near their usage

---

## Checklist for New Code

- [ ] All functions have type hints
- [ ] All public functions have docstrings
- [ ] No mypy errors
- [ ] No ruff errors
- [ ] Follows naming conventions
- [ ] Directory has MANIFEST.md (if new)
