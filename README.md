# PawPal+

PawPal+ is a pet-care planner built with Python and Streamlit. Add pets and care tasks, filter tasks by pet, type, or status, and generate a daily plan based on priority, deadlines, and the owner's available time.

## Features

- Manage an owner's pet list and add pets with basic profile information.
- Create care tasks with a pet, type, duration, priority, deadline, and recurrence frequency.
- Filter the task list by pet, task type, and completion status; view matching tasks in deadline order.
- Generate a daily plan from 8:00 AM by default. The scheduler excludes completed and future-due tasks, prioritizes high-priority tasks, and skips tasks that do not fit the owner's time budget.
- View scheduling warnings for overlapping tasks, missed deadlines, and time-budget overruns.
- Review a plan explanation, including why tasks were prioritized and which tasks were skipped.
- Use the Python scheduling API to create the next daily or weekly occurrence when a recurring task is marked complete, and to rank pets by pending care minutes.
- Save owner, pet, and task data to `data.json` so it is restored between app sessions.

## Quick Start

Create an environment and install the app dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Start the Streamlit app:

```bash
python3 -m streamlit run app.py
```

To run the terminal demonstration instead:

```bash
python3 main.py
```

## Using the App

1. Enter the owner's name and daily care-time budget.
2. Add one or more pets.
3. Add each pet's care tasks, including duration, priority, deadline, and frequency.
4. Use the pet, type, and status filters to find tasks. The task table is ordered by deadline, with tasks that have no deadline last.
5. Select **Generate schedule** to create the daily plan. Review any warnings and expand **Plan explanation** for the scheduler's rationale.

## Priority Indicators

The task list and generated schedule color the **Priority** cell to make urgency easy to scan: high priority uses bright coral, medium uses amber, and low uses muted slate. The priority text remains visible alongside its color. In `app.py`, `style_priority_cells()` returns the cell styles, `pandas.DataFrame.style.apply()` applies them to each table, and Streamlit's `st.table()` renders the styled tables. 

## Persistence

When the app starts, it loads the owner, pets, and tasks from `data.json` in the project folder. If the file does not exist, PawPal+ starts with a new owner profile. Changes to the owner's name or time budget, and newly added pets or tasks, are saved back to JSON. Task deadlines and scheduled times are stored as ISO-formatted datetimes. The runtime data file is ignored by Git because it can contain personal owner and pet information.

Files updated for persistence: `pawpal_system.py` adds `Owner.save_to_json()` and `Owner.load_from_json()`; `app.py` loads saved data at startup and saves changes; `tests/test_pawpal.py` verifies a JSON round trip; `.gitignore` excludes `data.json`; and this README documents the workflow.

## Scheduling Algorithms

| Capability | Method | Behavior |
|---|---|---|
| Daily planning | `Scheduler.generate_daily_plan()` | Sorts eligible incomplete tasks, assigns sequential start times, and stays within the owner's daily minute budget. Tasks that do not fit are recorded as skipped. |
| Priority ordering | `Scheduler.sort_tasks()` | Sorts by high, medium, then low priority; breaks ties by deadline and title. |
| Deadline ordering | `Scheduler.sort_by_time()` | Sorts chronologically by deadline and places undated tasks last. |
| Task filtering | `Scheduler.filter_tasks()` | Filters by pet object or case-insensitive pet name, task type, and completion status. |
| Conflict warnings | `Scheduler.detect_conflicts()` | Returns messages for overlapping tasks, including same-pet and cross-pet overlaps, missed deadlines, and budget overruns. |
| Overdue lookup | `Scheduler.get_overdue_tasks()` and `Task.is_overdue()` | Finds incomplete tasks with deadlines earlier than the current time. |
| Recurrence | `Task.mark_task_complete()` | Marks a task complete and creates the next daily or weekly occurrence for its pet. One-time tasks do not recur. |
| Pet workload ranking | `Scheduler.rank_pet_workloads()` | Ranks pets by pending task minutes due by the scheduler's date; completed and future-due tasks are excluded. Tasks without a deadline are included. |
| Plan explanation | `Scheduler.explain_plan()` | Summarizes the plan, priority rationale, budget usage, skipped tasks, and conflicts. |

Recurring-task completion and workload ranking are implemented in the Python API; the current Streamlit interface does not yet include controls for marking a task complete or viewing workload rankings.

## Demo Walkthrough

The Streamlit interface lets the owner set a name and daily care-time budget, add pets, and create tasks with a type, duration, priority, deadline, and frequency. The task list can be filtered by pet, type, and completion status; matching tasks are shown in deadline order.

Example workflow:

1. Add Mochi, a dog, and Whiskers, a cat.
2. Add Mochi's morning walk and medication, then add Whiskers' breakfast task.
3. Filter the task list to Mochi's pending tasks, or sort the full list by deadline.
4. Select **Generate schedule**. The scheduler considers incomplete tasks due by today, prioritizes high-priority tasks and earlier deadlines, assigns sequential start times from 8:00 AM by default, and respects the owner's time budget.
5. Review the daily plan, any conflict warnings, and the expandable plan explanation. The warning logic identifies overlaps, including tasks for the same or different pets, deadline overruns, and budget overruns.

The terminal demo also exercises deadline sorting, pet-name filtering, and duplicate-time conflict detection. Example output from `python3 main.py`:

```text
Today's Schedule
Owner: JJ | Date: 2026-10-10
08:00 - Breakfast for Whiskers (10 min, high priority)
08:10 - Medication for Mochi (5 min, high priority)
08:15 - Morning walk for Mochi (30 min, medium priority)

Tasks sorted by deadline
08:30 - Breakfast
09:00 - Medication
10:00 - Morning walk

Pending tasks for Mochi
Morning walk (30 min)
Medication (5 min)

Conflict check
Warning: Morning walk (Mochi) overlaps with Medication (Mochi) [same pet: Mochi].
```

## Tests

Install the dependencies and run the test suite:

```bash
python3 -m pytest
```

For coverage reporting, install the optional `pytest-cov` plugin and run:

```bash
python3 -m pip install pytest-cov
python3 -m pytest --cov
```


