from datetime import date, datetime, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "pawpal_owner" not in st.session_state:
    st.session_state.pawpal_owner = Owner(name="Jordan")
if "pawpal_plan_generated" not in st.session_state:
    st.session_state.pawpal_plan_generated = False

owner = st.session_state.pawpal_owner
scheduler = Scheduler(owner)

st.title("PawPal+")

owner_name = st.text_input("Owner name", value=owner.name, key="owner_name")
if owner_name != owner.name:
    owner.name = owner_name
    st.session_state.pawpal_plan_generated = False

available_minutes = st.number_input(
    "Daily pet-care time budget (minutes)",
    min_value=0,
    max_value=1440,
    value=owner.available_minutes_per_day,
    step=15,
    key="available_minutes",
)
if available_minutes != owner.available_minutes_per_day:
    owner.set_availability(int(available_minutes))
    st.session_state.pawpal_plan_generated = False

st.divider()
st.subheader("Pets")

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_breed = st.text_input("Breed (optional)")
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if not pet_name.strip():
        st.error("Enter a name for the pet.")
    else:
        owner.add_pet(
            Pet(name=pet_name.strip(), species=pet_species, breed=pet_breed.strip())
        )
        st.session_state.pawpal_plan_generated = False
        st.success(f"Added {pet_name.strip()}.")

if owner.pets:
    for pet in owner.pets:
        st.write(pet.get_summary())
else:
    st.info("Add a pet to start planning care tasks.")

st.divider()
st.subheader("Care tasks")

if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        selected_pet = st.selectbox(
            "Pet",
            owner.pets,
            format_func=lambda pet: pet.name,
        )
        task_title = st.text_input("Task title")
        task_type = st.selectbox(
            "Task type",
            ["feeding", "walk", "medication", "appointment", "grooming", "enrichment"],
        )
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        due_date = st.date_input("Deadline date", value=date.today())
        due_time = st.time_input("Deadline time", value=time(9, 0))
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        if not task_title.strip():
            st.error("Enter a title for the task.")
        else:
            selected_pet.add_task(
                Task(
                    title=task_title.strip(),
                    task_type=task_type,
                    duration_minutes=int(duration),
                    pet=selected_pet,
                    priority=priority,
                    due_time=datetime.combine(due_date, due_time),
                    frequency=frequency,
                )
            )
            st.session_state.pawpal_plan_generated = False
            st.success(f"Added {task_title.strip()} for {selected_pet.name}.")
else:
    st.info("Add a pet before creating care tasks.")

tasks = owner.get_all_tasks()
if tasks:
    st.table(
        [
            {
                "Pet": task.pet.name if task.pet else "Unassigned",
                "Task": task.title,
                "Type": task.task_type,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority,
                "Deadline": task.due_time.strftime("%Y-%m-%d %H:%M")
                if task.due_time
                else "None",
                "Status": "Completed" if task.is_completed else "Pending",
            }
            for task in tasks
        ]
    )

st.divider()
st.subheader("Today's schedule")

if st.button("Generate schedule", disabled=not tasks):
    scheduler.generate_daily_plan()
    st.session_state.pawpal_daily_plan = scheduler.daily_plan
    st.session_state.pawpal_skipped_tasks = scheduler.skipped_tasks
    st.session_state.pawpal_plan_explanation = scheduler.explain_plan()
    st.session_state.pawpal_plan_generated = True

if st.session_state.pawpal_plan_generated:
    daily_plan = st.session_state.pawpal_daily_plan
    if daily_plan:
        st.table(
            [
                {
                    "Time": task.scheduled_start.strftime("%H:%M"),
                    "Pet": task.pet.name if task.pet else "Unassigned",
                    "Task": task.title,
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": task.priority,
                }
                for task in daily_plan
            ]
        )
    else:
        st.info("No pending tasks fit in today's schedule.")

    st.write(st.session_state.pawpal_plan_explanation)
