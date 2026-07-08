"""PawPal+ system classes.

Class stubs based on diagrams/uml.mmd, implemented as dataclasses.
No scheduling logic yet — just the structure (attributes and
relationships) from the UML.
"""

from dataclasses import dataclass, field, replace
from datetime import date, time, timedelta
from itertools import combinations
from typing import Optional

# How often a recurring task repeats. "none" means it happens only once.
RECURRENCE_STEPS = {
    "none": None,
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
}


@dataclass
class Task:
    """A single pet care activity (e.g. a walk or feeding)."""

    name: str
    duration: int  # minutes
    completed: bool = False  # status: True once the task is done
    recurrence: str = "none"  # "none", "daily", or "weekly"
    due_date: Optional[date] = None  # when this occurrence is scheduled for
    start_time: Optional[time] = None  # time of day this task starts
    pet_name: Optional[str] = None  # which pet this task belongs to

    def next_occurrence(self):
        """Build the next occurrence of a recurring task.

        Returns a fresh, not-yet-completed Task whose due date is today plus
        one recurrence step (today + 1 day for "daily", today + 7 days for
        "weekly"), computed with timedelta. Returns None for a one-off task
        ("none"), which has no next occurrence.
        """
        step = RECURRENCE_STEPS.get(self.recurrence)
        if step is None:  # "none" or an unrecognized recurrence
            return None
        next_due = date.today() + step
        return replace(self, completed=False, due_date=next_due)

    def mark_complete(self):
        """Mark this task as completed.

        If the task is daily or weekly, this also creates and returns the
        next occurrence so the routine automatically continues. Returns
        None for a one-off task.
        """
        self.completed = True
        return self.next_occurrence()


@dataclass
class Pet:
    """A pet that has care tasks."""

    name: str
    animal_type: str
    age: int
    tasks: list[Task] = field(default_factory=list)  # Pet "has" Tasks

    def add_task(self, task):
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def complete_task(self, task):
        """Mark one of this pet's tasks complete and auto-schedule its next
        occurrence.

        For a daily/weekly task, the freshly created next occurrence is
        appended to this pet's task list and returned. For a one-off task,
        nothing new is added and None is returned.
        """
        upcoming = task.mark_complete()
        if upcoming is not None:
            self.tasks.append(upcoming)
        return upcoming


@dataclass
class Owner:
    """The pet owner, with a daily time budget."""

    name: str
    available_time: int  # minutes available today
    pet: Optional[Pet] = None  # Owner "owns" a Pet

    def add_pet(self, pet):
        """Attach a pet to this owner."""
        self.pet = pet


@dataclass
class Plan:
    """The generated daily plan summarizing an Owner and Pet."""

    owner_name: str  # from Owner
    pet_name: str    # from Pet
    leftover_time: int  # available_time left after scheduled tasks
    tasks: list[Task] = field(default_factory=list)  # Tasks the plan schedules

    def sort_by_time(self):
        """Sort the plan's tasks in place by duration (shortest first)."""
        self.tasks.sort(key=lambda task: task.duration)
        return self.tasks

    def filter_by_status(self, completed=True):
        """Return the plan's tasks matching the given completion status.

        Pass completed=True (default) for finished tasks, or
        completed=False for tasks still to do.
        """
        return [task for task in self.tasks if task.completed == completed]

    def detect_conflicts(self):
        """Warn about tasks whose scheduled times overlap.

        Lightweight strategy: only not-yet-completed tasks that have a
        start_time are considered. Two tasks conflict when they share the
        same due_date and their time windows [start, start + duration)
        overlap — the owner can't be in two places at once, whether the
        tasks belong to the same pet or different pets. Returns a list of
        human-readable warning strings (empty when there are no conflicts).
        """

        def window(task):
            """Return (start_minute, end_minute) from midnight for a task."""
            start = task.start_time.hour * 60 + task.start_time.minute
            return start, start + task.duration

        def label(task):
            """Describe a task as 'Name (Pet)' when the pet is known."""
            return f"{task.name} ({task.pet_name})" if task.pet_name else task.name

        def clock(minute):
            """Format a minute-of-day count back into HH:MM."""
            return f"{minute // 60:02d}:{minute % 60:02d}"

        schedulable = [
            t for t in self.tasks if t.start_time is not None and not t.completed
        ]

        warnings = []
        for a, b in combinations(schedulable, 2):
            if a.due_date != b.due_date:
                continue  # different days can't clash
            a_start, a_end = window(a)
            b_start, b_end = window(b)
            if a_start < b_end and b_start < a_end:  # half-open overlap
                when = a.due_date.isoformat() if a.due_date else "an unscheduled day"
                warnings.append(
                    f"⚠️ Conflict on {when}: "
                    f"'{label(a)}' {clock(a_start)}-{clock(a_end)} overlaps "
                    f"'{label(b)}' {clock(b_start)}-{clock(b_end)}."
                )
        return warnings
