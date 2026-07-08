"""Tests for the PawPal+ system classes."""

from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Plan, Task


def test_task_completion():
    """Calling mark_complete() should change the task's status to done."""
    task = Task(name="Morning walk", duration=30)

    # A new task starts out not completed.
    assert task.completed is False

    task.mark_complete()

    # After marking complete, the status should be True.
    assert task.completed is True


def test_task_addition():
    """Adding a task to a Pet should increase that pet's task count."""
    pet = Pet(name="Biscuit", animal_type="Golden Retriever", age=3)

    # A new pet starts with no tasks.
    assert len(pet.tasks) == 0

    pet.tasks.append(Task(name="Feeding", duration=10))

    # The task count should now be 1.
    assert len(pet.tasks) == 1


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_plan(tasks):
    """Build a Plan wrapping the given tasks (owner/pet names don't matter)."""
    return Plan(owner_name="Jordan", pet_name="Mochi", leftover_time=0, tasks=list(tasks))


# ---------------------------------------------------------------------------
# Sorting — Plan.sort_by_time()
# ---------------------------------------------------------------------------

def test_sort_happy_path():
    """Tasks come back shortest-duration first."""
    plan = make_plan([
        Task(name="Walk", duration=30),
        Task(name="Feed", duration=10),
        Task(name="Groom", duration=20),
    ])

    ordered = plan.sort_by_time()

    assert [t.duration for t in ordered] == [10, 20, 30]


def test_sort_empty_list():
    """Sorting an empty plan returns an empty list, no crash."""
    plan = make_plan([])

    assert plan.sort_by_time() == []


def test_sort_single_task():
    """A one-task plan is returned unchanged."""
    plan = make_plan([Task(name="Walk", duration=30)])

    ordered = plan.sort_by_time()

    assert [t.name for t in ordered] == ["Walk"]


def test_sort_is_stable_for_equal_durations():
    """Equal-duration tasks keep their original insertion order (stable sort)."""
    plan = make_plan([
        Task(name="First", duration=15),
        Task(name="Second", duration=15),
        Task(name="Third", duration=15),
    ])

    ordered = plan.sort_by_time()

    assert [t.name for t in ordered] == ["First", "Second", "Third"]


def test_sort_mutates_in_place_and_is_idempotent():
    """sort_by_time() sorts self.tasks in place; a second call is a no-op."""
    plan = make_plan([
        Task(name="Walk", duration=30),
        Task(name="Feed", duration=10),
    ])

    plan.sort_by_time()

    # The Plan's own list is now reordered (side effect, not a copy).
    assert [t.duration for t in plan.tasks] == [10, 30]

    # Sorting again leaves it exactly the same.
    plan.sort_by_time()
    assert [t.duration for t in plan.tasks] == [10, 30]


def test_sort_orders_by_duration_not_start_time():
    """sort_by_time sorts by DURATION, not start_time (documents the naming quirk)."""
    plan = make_plan([
        Task(name="Late but short", duration=5, start_time=time(18, 0)),
        Task(name="Early but long", duration=60, start_time=time(6, 0)),
    ])

    ordered = plan.sort_by_time()

    # Despite the name, the 18:00 task comes first because it's shorter.
    assert [t.name for t in ordered] == ["Late but short", "Early but long"]


# ---------------------------------------------------------------------------
# Filtering — Plan.filter_by_status()
# ---------------------------------------------------------------------------

def test_filter_by_status_splits_completed_and_pending():
    """filter_by_status returns only tasks matching the requested status."""
    plan = make_plan([
        Task(name="Done", duration=10, completed=True),
        Task(name="Todo", duration=20, completed=False),
    ])

    assert [t.name for t in plan.filter_by_status(completed=True)] == ["Done"]
    assert [t.name for t in plan.filter_by_status(completed=False)] == ["Todo"]


def test_filter_by_status_all_pending_returns_empty_completed():
    """When nothing is completed, the completed filter returns []."""
    plan = make_plan([
        Task(name="A", duration=10),
        Task(name="B", duration=20),
    ])

    assert plan.filter_by_status(completed=True) == []
    assert len(plan.filter_by_status(completed=False)) == 2


# ---------------------------------------------------------------------------
# Recurring tasks — next_occurrence / mark_complete / Pet.complete_task
# ---------------------------------------------------------------------------

def test_one_off_has_no_next_occurrence():
    """A 'none' task returns None from mark_complete and schedules nothing."""
    task = Task(name="Vet visit", duration=45, recurrence="none")

    assert task.mark_complete() is None


def test_daily_next_occurrence_is_tomorrow():
    """Completing a daily task yields a fresh, incomplete copy due tomorrow."""
    task = Task(name="Walk", duration=30, recurrence="daily")

    nxt = task.mark_complete()

    assert nxt is not None
    assert nxt.completed is False
    assert nxt.due_date == date.today() + timedelta(days=1)


def test_weekly_next_occurrence_is_seven_days_out():
    """Weekly recurrence advances the due date by a week."""
    task = Task(name="Bath", duration=40, recurrence="weekly")

    nxt = task.mark_complete()

    assert nxt.due_date == date.today() + timedelta(weeks=1)


def test_next_occurrence_carries_over_fields():
    """The next occurrence copies duration, start_time and pet_name."""
    task = Task(
        name="Feed",
        duration=10,
        recurrence="daily",
        start_time=time(8, 0),
        pet_name="Mochi",
    )

    nxt = task.mark_complete()

    assert nxt.duration == 10
    assert nxt.start_time == time(8, 0)
    assert nxt.pet_name == "Mochi"


def test_unrecognized_recurrence_fails_safe():
    """An unknown recurrence value is treated like 'none' (no next occurrence)."""
    task = Task(name="Odd", duration=10, recurrence="monthly")

    assert task.next_occurrence() is None


def test_complete_task_appends_next_occurrence_to_pet():
    """Pet.complete_task adds the follow-up for a recurring task."""
    pet = Pet(name="Mochi", animal_type="cat", age=2)
    task = Task(name="Walk", duration=30, recurrence="daily")
    pet.add_task(task)

    upcoming = pet.complete_task(task)

    assert upcoming in pet.tasks
    assert len(pet.tasks) == 2


def test_complete_task_one_off_adds_nothing():
    """Completing a one-off task leaves the task list length unchanged."""
    pet = Pet(name="Mochi", animal_type="cat", age=2)
    task = Task(name="Vet visit", duration=45, recurrence="none")
    pet.add_task(task)

    assert pet.complete_task(task) is None
    assert len(pet.tasks) == 1


def test_double_complete_duplicates_occurrence():
    """KNOWN QUIRK: completing an already-done recurring task schedules again.

    Documents current behavior — mark_complete is not idempotent, so a second
    call creates a second follow-up. If completion is ever made idempotent,
    update this test.
    """
    pet = Pet(name="Mochi", animal_type="cat", age=2)
    task = Task(name="Walk", duration=30, recurrence="daily")
    pet.add_task(task)

    pet.complete_task(task)
    pet.complete_task(task)

    # Original + two follow-ups.
    assert len(pet.tasks) == 3


# ---------------------------------------------------------------------------
# Conflict detection — Plan.detect_conflicts()
# ---------------------------------------------------------------------------

def test_no_conflicts_when_no_start_times():
    """Tasks without start_time are ignored, so no conflicts are reported."""
    plan = make_plan([
        Task(name="Walk", duration=30),
        Task(name="Feed", duration=10),
    ])

    assert plan.detect_conflicts() == []


def test_empty_plan_has_no_conflicts():
    """A plan with no tasks reports no conflicts."""
    assert make_plan([]).detect_conflicts() == []


def test_exact_same_start_time_conflicts():
    """Two tasks starting at the same time on the same day overlap."""
    day = date.today()
    plan = make_plan([
        Task(name="Walk", duration=30, start_time=time(9, 0), due_date=day),
        Task(name="Feed", duration=15, start_time=time(9, 0), due_date=day),
    ])

    assert len(plan.detect_conflicts()) == 1


def test_back_to_back_tasks_do_not_conflict():
    """A task ending exactly when the next starts is NOT a conflict (half-open)."""
    day = date.today()
    plan = make_plan([
        Task(name="Walk", duration=30, start_time=time(9, 0), due_date=day),
        Task(name="Feed", duration=15, start_time=time(9, 30), due_date=day),
    ])

    assert plan.detect_conflicts() == []


def test_overlapping_windows_conflict():
    """Partially overlapping windows on the same day are reported."""
    day = date.today()
    plan = make_plan([
        Task(name="Walk", duration=30, start_time=time(9, 0), due_date=day),
        Task(name="Feed", duration=30, start_time=time(9, 15), due_date=day),
    ])

    assert len(plan.detect_conflicts()) == 1


def test_completed_task_never_conflicts():
    """A completed task is excluded from conflict checks."""
    day = date.today()
    plan = make_plan([
        Task(name="Walk", duration=30, start_time=time(9, 0), due_date=day, completed=True),
        Task(name="Feed", duration=30, start_time=time(9, 0), due_date=day),
    ])

    assert plan.detect_conflicts() == []


def test_different_days_do_not_conflict():
    """Same clock time on different due dates is not a conflict."""
    plan = make_plan([
        Task(name="Walk", duration=30, start_time=time(9, 0), due_date=date.today()),
        Task(
            name="Feed",
            duration=30,
            start_time=time(9, 0),
            due_date=date.today() + timedelta(days=1),
        ),
    ])

    assert plan.detect_conflicts() == []


# ---------------------------------------------------------------------------
# Owner / model edge cases
# ---------------------------------------------------------------------------

def test_owner_starts_with_no_pet():
    """A fresh owner has no pet until one is added."""
    owner = Owner(name="Jordan", available_time=120)

    assert owner.pet is None

    pet = Pet(name="Mochi", animal_type="cat", age=2)
    owner.add_pet(pet)

    assert owner.pet is pet
