# Audit Report: mygoog_gui/widgets/sidebar.py

## Purpose
- Navigation sidebar providing access to all major service pages and settings.

## Main Exports
- `Sidebar`: A 200px fixed-width frame with checkable navigation buttons.
- `SidebarButton`: Custom checkable button with specialized styling.

## Findings
- **Exclusive Selection:** Correctly uses `QButtonGroup` with `setExclusive(True)` to ensure only one page is active at a time.
- **Dynamic Definition:** Page definitions are stored in a central `PAGES` list, making it easy to add or reorder navigation items.
- **Visual Consistency:** Integrates with the global object name "sidebar" to consume theme-specific styling.

## Quality Checklist
- [x] Exclusive button grouping implemented
- [x] Clear page change signaling
- [x] Bottom-aligned settings access
