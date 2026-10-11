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

```
Today's Schedule
Owner: Jordan | Date: 2026-10-10
08:00 - Breakfast for Prime (10 min, high priority)
08:10 - Medication for Timus (5 min, high priority)
08:15 - Morning walk for Timus (30 min, medium priority)
```

## 🧪 Testing PawPal+

//command to run tests is python3 -m pytest
//Tests covered: 
Pet/task ownership, adding and removing tasks, and collecting an owner’s tasks.
Daily and weekly recurrence, including creating the next occurrence, undated daily tasks, one-time tasks, and preventing repeat completion from creating duplicates.
Schedule priority ordering, daily time-budget limits, assigned start times, and reporting skipped tasks.
Chronological deadline sorting, with undated tasks last.
Ranking pets by pending task minutes while excluding completed and future-due tasks.
Conflict warnings for overlapping tasks on the same pet or different pets, plus daily budget overruns.
Task validation and filtering by pet object or name, task type, and completion status.

```bash
Sample test output:

```text
$ python3 -m pytest
tests/test_pawpal.py .........                                            [100%]

9 passed in 0.04s
```
//Confidence is 5 stars considering 9 tests were passed in 0.04s. 

# Run with coverage:
pytest --cov
```
Installed pytest-cov and reran python3 -m pytest --cov successfully: 9 tests passed. Total coverage is 92% (pawpal_system.py: 87%; tests: 100%)




## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Daily plan generation | `Scheduler.generate_daily_plan()` | Schedules incomplete tasks due by the selected date, starting at 8:00 AM by default, without exceeding the owner's daily time budget. |
| Priority sorting | `Scheduler.sort_tasks()` | Orders tasks by high, medium, then low priority; ties use earlier deadlines and task titles. |
| Deadline sorting | `Scheduler.sort_by_time()` | Orders tasks by deadline, placing tasks without a deadline last. |
| Task filtering | `Scheduler.filter_tasks()` | Filters by pet instance or name, task type, and completion status. |
| Conflict detection | `Scheduler.detect_conflicts()` | Warns about overlapping tasks, including same-pet and cross-pet conflicts, missed deadlines, and budget overruns. |
| Overdue task lookup | `Scheduler.get_overdue_tasks()`, `Task.is_overdue()` | Finds incomplete tasks whose deadlines have passed. |
| Recurring tasks | `Task.mark_task_complete()` | Completing a daily or weekly task creates the next occurrence and adds it to the pet's tasks. One-time tasks do not recur. |
| Pet workload ranking | `Scheduler.rank_pet_workloads()` | Ranks pets by pending task minutes due on or before the scheduler's date; completed and future-due tasks are excluded. |
| Plan explanation | `Scheduler.explain_plan()` | Describes scheduled tasks, the priority/deadline rationale, time-budget omissions, and detected conflicts. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->


