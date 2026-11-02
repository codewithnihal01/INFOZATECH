
import streamlit as st
import json
import os
from datetime import date

st.set_page_config(
    page_title="TaskFlow — Productivity",
    page_icon="✦",
    layout="wide"
)

FILE = "tasks.json"

# ---------- LOAD DATA ----------
if "tasks" not in st.session_state:
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                st.session_state.tasks = json.load(f)
        except:
            st.session_state.tasks = []
    else:
        st.session_state.tasks = []

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def save_tasks():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.tasks, f, indent=4)

def get_status(task):
    if task.get("completed", False):
        return "Completed"
    return task.get("status", "To Do")

def set_status(task, status):
    task["status"] = status
    task["completed"] = status == "Completed"

def task_date(task):
    try:
        return date.fromisoformat(task.get("due_date", date.today().isoformat()))
    except:
        return date.today()

# ---------- THEME ----------
if st.session_state.dark_mode:
    bg = "#0b1020"
    panel = "#151c30"
    card = "#1a2340"
    text = "#f5f7ff"
    muted = "#a0aecb"
    border = "#293452"
else:
    bg = "#f3f5fb"
    panel = "#ffffff"
    card = "#ffffff"
    text = "#172033"
    muted = "#64748b"
    border = "#e2e8f0"

st.markdown(f"""
<style>
.stApp {{
    background: {bg};
    color: {text};
    font-family: 'Segoe UI', sans-serif;
}}

.block-container {{
    max-width: 1450px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
}}

h1,h2,h3,h4,p,label {{
    color: {text};
}}

[data-testid="stSidebar"] {{
    background: {panel};
    border-right: 1px solid {border};
}}

[data-testid="stSidebar"] * {{
    color: {text} !important;
}}

.hero {{
    background: linear-gradient(120deg,#4338ca,#7c3aed,#c026d3);
    padding: 35px;
    border-radius: 26px;
    box-shadow: 0 15px 40px rgba(124,58,237,.25);
    margin-bottom: 25px;
}}

.hero h1 {{
    color: white !important;
    font-size: 38px;
    font-weight: 800;
}}

.hero p {{
    color: #ede9fe !important;
    font-size: 16px;
}}

.metric {{
    background: {panel};
    border: 1px solid {border};
    border-radius: 22px;
    padding: 22px;
    min-height: 145px;
    box-shadow: 0 8px 25px rgba(0,0,0,.06);
}}

.metric-label {{
    color: {muted} !important;
    font-size: 14px;
    font-weight: 600;
}}

.metric-value {{
    color: {text} !important;
    font-size: 36px;
    font-weight: 800;
    padding-top: 8px;
}}

.metric-icon {{
    font-size: 25px;
}}

.kanban-header {{
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 12px;
    font-size: 17px;
    font-weight: 800;
}}

.todo-header {{
    background: #312e81;
    color: #c7d2fe;
}}

.progress-header {{
    background: #164e63;
    color: #a5f3fc;
}}

.done-header {{
    background: #14532d;
    color: #bbf7d0;
}}

.task-card {{
    background: {card};
    border: 1px solid {border};
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}}

.task-title {{
    font-size: 17px;
    font-weight: 750;
    color: {text} !important;
}}

.task-info {{
    font-size: 12px;
    color: {muted} !important;
}}

.stButton button {{
    border-radius: 12px;
    font-weight: 700;
    transition: .2s ease;
}}

.stButton button:hover {{
    transform: translateY(-2px);
    border-color: #8b5cf6;
}}

.stTextInput input,
.stTextArea textarea,
.stDateInput input {{
    border-radius: 12px;
}}

div[data-testid="stProgressBar"] > div > div {{
    background: linear-gradient(90deg,#6366f1,#c026d3);
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-radius: 18px;
}}

.footer {{
    text-align: center;
    color: {muted};
    padding: 25px;
    font-size: 13px;
}}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <h1 style="color:#a78bfa !important;font-size:32px;">
    ✦ TaskFlow
    </h1>
    <p style="font-size:12px;letter-spacing:2px;">
    PRODUCTIVITY WORKSPACE
    </p>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🗂️ My Tasks", "📈 Analytics", "⚙️ Settings"],
        label_visibility="collapsed"
    )

    st.divider()

    st.session_state.dark_mode = st.toggle(
        "🌙 Dark Theme",
        value=st.session_state.dark_mode
    )

    st.divider()

    st.markdown("### ✨ Daily Inspiration")
    st.info("Small steps every day lead to big achievements.")

    st.caption("TASKFLOW • BUILT WITH PYTHON")

# ---------- DATA ----------
tasks = st.session_state.tasks
total = len(tasks)
completed = sum(1 for t in tasks if get_status(t) == "Completed")
pending = sum(1 for t in tasks if get_status(t) == "To Do")
progress_count = sum(1 for t in tasks if get_status(t) == "In Progress")
overdue = sum(
    1 for t in tasks
    if get_status(t) != "Completed" and task_date(t) < date.today()
)

progress = completed / total if total else 0

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <h1>✦ Your Productivity Hub</h1>
    <p>Plan your day. Focus on what matters. Make progress every day.</p>
</div>
""", unsafe_allow_html=True)

# ---------- DASHBOARD ----------
if page == "🏠 Dashboard":

    st.markdown("## 📊 Workspace Overview")

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("📋", "TOTAL TASKS", total),
        ("⏳", "TO DO", pending),
        ("⚡", "IN PROGRESS", progress_count),
        ("✅", "COMPLETED", completed),
    ]

    for col, item in zip([c1,c2,c3,c4], metrics):
        icon, label, value = item
        with col:
            st.markdown(f"""
            <div class="metric">
                <div class="metric-label">{icon} {label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    a, b = st.columns([1.5,1])

    with a:
        st.markdown("### 🎯 Completion Progress")
        st.progress(progress)
        st.markdown(f"**{int(progress*100)}%** of your tasks completed")

    with b:
        st.markdown("### 🚨 Deadline Overview")
        st.metric("Overdue Tasks", overdue)
        st.caption("Keep an eye on deadlines!")

    st.divider()

    # Kanban Board
    st.markdown("## 🧩 Task Board")
    st.caption("Your workflow at a glance.")

    col_todo, col_progress, col_done = st.columns(3)

    columns = [
        (col_todo, "To Do", "todo-header", "📝"),
        (col_progress, "In Progress", "progress-header", "⚡"),
        (col_done, "Completed", "done-header", "🎉")
    ]

    for column, status, header_class, emoji in columns:

        with column:
            matching = [
                (i,t) for i,t in enumerate(tasks)
                if get_status(t) == status
            ]

            st.markdown(
                f'<div class="kanban-header {header_class}">'
                f'{emoji} {status} <span style="float:right">'
                f'{len(matching)}</span></div>',
                unsafe_allow_html=True
            )

            if not matching:
                st.caption("No tasks here yet.")

            for i, task in matching:

                with st.container(border=True):

                    st.markdown(
                        f'<div class="task-title">{task["task"]}</div>',
                        unsafe_allow_html=True
                    )

                    priority = task.get("priority", "🟡 Medium")
                    category = task.get("category", "🎯 Other")
                    due = task_date(task)

                    st.caption(f"{priority}  •  {category}")
                    st.caption(f"📅 {due.strftime('%d %b %Y')}")

                    if task.get("description"):
                        st.caption(task["description"])

                    if status == "To Do":
                        if st.button("▶ Start", key=f"start_{i}", use_container_width=True):
                            set_status(tasks[i], "In Progress")
                            save_tasks()
                            st.rerun()

                    elif status == "In Progress":
                        if st.button("✓ Complete", key=f"finish_{i}", use_container_width=True):
                            set_status(tasks[i], "Completed")
                            save_tasks()
                            st.rerun()

                    else:
                        if st.button("↩ Reopen", key=f"reopen_{i}", use_container_width=True):
                            set_status(tasks[i], "To Do")
                            save_tasks()
                            st.rerun()

                    if st.button("🗑 Delete", key=f"board_delete_{i}", use_container_width=True):
                        tasks.pop(i)
                        save_tasks()
                        st.rerun()

    st.divider()

    st.markdown("## 📅 Upcoming Tasks")

    upcoming = sorted(
        [
            t for t in tasks
            if get_status(t) != "Completed"
        ],
        key=lambda t: task_date(t)
    )[:5]

    if upcoming:
        for task in upcoming:
            due = task_date(task)
            if due < date.today():
                st.warning(f"🚨 **{task['task']}** — Overdue ({due})")
            elif due == date.today():
                st.info(f"📍 **{task['task']}** — Due Today")
            else:
                st.write(f"📅 **{task['task']}** — {due}")
    else:
        st.success("All tasks completed! 🎉")

# ---------- MY TASKS ----------
elif page == "🗂️ My Tasks":

    st.markdown("## 🗂️ Task Management")
    st.caption("Create, search, edit, and organize your tasks.")

    with st.expander("➕ Create New Task", expanded=True):

        with st.form("create_task", clear_on_submit=True):

            name = st.text_input("Task Name")
            description = st.text_area("Description")

            c1,c2,c3 = st.columns(3)

            with c1:
                category = st.selectbox(
                    "Category",
                    ["📚 Study","💼 Work","🏠 Personal","🎯 Other"]
                )

            with c2:
                priority = st.selectbox(
                    "Priority",
                    ["🔴 High","🟡 Medium","🟢 Low"]
                )

            with c3:
                due_date = st.date_input("Due Date", value=date.today())

            submit = st.form_submit_button(
                "🚀 Add Task",
                use_container_width=True
            )

            if submit:
                if name.strip():
                    tasks.append({
                        "task": name.strip(),
                        "description": description.strip(),
                        "category": category,
                        "priority": priority,
                        "due_date": due_date.isoformat(),
                        "completed": False,
                        "status": "To Do"
                    })
                    save_tasks()
                    st.success("Task created!")
                    st.rerun()
                else:
                    st.warning("Enter a task name.")

    st.divider()

    search = st.text_input("🔍 Search tasks")

    status_filter = st.selectbox(
        "Filter by status",
        ["All","To Do","In Progress","Completed"]
    )

    for i, task in enumerate(tasks):

        if search.lower() not in task["task"].lower():
            continue

        if status_filter != "All" and get_status(task) != status_filter:
            continue

        with st.container(border=True):

            c1,c2,c3 = st.columns([5,1,1])

            with c1:
                st.markdown(f"### {task['task']}")
                st.caption(
                    f"{task.get('priority','🟡 Medium')} • "
                    f"{task.get('category','🎯 Other')} • "
                    f"{get_status(task)}"
                )
                st.caption(f"📅 {task_date(task)}")
                if task.get("description"):
                    st.write(task["description"])

            with c2:
                if get_status(task) == "To Do":
                    if st.button("▶ Start", key=f"taskstart_{i}"):
                        set_status(tasks[i], "In Progress")
                        save_tasks()
                        st.rerun()

                elif get_status(task) == "In Progress":
                    if st.button("✓ Done", key=f"taskdone_{i}"):
                        set_status(tasks[i], "Completed")
                        save_tasks()
                        st.rerun()

                else:
                    if st.button("↩ Reopen", key=f"taskreopen_{i}"):
                        set_status(tasks[i], "To Do")
                        save_tasks()
                        st.rerun()

            with c3:
                if st.button("🗑 Delete", key=f"taskdelete_{i}"):
                    tasks.pop(i)
                    save_tasks()
                    st.rerun()

            with st.expander("✏️ Edit Task"):
                with st.form(f"edit_task_{i}"):

                    new_name = st.text_input("Task Name", value=task["task"])
                    new_desc = st.text_area(
                        "Description",
                        value=task.get("description", "")
                    )

                    categories = ["📚 Study","💼 Work","🏠 Personal","🎯 Other"]
                    priorities = ["🔴 High","🟡 Medium","🟢 Low"]

                    new_category = st.selectbox(
                        "Category",
                        categories,
                        index=categories.index(task.get("category","🎯 Other"))
                    )

                    new_priority = st.selectbox(
                        "Priority",
                        priorities,
                        index=priorities.index(task.get("priority","🟡 Medium"))
                    )

                    new_date = st.date_input(
                        "Due Date",
                        value=task_date(task)
                    )

                    save_edit = st.form_submit_button("💾 Save")

                    if save_edit:
                        if new_name.strip():
                            tasks[i]["task"] = new_name.strip()
                            tasks[i]["description"] = new_desc.strip()
                            tasks[i]["category"] = new_category
                            tasks[i]["priority"] = new_priority
                            tasks[i]["due_date"] = new_date.isoformat()
                            save_tasks()
                            st.success("Updated!")
                            st.rerun()
                        else:
                            st.warning("Task name required.")

# ---------- ANALYTICS ----------
elif page == "📈 Analytics":

    st.markdown("## 📈 Productivity Analytics")
    st.caption("Visualize your performance and workflow.")

    c1,c2 = st.columns(2)

    with c1:
        st.markdown("### Workflow Distribution")

        st.bar_chart({
            "Tasks": {
                "To Do": pending,
                "In Progress": progress_count,
                "Completed": completed
            }
        })

    with c2:
        st.markdown("### Priority Breakdown")

        st.bar_chart({
            "Tasks": {
                "High": sum(1 for t in tasks if t.get("priority") == "🔴 High"),
                "Medium": sum(1 for t in tasks if t.get("priority") == "🟡 Medium"),
                "Low": sum(1 for t in tasks if t.get("priority") == "🟢 Low")
            }
        })

    st.markdown("### 🗂️ Category Breakdown")

    category_data = {}

    for task in tasks:
        category = task.get("category", "Other")
        category_data[category] = category_data.get(category, 0) + 1

    if category_data:
        st.bar_chart(category_data)
    else:
        st.info("Add tasks to generate analytics.")

# ---------- SETTINGS ----------
elif page == "⚙️ Settings":

    st.markdown("## ⚙️ Settings")

    st.markdown("### Appearance")
    st.write("Use the Dark Theme switch in the sidebar.")

    st.divider()

    st.markdown("### Data")
    st.write(f"Your saved tasks: **{total}**")

    if st.button("🗑 Clear All Tasks"):
        st.session_state.confirm_clear = True

    if st.session_state.get("confirm_clear", False):

        st.warning("Confirm deletion of all tasks.")

        c1,c2 = st.columns(2)

        with c1:
            if st.button("Yes, Clear All"):
                st.session_state.tasks = []
                save_tasks()
                st.session_state.confirm_clear = False
                st.rerun()

        with c2:
            if st.button("Cancel"):
                st.session_state.confirm_clear = False
                st.rerun()

    st.divider()

    st.markdown("### 💎 About TaskFlow")
    st.write("TaskFlow is a Python-based productivity dashboard with persistent task management.")

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    ✦ TASKFLOW • PRODUCTIVITY WORKSPACE<br>
    Plan beautifully. Execute confidently. ✨
</div>
""", unsafe_allow_html=True)
