"""Demo script for PawPal+.

Creates an owner and a couple of pets, gives the pets some care tasks,
and prints everything out. This is a quick manual check of the classes
in pawpal_system.py (no scheduling logic yet).
"""

from pawpal_system import Owner, Pet, Task, Plan


def main():
    # 1. Create an owner with a daily time budget (in minutes).
    owner = Owner(name="Tanisha", available_time=120)

    # 2. Create at least two pets.
    biscuit = Pet(name="Biscuit", animal_type="Golden Retriever", age=3)
    whiskers = Pet(name="Whiskers", animal_type="Cat", age=5)

    # Give the owner a primary pet (Owner "owns" a Pet).
    owner.pet = biscuit

    # 3. Add at least three tasks with different durations.
    biscuit.tasks.append(Task(name="Morning walk", duration=30))
    biscuit.tasks.append(Task(name="Feeding", duration=10))
    biscuit.tasks.append(Task(name="Grooming", duration=20))

    whiskers.tasks.append(Task(name="Litter cleaning", duration=15))
    whiskers.tasks.append(Task(name="Play time", duration=25))

    # Print a simple summary so we can see the objects were built correctly.
    pets = [biscuit, whiskers]

    print(f"Owner: {owner.name} (available time: {owner.available_time} min)\n")

    # Collect every task across all pets so we can total them up.
    all_tasks = []
    for pet in pets:
        print(f"{pet.name} — {pet.animal_type}, age {pet.age}")
        total = 0
        for task in pet.tasks:
            print(f"    - {task.name} ({task.duration} min)")
            total += task.duration
        all_tasks.extend(pet.tasks)
        print(f"    Total task time: {total} min\n")

    # Build a Plan: add up all task times and subtract from the owner's time.
    total_task_time = sum(task.duration for task in all_tasks)
    leftover = owner.available_time - total_task_time

    plan = Plan(
        owner_name=owner.name,
        pet_name=", ".join(pet.name for pet in pets),
        leftover_time=leftover,
        tasks=all_tasks,
    )

    print(f"Plan for {plan.owner_name}:")
    print(f"    Total time for all tasks: {total_task_time} min")
    print(f"    Leftover available time: {plan.leftover_time} min")


if __name__ == "__main__":
    main()
