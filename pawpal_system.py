"""Class skeletons for PawPal+."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from pathlib import Path


@dataclass
class Owner:
    name: str
    email: str = ""
    phone: str = ""
    pets: list[Pet] = field(default_factory=list)
    available_minutes_per_day: int = 120
    preferences: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate the owner's daily care-time budget."""
        self.set_availability(self.available_minutes_per_day)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner if it is not already listed."""
        if all(existing is not pet for existing in self.pets):
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's collection."""
        self.pets = [existing for existing in self.pets if existing is not pet]

    def get_all_tasks(self) -> list[Task]:
        """Return each task belonging to any of the owner's pets."""
        tasks: list[Task] = []
        seen: set[int] = set()
        for pet in self.pets:
            for task in pet.tasks:
                if id(task) not in seen:
                    tasks.append(task)
                    seen.add(id(task))
        return tasks

    def set_availability(self, minutes: int) -> None:
        """Set the owner's available daily care time in minutes."""
        if minutes < 0:
            raise ValueError("Available minutes cannot be negative.")
        self.available_minutes_per_day = minutes

    def save_to_json(self, file_path: str | Path = "data.json") -> None:
        """Save this owner and nested pet tasks to a JSON file."""
        data = {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "available_minutes_per_day": self.available_minutes_per_day,
            "preferences": self.preferences,
            "pets": [
                {
                    "name": pet.name,
                    "species": pet.species,
                    "breed": pet.breed,
                    "age": pet.age,
                    "weight": pet.weight,
                    "special_needs": pet.special_needs,
                    "tasks": [
                        {
                            "title": task.title,
                            "task_type": task.task_type,
                            "duration_minutes": task.duration_minutes,
                            "priority": task.priority,
                            "due_time": task.due_time.isoformat()
                            if task.due_time
                            else None,
                            "scheduled_start": task.scheduled_start.isoformat()
                            if task.scheduled_start
                            else None,
                            "frequency": task.frequency,
                            "is_completed": task.is_completed,
                            "notes": task.notes,
                        }
                        for task in pet.tasks
                    ],
                }
                for pet in self.pets
            ],
        }
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    @classmethod
    def load_from_json(cls, file_path: str | Path = "data.json") -> Owner:
        """Load an owner and nested pet tasks from a JSON file."""
        data = json.loads(Path(file_path).read_text(encoding="utf-8"))
        owner = cls(
            name=data["name"],
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            available_minutes_per_day=data.get("available_minutes_per_day", 120),
            preferences=data.get("preferences", {}),
        )
        for pet_data in data.get("pets", []):
            pet = Pet(
                name=pet_data["name"],
                species=pet_data["species"],
                breed=pet_data.get("breed", ""),
                age=pet_data.get("age", 0),
                weight=pet_data.get("weight", 0.0),
                special_needs=pet_data.get("special_needs", ""),
            )
            owner.add_pet(pet)
            for task_data in pet_data.get("tasks", []):
                task = Task(
                    title=task_data["title"],
                    task_type=task_data["task_type"],
                    duration_minutes=task_data["duration_minutes"],
                    pet=pet,
                    priority=task_data.get("priority", "medium"),
                    due_time=(
                        datetime.fromisoformat(task_data["due_time"])
                        if task_data.get("due_time")
                        else None
                    ),
                    scheduled_start=(
                        datetime.fromisoformat(task_data["scheduled_start"])
                        if task_data.get("scheduled_start")
                        else None
                    ),
                    frequency=task_data.get("frequency", "once"),
                    is_completed=task_data.get("is_completed", False),
                    notes=task_data.get("notes", ""),
                )
                pet.add_task(task)
        return owner


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    age: int = 0
    weight: float = 0.0
    special_needs: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Assign a task to this pet."""
        if task.pet is not None and task.pet is not self:
            raise ValueError("A task cannot be assigned to more than one pet.")
        if all(existing is not task for existing in self.tasks):
            task.pet = self
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet and clear its pet reference."""
        self.tasks = [existing for existing in self.tasks if existing is not task]
        if task.pet is self:
            task.pet = None

    def get_pending_tasks(self) -> list[Task]:
        """Return this pet's tasks that are not completed."""
        return [task for task in self.tasks if not task.is_completed]

    def get_summary(self) -> str:
        """Return a readable summary of this pet's profile."""
        summary = f"{self.name} ({self.species}"
        if self.breed:
            summary += f", {self.breed}"
        summary += f"), age {self.age}, {self.weight:g} kg"
        if self.special_needs:
            summary += f". Special needs: {self.special_needs}"
        return summary


@dataclass
class Task:
    title: str
    task_type: str
    duration_minutes: int
    pet: Pet | None = None
    priority: str = "medium"
    due_time: datetime | None = None
    scheduled_start: datetime | None = None
    frequency: str = "once"
    is_completed: bool = False
    notes: str = ""

    def __post_init__(self) -> None:
        """Validate and normalize task duration, priority, frequency, and type."""
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero.")
        self.priority = self.priority.strip().lower()
        if self.priority not in {"high", "medium", "low"}:
            raise ValueError("Priority must be high, medium, or low.")
        self.frequency = self.frequency.strip().lower()
        if self.frequency not in {"once", "daily", "weekly"}:
            raise ValueError("Frequency must be once, daily, or weekly.")
        self.task_type = self.task_type.strip().lower()

    def mark_task_complete(self, now: datetime | None = None) -> Task | None:
        """Complete this task and create its next occurrence if recurring."""
        if self.is_completed:
            return None
        self.is_completed = True
        if self.frequency == "once":
            return None

        interval = timedelta(days=1 if self.frequency == "daily" else 7)
        next_due_time = (self.due_time or now or datetime.now()) + interval
        next_task = Task(
            title=self.title,
            task_type=self.task_type,
            duration_minutes=self.duration_minutes,
            pet=self.pet,
            priority=self.priority,
            due_time=next_due_time,
            frequency=self.frequency,
            notes=self.notes,
        )
        if self.pet is not None:
            self.pet.add_task(next_task)
        return next_task

    def mark_complete(self, now: datetime | None = None) -> Task | None:
        """Backward-compatible alias for mark_task_complete()."""
        return self.mark_task_complete(now)

    def reschedule(self, new_time: datetime) -> None:
        """Set the task's scheduled start time."""
        self.scheduled_start = new_time

    def is_overdue(self, now: datetime | None = None) -> bool:
        """Return whether this incomplete task's deadline has passed."""
        current_time = now or datetime.now()
        return (
            not self.is_completed
            and self.due_time is not None
            and self.due_time.timestamp() < current_time.timestamp()
        )

    def is_high_priority(self) -> bool:
        """Return whether this task has high priority."""
        return self.priority == "high"

    def get_details(self) -> str:
        """Return a formatted description of this task."""
        pet_name = self.pet.name if self.pet is not None else "unassigned"
        due = self.due_time.strftime("%Y-%m-%d %H:%M") if self.due_time else "no deadline"
        start = (
            self.scheduled_start.strftime("%H:%M")
            if self.scheduled_start
            else "unscheduled"
        )
        return (
            f"{self.title} for {pet_name} [{self.task_type}], "
            f"{self.duration_minutes} min, {self.priority} priority, "
            f"starts {start}, due {due}"
        )


@dataclass
class Scheduler:
    owner: Owner
    date: date = field(default_factory=date.today)
    daily_plan: list[Task] = field(default_factory=list)
    start_time: time = time(8, 0)
    skipped_tasks: list[Task] = field(default_factory=list, init=False, repr=False)

    def generate_daily_plan(self) -> list[Task]:
        """Schedule eligible tasks in priority order within the owner's time budget."""
        for task in self.daily_plan:
            task.scheduled_start = None

        candidates = [
            task
            for task in self.owner.get_all_tasks()
            if not task.is_completed
            and (task.due_time is None or task.due_time.date() <= self.date)
        ]
        self.daily_plan = []
        self.skipped_tasks = []
        minutes_used = 0
        next_start = datetime.combine(self.date, self.start_time)

        for task in self.sort_tasks(candidates):
            if minutes_used + task.duration_minutes > self.owner.available_minutes_per_day:
                self.skipped_tasks.append(task)
                continue
            task.scheduled_start = next_start
            self.daily_plan.append(task)
            minutes_used += task.duration_minutes
            next_start += timedelta(minutes=task.duration_minutes)

        return self.daily_plan.copy()

    def sort_tasks(self, tasks: list[Task] | None = None) -> list[Task]:
        """Sort tasks by priority, deadline, and title."""
        candidates = tasks if tasks is not None else self.owner.get_all_tasks()
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            candidates,
            key=lambda task: (
                priority_order[task.priority],
                task.due_time.timestamp() if task.due_time else float("inf"),
                task.title.casefold(),
            ),
        )

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Sort tasks by deadline, placing tasks without a deadline last."""
        candidates = tasks if tasks is not None else self.owner.get_all_tasks()
        return sorted(
            candidates,
            key=lambda task: (
                task.due_time.timestamp() if task.due_time else float("inf")
            ),
        )

    def rank_pet_workloads(self) -> list[tuple[Pet, int]]:
        """Rank pets by pending task minutes due on or before this date."""
        workloads = [
            (
                pet,
                sum(
                    task.duration_minutes
                    for task in pet.get_pending_tasks()
                    if task.due_time is None or task.due_time.date() <= self.date
                ),
            )
            for pet in self.owner.pets
        ]
        return sorted(workloads, key=lambda workload: workload[1], reverse=True)

    def detect_conflicts(self) -> list[str]:
        """Report schedule overlaps, missed deadlines, and budget overruns."""
        conflicts: list[str] = []
        scheduled = sorted(
            (task for task in self.daily_plan if task.scheduled_start is not None),
            key=lambda task: task.scheduled_start.timestamp(),
        )

        for index, task in enumerate(scheduled):
            start_timestamp = task.scheduled_start.timestamp()
            end_timestamp = start_timestamp + task.duration_minutes * 60
            for other in scheduled[index + 1 :]:
                other_start = other.scheduled_start.timestamp()
                if other_start >= end_timestamp:
                    break
                task_pet = task.pet.name if task.pet else "Unassigned"
                other_pet = other.pet.name if other.pet else "Unassigned"
                if task.pet is not None and task.pet is other.pet:
                    relationship = f"same pet: {task_pet}"
                elif task.pet is not None and other.pet is not None:
                    relationship = f"different pets: {task_pet} and {other_pet}"
                else:
                    relationship = "involving an unassigned task"
                conflicts.append(
                    f"{task.title} ({task_pet}) overlaps with "
                    f"{other.title} ({other_pet}) [{relationship}]."
                )

            if task.due_time and end_timestamp > task.due_time.timestamp():
                conflicts.append(f"{task.title} is scheduled to finish after its deadline.")

        total_minutes = sum(task.duration_minutes for task in self.daily_plan)
        if total_minutes > self.owner.available_minutes_per_day:
            conflicts.append(
                f"Plan uses {total_minutes} minutes, exceeding the "
                f"{self.owner.available_minutes_per_day}-minute daily budget."
            )
        return conflicts

    def get_overdue_tasks(self) -> list[Task]:
        """Return all overdue tasks belonging to the owner's pets."""
        return [task for task in self.owner.get_all_tasks() if task.is_overdue()]

    def filter_tasks(
        self,
        pet: Pet | str | None = None,
        task_type: str | None = None,
        status: str | bool | None = None,
    ) -> list[Task]:
        """Filter the owner's tasks by pet or pet name, type, and completion status."""
        tasks = self.owner.get_all_tasks()
        if pet is not None:
            if isinstance(pet, Pet):
                tasks = [task for task in tasks if task.pet is pet]
            else:
                pet_name = pet.strip().casefold()
                tasks = [
                    task
                    for task in tasks
                    if task.pet is not None and task.pet.name.casefold() == pet_name
                ]
        if task_type is not None:
            requested_type = task_type.strip().lower()
            tasks = [task for task in tasks if task.task_type == requested_type]
        if status is not None:
            if isinstance(status, bool):
                is_completed = status
            elif status.strip().lower() in {"completed", "complete"}:
                is_completed = True
            elif status.strip().lower() in {"pending", "incomplete"}:
                is_completed = False
            else:
                raise ValueError("Status must be pending, completed, or a boolean.")
            tasks = [task for task in tasks if task.is_completed is is_completed]
        return tasks

    def explain_plan(self) -> str:
        """Describe the daily plan, selection rationale, and any conflicts."""
        if not self.daily_plan:
            if self.skipped_tasks:
                return "No pending tasks fit within the available time for this day."
            return "No pending tasks are due for this day."

        total_minutes = sum(task.duration_minutes for task in self.daily_plan)
        lines = [f"Daily plan for {self.owner.name} on {self.date.isoformat()}"]
        for task in self.daily_plan:
            start = task.scheduled_start.strftime("%H:%M") if task.scheduled_start else "?"
            lines.append(f"{start} - {task.get_details()}")
        lines.append(
            f"Prioritized high-priority tasks, then earlier deadlines; "
            f"scheduled {total_minutes} of "
            f"{self.owner.available_minutes_per_day} available minutes."
        )
        if self.skipped_tasks:
            skipped_titles = ", ".join(task.title for task in self.skipped_tasks)
            lines.append(f"Left out due to the time budget: {skipped_titles}.")
        conflicts = self.detect_conflicts()
        if conflicts:
            lines.append("Conflicts: " + " ".join(conflicts))
        return "\n".join(lines)
