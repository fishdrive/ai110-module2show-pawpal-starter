from datetime import date, datetime, time

from pawpal_system import Owner, Pet, Scheduler, Task


today = date.today()
owner = Owner(
    name="Jordan Fisher",
    email="jordan@example.com",
    available_minutes_per_day=90,
)

mochi = Pet(name="Mochi", species="dog", breed="Shiba Inu", age=3)
whiskers = Pet(name="Whiskers", species="cat", age=5)
owner.add_pet(mochi)
owner.add_pet(whiskers)

morning_walk = Task(
    title="Morning walk",
    task_type="walk",
    duration_minutes=30,
    priority="medium",
    due_time=datetime.combine(today, time(10, 0)),
)
mochi.add_task(morning_walk)

breakfast = Task(
    title="Breakfast",
    task_type="feeding",
    duration_minutes=10,
    priority="high",
    due_time=datetime.combine(today, time(8, 30)),
)
whiskers.add_task(breakfast)

medication = Task(
    title="Medication",
    task_type="medication",
    duration_minutes=5,
    priority="high",
    due_time=datetime.combine(today, time(9, 0)),
)
mochi.add_task(medication)

scheduler = Scheduler(owner=owner, date=today)
scheduled_tasks = scheduler.generate_daily_plan()

print("Today's Schedule")
print(f"Owner: {owner.name} | Date: {today.isoformat()}")
for task in scheduled_tasks:
    start = task.scheduled_start.strftime("%H:%M")
    pet_name = task.pet.name if task.pet else "Unassigned"
    print(
        f"{start} - {task.title} for {pet_name} "
        f"({task.duration_minutes} min, {task.priority} priority)"
    )

print("\nTasks sorted by deadline")
for task in scheduler.sort_by_time():
    deadline = task.due_time.strftime("%H:%M") if task.due_time else "No deadline"
    print(f"{deadline} - {task.title}")

print("\nPending tasks for Mochi")
for task in scheduler.filter_tasks(pet="Mochi", status="pending"):
    print(f"{task.title} ({task.duration_minutes} min)")

shared_start = datetime.combine(today, time(8, 15))
morning_walk.reschedule(shared_start)
medication.reschedule(shared_start)
scheduler.daily_plan = [morning_walk, medication]

print("\nConflict check")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"Warning: {warning}")
else:
    print("No scheduling conflicts found.")
