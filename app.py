from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Task, Plan

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

# Create the Owner once and keep it across reruns (don't rebuild on refresh).
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_time=120)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, max_value=30, value=2)

# Create the Pet once, nested under the owner (Owner "owns" Pet).
if st.session_state.owner.pet is None:
    st.session_state.owner.add_pet(Pet(name=pet_name, animal_type=species, age=int(age)))

pet = st.session_state.owner.pet

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2 = st.columns(2)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
    start_time = st.time_input("Start time")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"])

# Add tasks via the Pet's own method (Pet "has" Tasks) — no separate list needed.
# Give each task a start_time and today's due_date so the Plan can detect
# scheduling conflicts, and stamp the pet_name for readable warnings.
if st.button("Add task"):
    pet.add_task(
        Task(
            name=task_title,
            duration=int(duration),
            recurrence=recurrence,
            start_time=start_time,
            due_date=date.today(),
            pet_name=pet.name,
        )
    )

if pet.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "name": t.name,
                "start_time": t.start_time.strftime("%H:%M") if t.start_time else "—",
                "duration_minutes": t.duration,
                "recurrence": t.recurrence,
                "completed": t.completed,
            }
            for t in pet.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Builds a Plan from the tasks above, sorted shortest-first, with conflict warnings.")


def duration_row(task):
    """One table row for a task in the generated plan."""
    return {
        "name": task.name,
        "start_time": task.start_time.strftime("%H:%M") if task.start_time else "—",
        "duration_minutes": task.duration,
        "recurrence": task.recurrence,
    }


if st.button("Generate schedule"):
    if not pet.tasks:
        st.info("Add at least one task above before generating a schedule.")
    else:
        # Build the Plan from the owner's time budget and the pet's tasks.
        scheduled_time = sum(t.duration for t in pet.tasks)
        plan = Plan(
            owner_name=st.session_state.owner.name,
            pet_name=pet.name,
            leftover_time=st.session_state.owner.available_time - scheduled_time,
            tasks=list(pet.tasks),
        )

        # 1. Conflict warnings — surface overlapping tasks first.
        conflicts = plan.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(warning)
        else:
            st.success("✅ No scheduling conflicts — every task fits without overlapping.")

        # 2. Time-budget summary.
        if plan.leftover_time >= 0:
            st.success(
                f"⏱️ {scheduled_time} min scheduled · "
                f"{plan.leftover_time} min of {st.session_state.owner.available_time} min still free."
            )
        else:
            st.warning(
                f"⏱️ Over budget by {-plan.leftover_time} min — "
                f"tasks need {scheduled_time} min but only "
                f"{st.session_state.owner.available_time} min is available."
            )

        # 3. Full plan, sorted shortest-first via the Plan's own method.
        st.markdown("### 📋 Plan (sorted by time, shortest first)")
        st.table([duration_row(t) for t in plan.sort_by_time()])

        # 4. Split remaining vs. completed using filter_by_status.
        remaining = plan.filter_by_status(completed=False)
        completed = plan.filter_by_status(completed=True)

        col_todo, col_done = st.columns(2)
        with col_todo:
            st.markdown("#### 🟡 To do")
            if remaining:
                st.table([duration_row(t) for t in remaining])
            else:
                st.success("All tasks completed! 🎉")
        with col_done:
            st.markdown("#### ✅ Completed")
            if completed:
                st.table([duration_row(t) for t in completed])
            else:
                st.info("Nothing completed yet.")
