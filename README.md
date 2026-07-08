# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Owner: Tanisha (available time: 120 min)

Biscuit — Golden Retriever, age 3
    - Morning walk (30 min)
    - Feeding (10 min)
    - Grooming (20 min)
    Total task time: 60 min

Whiskers — Cat, age 5
    - Litter cleaning (15 min)
    - Play time (25 min)
    Total task time: 40 min

Plan for Tanisha:
    Total time for all tasks: 100 min
    Leftover available time: 20 min
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Plan.sort_by_time()` | Sorts the plan's tasks in place by `duration`, shortest first. |
| Filtering | `Plan.filter_by_status(completed=...)` | Returns tasks matching a completion status — completed tasks vs. remaining to-dos. |
| Conflict handling | `Plan.detect_conflicts()` | Flags tasks on the same `due_date` whose `[start, start + duration)` time windows overlap, across the same or different pets, and returns warning messages. |
| Recurring tasks | `Task.mark_complete()` / `Task.next_occurrence()` / `Pet.complete_task()` | Completing a daily/weekly task auto-creates the next occurrence (today + 1 day or + 7 days via `timedelta`); `Pet.complete_task()` appends it to the pet's list. |

## Testing PawPal+
use python -m pytest to run

PawPal+'s 26 tests cover sorting by duration, status filtering, recurring-task generation, and time-conflict detection, including edge cases like empty lists, back-to-back tasks, and one-off vs. daily/weekly recurrence. Two tests intentionally document questionable current behavior: non-idempotent completion that duplicates tasks, and sort_by_time() sorting by duration instead of start time.

successful terminal output:
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Users/tanishajain/Desktop/pawpal/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/tanishajain/Desktop/pawpal
collecting ... collected 26 items

tests/test_pawpal.py::test_task_completion PASSED                        [  3%]
tests/test_pawpal.py::test_task_addition PASSED                          [  7%]
tests/test_pawpal.py::test_sort_happy_path PASSED                        [ 11%]
tests/test_pawpal.py::test_sort_empty_list PASSED                        [ 15%]
tests/test_pawpal.py::test_sort_single_task PASSED                       [ 19%]
tests/test_pawpal.py::test_sort_is_stable_for_equal_durations PASSED     [ 23%]
tests/test_pawpal.py::test_sort_mutates_in_place_and_is_idempotent PASSED [ 26%]
tests/test_pawpal.py::test_sort_orders_by_duration_not_start_time PASSED [ 30%]
tests/test_pawpal.py::test_filter_by_status_splits_completed_and_pending PASSED [ 34%]
tests/test_pawpal.py::test_filter_by_status_all_pending_returns_empty_completed PASSED [ 38%]
tests/test_pawpal.py::test_one_off_has_no_next_occurrence PASSED         [ 42%]
tests/test_pawpal.py::test_daily_next_occurrence_is_tomorrow PASSED      [ 46%]
tests/test_pawpal.py::test_weekly_next_occurrence_is_seven_days_out PASSED [ 50%]
tests/test_pawpal.py::test_next_occurrence_carries_over_fields PASSED    [ 53%]
tests/test_pawpal.py::test_unrecognized_recurrence_fails_safe PASSED     [ 57%]
tests/test_pawpal.py::test_complete_task_appends_next_occurrence_to_pet PASSED [ 61%]
tests/test_pawpal.py::test_complete_task_one_off_adds_nothing PASSED     [ 65%]
tests/test_pawpal.py::test_double_complete_duplicates_occurrence PASSED  [ 69%]
tests/test_pawpal.py::test_no_conflicts_when_no_start_times PASSED       [ 73%]
tests/test_pawpal.py::test_empty_plan_has_no_conflicts PASSED            [ 76%]
tests/test_pawpal.py::test_exact_same_start_time_conflicts PASSED        [ 80%]
tests/test_pawpal.py::test_back_to_back_tasks_do_not_conflict PASSED     [ 84%]
tests/test_pawpal.py::test_overlapping_windows_conflict PASSED           [ 88%]
tests/test_pawpal.py::test_completed_task_never_conflicts PASSED         [ 92%]
tests/test_pawpal.py::test_different_days_do_not_conflict PASSED         [ 96%]
tests/test_pawpal.py::test_owner_starts_with_no_pet PASSED               [100%]

============================== 26 passed in 0.02s ==============================

Confidence level: 4/5 stars

## 📸 Demo Walkthrough

### Main UI features

The Streamlit app (`streamlit run app.py`) is organized top-to-bottom so a user can go from empty state to a full daily plan without leaving the page:

- **Owner & pet setup** — enter the owner's name and daily time budget (minutes available today), plus the pet's name, species, and age.
- **Task entry** — add care tasks with a title, duration, **start time**, and a **recurrence** setting (`none` / `daily` / `weekly`). Each added task is stamped with today's date and the pet's name so the scheduler can reason about it.
- **Current tasks table** — every task the pet has is listed with its start time, duration, recurrence, and completion status.
- **Generate schedule** — builds a `Plan` from the pet's tasks and renders the results with Streamlit status components (`st.success`, `st.warning`, `st.table`): conflict warnings, a time-budget summary, the full plan sorted shortest-first, and side-by-side "To do" vs. "Completed" tables.

### Example workflow

1. **Set up the owner** — type an owner name (e.g. *Jordan*) and leave the daily budget at 120 minutes.
2. **Add a pet** — enter a pet name (e.g. *Mochi*), pick a species, and set the age. The pet is attached to the owner.
3. **Add a task** — title it *Morning walk*, set duration to 20 min and a start time of 09:00, then click **Add task**. It appears in the *Current tasks* table.
4. **Add a second, overlapping task** — e.g. *Feeding* for 10 min also starting at 09:00, to demonstrate conflict detection.
5. **View today's schedule** — click **Generate schedule** to see conflict warnings, the time budget, the sorted plan, and the to-do/completed split.

### Key Plan behaviors shown

- **Sorting** — `Plan.sort_by_time()` orders the generated plan by duration, shortest task first (shown in the "Plan (sorted by time)" table).
- **Status filtering** — `Plan.filter_by_status()` splits tasks into "🟡 To do" and "✅ Completed" tables.
- **Conflict warnings** — `Plan.detect_conflicts()` flags tasks on the same day whose `[start, start + duration)` windows overlap and surfaces each as an `st.warning`; when nothing overlaps, an `st.success` confirms the day is clear.
- **Time budget** — the plan reports leftover minutes against the owner's `available_time`, warning when tasks exceed the budget.
- **Recurring tasks** — completing a `daily`/`weekly` task auto-generates its next occurrence (see the `Task`/`Pet` methods in *Smarter Scheduling* above).

### Sample CLI output (`python main.py`)

The `main.py` demo script exercises the same classes without the UI:

```
Owner: Tanisha (available time: 120 min)

Biscuit — Golden Retriever, age 3
    - Morning walk (30 min)
    - Feeding (10 min)
    - Grooming (20 min)
    Total task time: 60 min

Whiskers — Cat, age 5
    - Play time (25 min)
    - Litter cleaning (15 min)
    Total task time: 40 min

Plan for Tanisha:
    Total time for all tasks: 100 min
    Leftover available time: 20 min

Tasks sorted by time (shortest first):
    - Feeding (10 min)
    - Litter cleaning (15 min)
    - Grooming (20 min)
    - Play time (25 min)
    - Morning walk (30 min)

Completed tasks:
    - Feeding (10 min)
    - Litter cleaning (15 min)
Remaining tasks:
    - Grooming (20 min)
    - Play time (25 min)
    - Morning walk (30 min)
```
