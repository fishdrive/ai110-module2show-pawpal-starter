"""Class skeletons for PawPal+."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Owner:
    name: str
    email: str = ""
    phone: str = ""
    pets: list[Pet] = field(default_factory=list)
    available_minutes_per_day: int = 120
    preferences: dict[str, str] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass

    def set_availability(self, minutes: int) -> None:
        pass


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
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_pending_tasks(self) -> list[Task]:
        pass

    def get_summary(self) -> str:
        pass


@dataclass
class Task:
    title: str
    task_type: str
    duration_minutes: int
    pet: Pet | None = None
    priority: str = "medium"
    due_time: datetime | None = None
    frequency: str = "once"
    is_completed: bool = False
    notes: str = ""

    def mark_complete(self) -> Task | None:
        pass

    def reschedule(self, new_time: datetime) -> None:
        pass

    def is_overdue(self) -> bool:
        pass

    def is_high_priority(self) -> bool:
        pass

    def get_details(self) -> str:
        pass


@dataclass
class Scheduler:
    owner: Owner
    date: date = field(default_factory=date.today)
    daily_plan: list[Task] = field(default_factory=list)

    def generate_daily_plan(self) -> list[Task]:
        pass

    def sort_tasks(self) -> list[Task]:
        pass

    def detect_conflicts(self) -> list[str]:
        pass

    def get_overdue_tasks(self) -> list[Task]:
        pass

    def filter_tasks(
        self,
        pet: Pet | None = None,
        task_type: str | None = None,
        status: str | bool | None = None,
    ) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass
