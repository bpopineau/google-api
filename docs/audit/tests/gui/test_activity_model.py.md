# Audit Report: tests/gui/test_activity_model.py

## Purpose
- Unit tests for the `ActivityModel` and related items.

## Findings
- **Data Integrity:** Verifies that model items correctly store and return data via standard Qt roles (`TitleRole`, `StatusRole`, `DetailsRole`).
- **Update Logic:** Confirms that `update_status` correctly modifies existing items by ID and handles non-existent IDs gracefully.

## Quality Checklist
- [x] Verified model role data
- [x] Confirmed status update logic
