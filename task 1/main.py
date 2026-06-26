import streamlit as st
import json
import os

# ============================================
# DecodeLabs - Project 1: To-Do List
# Features: Add, View, Delete, Complete, Save
# UI: Streamlit | Storage: JSON File
# ============================================

DATA_FILE = "tasks.json"

# ---------- FILE PERSISTENCE ----------

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# ---------- PAGE CONFIG ----------

st.set_page_config(page_title="DecodeLabs To-Do", page_icon="✅")

# ---------- SESSION STATE ----------

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

if "next_id" not in st.session_state:
    ids = [t["id"] for t in st.session_state.tasks]
    st.session_state.next_id = max(ids) + 1 if ids else 1

# ---------- HEADER ----------

st.title("📋 My To-Do List")
st.caption("DecodeLabs • Project 1")

# ---------- STATS ----------

tasks = st.session_state.tasks
total = len(tasks)
done_count = sum(1 for t in tasks if t["done"])
pending_count = total - done_count

col1, col2, col3 = st.columns(3)
col1.metric("Total", total)
col2.metric("Done", done_count)
col3.metric("Pending", pending_count)

st.divider()

# ---------- ADD TASK ----------

st.subheader("Add New Task")

new_task = st.text_input(
    label="Task",
    placeholder="e.g. Finish Python assignment...",
    label_visibility="collapsed"
)

if st.button("＋ Add Task", type="primary", use_container_width=True):
    if new_task.strip() == "":
        st.warning("Please enter a task before adding.")
    else:
        task_dict = {
            "id": st.session_state.next_id,
            "title": new_task.strip(),
            "done": False
        }
        st.session_state.tasks.append(task_dict)
        st.session_state.next_id += 1
        save_tasks(st.session_state.tasks)
        st.success(f'"{new_task.strip()}" added!')
        st.rerun()

st.divider()

# ---------- VIEW TASKS ----------

st.subheader("Your Tasks")

if len(st.session_state.tasks) == 0:
    st.info("No tasks yet. Add one above to get started!")
else:
    for task in st.session_state.tasks:
        col1, col2, col3 = st.columns([0.7, 0.15, 0.15])

        with col1:
            status = "✅" if task["done"] else "🔵"
            title = f"~~{task['title']}~~" if task["done"] else task["title"]
            st.write(f"{status} **#{task['id']}** — {title}")

        with col2:
            btn_label = "↩️" if task["done"] else "✔️"
            if st.button(btn_label, key=f"done_{task['id']}", use_container_width=True):
                for t in st.session_state.tasks:
                    if t["id"] == task["id"]:
                        t["done"] = not t["done"]
                        break
                save_tasks(st.session_state.tasks)
                st.rerun()

        with col3:
            if st.button("🗑️", key=f"del_{task['id']}", use_container_width=True):
                st.session_state.tasks = [
                    t for t in st.session_state.tasks if t["id"] != task["id"]
                ]
                save_tasks(st.session_state.tasks)
                st.rerun()

# ---------- CLEAR ALL ----------

if len(st.session_state.tasks) > 0:
    st.divider()
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_b:
        if st.button("🗑 Clear All Tasks", use_container_width=True):
            st.session_state.tasks = []
            save_tasks([])
            st.rerun()