from datetime import date, datetime

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def test_pet_task_relationship_and_owner_task_collection():
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", "walk", 20)
    pet.add_task(task)
    owner = Owner("Jordan", pets=[pet])

    assert task.pet is pet
    assert owner.get_all_tasks() == [task]
    assert pet.get_pending_tasks() == [task]

    pet.remove_task(task)
    assert task.pet is None
    assert owner.get_all_tasks() == []


def test_recurring_task_completion_creates_next_occurrence():
    pet = Pet("Mochi", "dog")
    task = Task(
        "Medication",
        "medication",
        5,
        pet=pet,
        frequency="daily",
        due_time=datetime(2026, 10, 10, 9, 0),
    )
    pet.add_task(task)

    next_task = task.mark_task_complete()

    assert task.is_completed
    assert next_task is not None
    assert next_task.due_time == datetime(2026, 10, 11, 9, 0)
    assert next_task in pet.tasks

    undated = Task("Brush teeth", "dental", 3, pet=pet, frequency="daily")
    next_undated = undated.mark_task_complete(now=datetime(2026, 10, 10, 9, 0))
    assert next_undated.due_time == datetime(2026, 10, 11, 9, 0)

    weekly = Task(
        "Grooming",
        "grooming",
        30,
        pet=pet,
        frequency="weekly",
        due_time=datetime(2026, 10, 10, 10, 0),
    )
    pet.add_task(weekly)
    next_weekly = weekly.mark_task_complete()

    assert next_weekly is not None
    assert next_weekly.due_time == datetime(2026, 10, 17, 10, 0)
    assert next_weekly in pet.tasks
    assert weekly.mark_task_complete() is None

    one_time = Task("Brush", "grooming", 5, pet=pet)
    assert one_time.mark_complete() is None
    assert one_time.is_completed


def test_scheduler_prioritizes_tasks_within_daily_budget():
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Short walk", "walk", 15, pet=pet, priority="low"))
    pet.add_task(Task("Medication", "medication", 25, pet=pet, priority="high"))
    pet.add_task(Task("Grooming", "grooming", 20, pet=pet, priority="medium"))
    owner = Owner("Jordan", pets=[pet], available_minutes_per_day=40)
    scheduler = Scheduler(owner, date=date(2026, 10, 10))

    plan = scheduler.generate_daily_plan()

    assert [task.title for task in plan] == ["Medication", "Short walk"]
    assert plan[0].scheduled_start == datetime(2026, 10, 10, 8, 0)
    assert plan[1].scheduled_start == datetime(2026, 10, 10, 8, 25)
    assert "Grooming" in scheduler.explain_plan()


def test_scheduler_sort_by_time_orders_deadlines_and_puts_undated_last():
    pet = Pet("Mochi", "dog")
    later = Task("Evening walk", "walk", 20, pet=pet, due_time=datetime(2026, 10, 10, 18))
    undated = Task("Play", "enrichment", 15, pet=pet)
    earlier = Task("Medication", "medication", 5, pet=pet, due_time=datetime(2026, 10, 10, 9))
    scheduler = Scheduler(Owner("Jordan", pets=[pet]))

    assert scheduler.sort_by_time([later, undated, earlier]) == [earlier, later, undated]


def test_scheduler_ranks_pet_workload_by_pending_minutes_due_today():
    mochi = Pet("Mochi", "dog")
    whiskers = Pet("Whiskers", "cat")
    mochi.add_task(Task("Walk", "walk", 25, pet=mochi))
    mochi.add_task(Task("Medication", "medication", 5, pet=mochi))
    completed_task = Task("Grooming", "grooming", 60, pet=whiskers)
    whiskers.add_task(completed_task)
    completed_task.mark_task_complete()
    whiskers.add_task(Task(
        "Vet visit", "appointment", 30, pet=whiskers,
        due_time=datetime(2026, 10, 11, 9, 0),
    ))
    owner = Owner("Jordan", pets=[mochi, whiskers])
    scheduler = Scheduler(owner, date=date(2026, 10, 10))

    workloads = scheduler.rank_pet_workloads()

    assert workloads == [(mochi, 30), (whiskers, 0)]


def test_conflict_detection_reports_overlaps_and_budget_overrun():
    pet = Pet("Mochi", "dog")
    first = Task("Walk", "walk", 30, pet=pet)
    second = Task("Grooming", "grooming", 30, pet=pet)
    first.scheduled_start = datetime(2026, 10, 10, 8, 0)
    second.scheduled_start = datetime(2026, 10, 10, 8, 15)
    scheduler = Scheduler(Owner("Jordan", pets=[pet], available_minutes_per_day=45))
    scheduler.daily_plan = [first, second]

    conflicts = scheduler.detect_conflicts()

    assert any("overlaps" in conflict for conflict in conflicts)
    assert any("daily budget" in conflict for conflict in conflicts)


def test_conflict_detection_identifies_same_and_different_pets():
    mochi = Pet("Mochi", "dog")
    whiskers = Pet("Whiskers", "cat")
    walk = Task("Walk", "walk", 30, pet=mochi)
    grooming = Task("Grooming", "grooming", 20, pet=mochi)
    feeding = Task("Feeding", "feeding", 10, pet=whiskers)
    shared_start = datetime(2026, 10, 10, 9, 0)
    for task in (walk, grooming, feeding):
        task.scheduled_start = shared_start

    scheduler = Scheduler(Owner("Jordan", pets=[mochi, whiskers]))
    scheduler.daily_plan = [walk, grooming, feeding]

    conflicts = scheduler.detect_conflicts()

    assert any("same pet: Mochi" in conflict for conflict in conflicts)
    assert any("different pets: Mochi and Whiskers" in conflict for conflict in conflicts)


def test_task_validation_and_filtering():
    pet = Pet("Mochi", "dog")
    task = Task("Walk", "walk", 20, pet=pet, priority="HIGH")
    pet.add_task(task)
    scheduler = Scheduler(Owner("Jordan", pets=[pet]))

    assert task.is_high_priority()
    assert scheduler.filter_tasks(pet=pet, task_type="WALK", status="pending") == [task]
    with pytest.raises(ValueError):
        Task("Impossible", "walk", 0)


def test_scheduler_filters_by_pet_name_and_completion_status():
    mochi = Pet("Mochi", "dog")
    whiskers = Pet("Whiskers", "cat")
    completed_task = Task("Medication", "medication", 5, pet=mochi)
    pending_task = Task("Walk", "walk", 20, pet=mochi)
    other_pet_task = Task("Feeding", "feeding", 10, pet=whiskers)
    mochi.add_task(completed_task)
    mochi.add_task(pending_task)
    whiskers.add_task(other_pet_task)
    completed_task.mark_task_complete()
    scheduler = Scheduler(Owner("Jordan", pets=[mochi, whiskers]))

    assert scheduler.filter_tasks(pet="MOCHI") == [completed_task, pending_task]
    assert scheduler.filter_tasks(status="completed") == [completed_task]
    assert scheduler.filter_tasks(pet="mochi", status="pending") == [pending_task]