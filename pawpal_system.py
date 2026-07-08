"""PawPal+ system classes.

Class stubs based on diagrams/uml.mmd, implemented as dataclasses.
No scheduling logic yet — just the structure (attributes and
relationships) from the UML.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    """A single pet care activity (e.g. a walk or feeding)."""

    name: str
    duration: int  # minutes


@dataclass
class Pet:
    """A pet that has care tasks."""

    name: str
    animal_type: str
    age: int
    tasks: list[Task] = field(default_factory=list)  # Pet "has" Tasks


@dataclass
class Owner:
    """The pet owner, with a daily time budget."""

    name: str
    available_time: int  # minutes available today
    pet: Optional[Pet] = None  # Owner "owns" a Pet


@dataclass
class Plan:
    """The generated daily plan summarizing an Owner and Pet."""

    owner_name: str  # from Owner
    pet_name: str    # from Pet
    leftover_time: int  # available_time left after scheduled tasks
    tasks: list[Task] = field(default_factory=list)  # Tasks the plan schedules
