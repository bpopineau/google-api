---
description: Guide for building features that combine multiple mygooglib services
---

1. Identify the Integration Pattern
   - **Source → Target patterns already in mygooglib**:
     - `examples/sheets_to_gmail_summary.py` — Sheets → Gmail
   - **Common patterns from AUTOMATION_GOALS.md**:
     - Sheets → Calendar: Create events from spreadsheet schedule
     - Gmail → Sheets: Log emails to tracking spreadsheet
     - Tasks → Docs: Generate task summary document
     - Calendar → Gmail: Email daily agenda

2. Design Data Flow
   - **Define clearly**:
     ```
     [Source Service] → [Transform Logic] → [Target Service]
     ```
   - **Example**: Sheets → Calendar
     ```
     sheets.get_range("Schedule", "A2:D100")
       → Parse rows into event dicts
       → calendar.add_event(summary, start, end) for each
     ```

3. Implement in Stages
   - **Stage 1**: Read from source
     ```python
     clients = get_clients()
     rows = clients.sheets.get_range(spreadsheet_id, range_)
     ```
   - **Stage 2**: Transform data
     ```python
     events = []
     for row in rows:
         events.append({
             "summary": row[0],
             "start": parse_datetime(row[1]),
             "end": parse_datetime(row[2]),
         })
     ```
   - **Stage 3**: Write to target
     ```python
     for event in events:
         clients.calendar.add_event(**event)
     ```

4. Create Example Script
   - **Location**: `examples/[source]_to_[target].py`
   - **Naming**: Use service names (e.g., `sheets_to_calendar.py`)
   - **Pattern**: Follow `examples/sheets_to_gmail_summary.py`

5. Add as Workflow Method (Optional)
   - **If reusable**, add to `mygooglib/workflows.py` (new module):
     ```python
     def sheets_to_calendar(spreadsheet_id: str, range_: str, calendar_id: str = "primary"):
         """Create calendar events from a spreadsheet schedule."""
     ```

6. Add CLI Command (Optional)
   - **File**: `mygooglib/cli/workflows.py` (new)
   - **Command**: `mygoog workflow sheets-to-calendar --spreadsheet "ID" --range "A2:D100"`

7. Document
   - Add to `docs/guides/usage.md` under "Cross-Service Workflows".
   - Add to `AUTOMATION_GOALS.md` Section 6 as completed.

8. Test
   - Create `tests/test_workflows.py` with mocked clients.
   - Run with real data: `python examples/[source]_to_[target].py`
