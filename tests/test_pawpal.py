"""Tests for the PawPal+ system classes."""

from pawpal_system import Pet, Task


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
