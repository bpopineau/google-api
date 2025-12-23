# Audit Report: mygooglib/core/config.py

## Purpose
- Provides a centralized, singleton-based configuration system using JSON for storage. Handles schema definition, disk persistence, and migration from legacy config directories.

## Main Exports
- `Config`: Dataclass schema for application settings (theme, window geometry, etc.).
- `AppConfig`: Singleton manager providing property-based access and automatic saving.

## Findings
- **Storage:** Currently uses `~/.mygoog` globally.
- **Migration:** Explicitly migrates `~/.mygooglib` to `~/.mygoog` if found.
- **Extensibility:** `from_dict` implementation allows for forward compatibility by filtering unknown keys.
- **Persistence:** Setters on `AppConfig` trigger immediate `save()` calls.

## TODOs
- [ ] [Consistency] Align `config_dir` resolution with `auth.py` to use `LOCALAPPDATA` on Windows.
- [ ] [Technical Debt] Consider using a pydantic-like validation if the config grows significantly more complex.

## Quality Checklist
- [x] Docstrings follow project style
- [x] Type hints are complete and modern
- [x] Unused code removed
- [x] Logically verified for edge cases
