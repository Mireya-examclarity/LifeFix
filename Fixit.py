import streamlit as st
from datetime import date, datetime

# ============================================================
# LIFE FIX 🧠
# Everyday Problems → Simple Software Solutions
# ============================================================

st.set_page_config(
    page_title="LifeFix",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #182848 0%, transparent 30%),
        radial-gradient(circle at 90% 20%, #4b134f 0%, transparent 25%),
        linear-gradient(135deg, #050505, #0b1020 50%, #12071a);
    colour: white;
}

h1, h2, h3, h4, p, label, span, div {
    colour: white !important;
}

.hero {
    text-align: center;
    padding: 50px 25px;
    border-radius: 30px;
    background:
        linear-gradient(
            135deg,
            rgba(40,60,120,.35),
            rgba(120,30,100,.25)
        );
    border: 1px solid rgba(255,255,255,.15);
    box-shadow: 0 0 60px rgba(80,100,255,.15);
    margin-bottom: 30px;
}

.hero-title {
    font-size: 65px;
    font-weight: 900;
    letter-spacing: 3px;
}

.hero-subtitle {
    font-size: 22px;
    colour: #b8c7ff !important;
}

.card {
    padding: 22px;
    border-radius: 20px;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.1);
    margin: 10px 0;
}

.task-card {
    padding: 18px;
    border-radius: 18px;
    background: rgba(255,255,255,.05);
    border-left: 5px solid #6c63ff;
    margin: 10px 0;
}

.high {
    border-left-colour: #ff4b4b;
}

.medium {
    border-left-colour: #ffa726;
}

.low {
    border-left-colour: #4caf50;
}

.big {
    font-size: 40px;
    font-weight: 800;
}

.footer {
    text-align: center;
    padding: 40px;
    colour: #777 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "tasks" not in st.session_state:
    st.session_state.tasks = []


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
🧠 LIFE<span style="colour:#6c63ff;">FIX</span>
</div>

<div class="hero-subtitle">
Small Problems. Smart Solutions.
</div>

<p>
Turn everyday problems into simple digital solutions.
</p>

<div style="font-size:60px;">
🧠 ⚡ 🛠️ ✨
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# PROJECT INTRO
# ============================================================

st.header("💡 What are we fixing?")

st.markdown("""
<div class="card">

<h3>😵 The Problem</h3>

<p>
When we have multiple assignments, projects, exams or
personal tasks, it can be difficult to decide what to
work on first.
</p>

<h3>⚡ The Solution</h3>

<p>
LifeFix analyzes your tasks using their deadlines,
estimated time and importance, then creates a suggested
order so you know what to do next.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🛠️ Add a Task")

    task_name = st.text_input(
        "Task name",
        placeholder="e.g. Physics assignment"
    )

    deadline = st.date_input(
        "Deadline",
        value=date.today()
    )

    hours = st.number_input(
        "Estimated hours",
        min_value=0.5,
        max_value=100.0,
        value=2.0,
        step=0.5
    )

    importance = st.select_slider(
        "Importance",
        options=[
            "Low",
            "Medium",
            "High"
        ],
        value="Medium"
    )

    if st.button(
        "➕ ADD TASK",
        use_container_width=True
    ):

        if task_name.strip():

            task = {
                "name": task_name.strip(),
                "deadline": deadline,
                "hours": hours,
                "importance": importance,
                "completed": False
            }

            st.session_state.tasks.append(task)

            st.success(
                f"Added: {task_name}"
            )

        else:

            st.warning(
                "Enter a task name."
            )


    st.divider()

    if st.button(
        "🗑️ CLEAR ALL TASKS",
        use_container_width=True
    ):

        st.session_state.tasks = []

        st.rerun()


# ============================================================
# TASK SCORING
# ============================================================

def calculate_score(task):

    today = date.today()

    days_left = (
        task["deadline"] - today
    ).days

    # Deadline score
    if days_left <= 0:
        deadline_score = 100

    elif days_left == 1:
        deadline_score = 90

    elif days_left <= 3:
        deadline_score = 75

    elif days_left <= 7:
        deadline_score = 55

    elif days_left <= 14:
        deadline_score = 35

    else:
        deadline_score = 15

    # Importance score
    importance_scores = {
        "Low": 20,
        "Medium": 50,
        "High": 100
    }

    importance_score = importance_scores[
        task["importance"]
    ]

    # Time score
    time_score = min(
        task["hours"] * 8,
        80
    )

    # Final score
    score = (
        deadline_score * 0.50
        +
        importance_score * 0.35
        +
        time_score * 0.15
    )

    return round(score, 1)


# ============================================================
# DASHBOARD
# ============================================================

st.divider()

st.header("📊 Your LifeFix Dashboard")

total = len(
    st.session_state.tasks
)

completed = sum(
    task["completed"]
    for task in st.session_state.tasks
)

remaining = total - completed

total_hours = sum(
    task["hours"]
    for task in st.session_state.tasks
    if not task["completed"]
)

d1, d2, d3, d4 = st.columns(4)

d1.metric(
    "📝 Tasks",
    total
)

d2.metric(
    "✅ Completed",
    completed
)

d3.metric(
    "⏳ Remaining",
    remaining
)

d4.metric(
    "⏱️ Hours Left",
    f"{total_hours:.1f}"
)


# ============================================================
# PROGRESS
# ============================================================

if total > 0:

    progress = completed / total

    st.subheader("🎯 Overall Progress")

    st.progress(
        progress
    )

    st.write(
        f"{completed}/{total} tasks completed "
        f"({int(progress * 100)}%)"
    )


# ============================================================
# TASK LIST
# ============================================================

st.divider()

st.header("📋 Your Tasks")

if not st.session_state.tasks:

    st.info(
        "No tasks yet. Add your first task from the sidebar! 👈"
    )

else:

    # Create sorted list
    sorted_tasks = sorted(
        st.session_state.tasks,
        key=calculate_score,
        reverse=True
    )

    for index, task in enumerate(sorted_tasks):

        score = calculate_score(task)

        days_left = (
            task["deadline"] - date.today()
        ).days

        if score >= 70:
            priority = "🔴 HIGH"
            css = "high"

        elif score >= 45:
            priority = "🟠 MEDIUM"
            css = "medium"

        else:
            priority = "🟢 LOW"
            css = "low"

        st.markdown(
            f"""
            <div class="task-card {css}">

            <h3>
            {index + 1}. {task["name"]}
            </h3>

            <p>
            📅 Deadline: {task["deadline"]}
            &nbsp;&nbsp;|&nbsp;&nbsp;
            ⏱️ {task["hours"]} hours
            &nbsp;&nbsp;|&nbsp;&nbsp;
            ⭐ {task["importance"]}
            </p>

            <p>
            {priority}
            &nbsp;&nbsp;
            • Priority Score: {score}
            </p>

            <p>
            {"⚠️ Due today!" if days_left == 0 else
             "🚨 Overdue!" if days_left < 0 else
             f"⏳ {days_left} day(s) remaining"}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        done = st.checkbox(
            "Mark as completed",
            value=task["completed"],
            key=f"done_{index}"
        )

        task["completed"] = done


# ============================================================
# WHAT SHOULD I DO NOW?
# ============================================================

st.divider()

st.header("⚡ What Should I Do Right Now?")

if st.session_state.tasks:

    incomplete = [
        task
        for task in st.session_state.tasks
        if not task["completed"]
    ]

    if incomplete:

        best_task = max(
            incomplete,
            key=calculate_score
        )

        score = calculate_score(
            best_task
        )

        st.markdown(
            f"""
            <div class="card"
            style="
            text-align:center;
            border:2px solid #6c63ff;
            box-shadow:0 0 30px rgba(108,99,255,.25);
            ">

            <p>🔥 LIFE FIX RECOMMENDS</p>

            <div class="big">
            {best_task["name"]}
            </div>

            <p>
            ⏱️ Estimated time:
            {best_task["hours"]} hours
            </p>

            <p>
            📅 Deadline:
            {best_task["deadline"]}
            </p>

            <p>
            🧠 Priority Score:
            {score}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.success(
            "Start this task first. "
            "LifeFix thinks it has the highest priority."
        )

    else:

        st.balloons()

        st.success(
            "🎉 EVERYTHING IS DONE!"
        )

else:

    st.info(
        "Add some tasks and I'll tell you what to do first."
    )


# ============================================================
# QUICK TIME PLANNER
# ============================================================

st.divider()

st.header("⏰ I Have Limited Time")

available_time = st.number_input(
    "How many hours do you have right now?",
    min_value=0.5,
    max_value=24.0,
    value=2.0,
    step=0.5
)

if st.button("⚡ BUILD MY MINI PLAN"):

    incomplete = [
        task
        for task in st.session_state.tasks
        if not task["completed"]
    ]

    if not incomplete:

        st.info(
            "You have no unfinished tasks."
        )

    else:

        sorted_tasks = sorted(
            incomplete,
            key=calculate_score,
            reverse=True
        )

        remaining_time = available_time

        st.subheader(
            f"🗓️ Your {available_time}-hour plan"
        )

        for task in sorted_tasks:

            if remaining_time <= 0:
                break

            time_used = min(
                task["hours"],
                remaining_time
            )

            st.write(
                f"### {task['name']}"
            )

            st.progress(
                time_used / task["hours"]
            )

            st.caption(
                f"Work for approximately "
                f"{time_used:.1f} hour(s)"
            )

            remaining_time -= time_used

        if remaining_time > 0:

            st.success(
                f"You still have "
                f"{remaining_time:.1f} hour(s) free."
            )


# ============================================================
# HOW IT WORKS
# ============================================================

st.divider()

st.header("🧠 How LifeFix Decides")

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("""
    <div class="card">

    <h3>📅 Deadline</h3>

    <p>
    Tasks with closer deadlines receive
    a higher priority.
    </p>

    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown("""
    <div class="card">

    <h3>⭐ Importance</h3>

    <p>
    More important tasks receive
    additional priority.
    </p>

    </div>
    """, unsafe_allow_html=True)


with c3:

    st.markdown("""
    <div class="card">

    <h3>⏱️ Time</h3>

    <p>
    Longer tasks are considered when
    building your plan.
    </p>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown("""
<div class="footer">

🧠 <b>LIFE FIX</b>

<br><br>

Small Problems → Smart Solutions

<br>

Built with Python and Streamlit

<br><br>

Project 3 🚀

</div>
""", unsafe_allow_html=True)
# ============================================================
# LIFE FIX — MORE EVERYDAY TOOLS 🚀
# ============================================================

st.divider()

st.header("🧰 LifeFix Toolbox")
st.write(
    "More small tools for everyday problems — all inside one place."
)

tool = st.selectbox(
    "Choose a tool",
    [
        "💰 Expense Splitter",
        "🎒 Smart Packing List",
        "🤔 Decision Maker",
        "📦 Where Did I Put It?",
        "🔢 Everyday Calculator",
        "💧 Break & Water Planner",
        "📊 LifeFix Statistics"
    ],
    key="toolbox"
)


# ============================================================
# 💰 EXPENSE SPLITTER
# ============================================================

if tool == "💰 Expense Splitter":

    st.subheader("💰 Split a Bill")

    st.write(
        "Going out with friends? Calculate how much each person owes."
    )

    amount = st.number_input(
        "Total bill",
        min_value=0.0,
        value=100.0,
        step=10.0,
        key="bill_amount"
    )

    people = st.number_input(
        "Number of people",
        min_value=1,
        max_value=100,
        value=2,
        step=1,
        key="bill_people"
    )

    tip = st.slider(
        "Tip %",
        0,
        30,
        0,
        key="bill_tip"
    )

    tax = st.slider(
        "Tax %",
        0,
        30,
        0,
        key="bill_tax"
    )

    if st.button(
        "🧮 SPLIT BILL",
        key="split_bill"
    ):

        tip_amount = amount * tip / 100
        tax_amount = amount * tax / 100

        final_amount = (
            amount
            + tip_amount
            + tax_amount
        )

        each_person = (
            final_amount / people
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Original",
            f"{amount:.2f}"
        )

        c2.metric(
            "Final Bill",
            f"{final_amount:.2f}"
        )

        c3.metric(
            "Each Person",
            f"{each_person:.2f}"
        )

        st.success(
            f"Everyone pays approximately {each_person:.2f}"
        )


# ============================================================
# 🎒 SMART PACKING LIST
# ============================================================

elif tool == "🎒 Smart Packing List":

    st.subheader("🎒 Smart Packing Assistant")

    st.write(
        "Tell LifeFix what kind of trip you're taking."
    )

    trip_type = st.selectbox(
        "Trip type",
        [
            "🏖️ Beach Trip",
            "🏔️ Mountain Trip",
            "🏙️ City Trip",
            "🏫 School Trip",
            "🚀 Space Camp",
            "✈️ General Travel"
        ],
        key="trip_type"
    )

    days = st.number_input(
        "Number of days",
        min_value=1,
        max_value=60,
        value=3,
        step=1,
        key="trip_days"
    )

    packing_lists = {

        "🏖️ Beach Trip": [
            "👕 T-shirts",
            "🩳 Shorts",
            "🩴 Sandals",
            "🧴 Sunscreen",
            "🕶️ Sunglasses",
            "🩱 Swimwear",
            "🧻 Towel",
            "💧 Water bottle",
            "🔌 Charger",
            "🪥 Toothbrush"
        ],

        "🏔️ Mountain Trip": [
            "🧥 Jacket",
            "👕 Warm clothes",
            "🥾 Hiking shoes",
            "🧦 Extra socks",
            "🧴 Sunscreen",
            "💧 Water bottle",
            "🔦 Flashlight",
            "🩹 First-aid kit",
            "🔋 Power bank",
            "🪥 Toothbrush"
        ],

        "🏙️ City Trip": [
            "👕 Clothes",
            "👟 Comfortable shoes",
            "💳 Wallet",
            "📱 Phone",
            "🔌 Charger",
            "🧴 Toiletries",
            "💧 Water bottle",
            "🎒 Backpack",
            "🕶️ Sunglasses"
        ],

        "🏫 School Trip": [
            "🎒 Backpack",
            "📓 Notebook",
            "✏️ Pens",
            "💧 Water bottle",
            "🍎 Snacks",
            "🧢 Cap",
            "🧴 Sunscreen",
            "📱 Phone",
            "🔌 Charger"
        ],

        "🚀 Space Camp": [
            "👕 Comfortable clothes",
            "👟 Shoes",
            "📓 Notebook",
            "✏️ Pens",
            "💻 Laptop",
            "🔌 Charger",
            "🎧 Headphones",
            "💧 Water bottle",
            "🎒 Backpack",
            "🚀 Curiosity"
        ],

        "✈️ General Travel": [
            "👕 Clothes",
            "👟 Shoes",
            "🪥 Toothbrush",
            "🧴 Toiletries",
            "📱 Phone",
            "🔌 Charger",
            "💳 Wallet",
            "💧 Water bottle",
            "🎒 Backpack"
        ]
    }

    items = packing_lists[trip_type]

    st.write(
        f"### Suggested list for {days} day(s)"
    )

    checked_items = []

    columns = st.columns(2)

    for i, item in enumerate(items):

        with columns[i % 2]:

            if st.checkbox(
                item,
                key=f"packing_{trip_type}_{i}"
            ):
                checked_items.append(item)

    progress = len(checked_items) / len(items)

    st.progress(progress)

    st.write(
        f"{len(checked_items)}/{len(items)} packed"
    )

    if progress == 1:

        st.balloons()

        st.success(
            "🎉 EVERYTHING IS PACKED!"
        )


# ============================================================
# 🤔 DECISION MAKER
# ============================================================

elif tool == "🤔 Decision Maker":

    st.subheader("🤔 Can't Decide?")

    st.write(
        "Compare two choices using the things that matter to you."
    )

    option_a = st.text_input(
        "Option A",
        placeholder="Example: Buy a laptop",
        key="decision_a"
    )

    option_b = st.text_input(
        "Option B",
        placeholder="Example: Buy a tablet",
        key="decision_b"
    )

    st.write("### ⭐ Rate what matters")

    importance_price = st.slider(
        "💰 Price importance",
        1,
        10,
        5,
        key="price_importance"
    )

    importance_quality = st.slider(
        "⭐ Quality importance",
        1,
        10,
        5,
        key="quality_importance"
    )

    importance_ease = st.slider(
        "😊 Ease of use importance",
        1,
        10,
        5,
        key="ease_importance"
    )

    if option_a and option_b:

        st.write("### Give each option a score")

        a1, b1 = st.columns(2)

        with a1:

            st.markdown(
                f"### 🅰️ {option_a}"
            )

            price_a = st.slider(
                "Price",
                1,
                10,
                5,
                key="price_a"
            )

            quality_a = st.slider(
                "Quality",
                1,
                10,
                5,
                key="quality_a"
            )

            ease_a = st.slider(
                "Ease",
                1,
                10,
                5,
                key="ease_a"
            )

        with b1:

            st.markdown(
                f"### 🅱️ {option_b}"
            )

            price_b = st.slider(
                "Price",
                1,
                10,
                5,
                key="price_b"
            )

            quality_b = st.slider(
                "Quality",
                1,
                10,
                5,
                key="quality_b"
            )

            ease_b = st.slider(
                "Ease",
                1,
                10,
                5,
                key="ease_b"
            )

        if st.button(
            "🧠 MAKE DECISION",
            key="make_decision"
        ):

            score_a = (
                price_a * importance_price
                +
                quality_a * importance_quality
                +
                ease_a * importance_ease
            )

            score_b = (
                price_b * importance_price
                +
                quality_b * importance_quality
                +
                ease_b * importance_ease
            )

            st.divider()

            if score_a > score_b:

                st.success(
                    f"🏆 LifeFix recommends: {option_a}"
                )

            elif score_b > score_a:

                st.success(
                    f"🏆 LifeFix recommends: {option_b}"
                )

            else:

                st.info(
                    "🤝 It's a tie! Both options scored equally."
                )

            c1, c2 = st.columns(2)

            c1.metric(
                option_a,
                score_a
            )

            c2.metric(
                option_b,
                score_b
            )


# ============================================================
# 📦 WHERE DID I PUT IT?
# ============================================================

elif tool == "📦 Where Did I Put It?":

    st.subheader("📦 Where Did I Put It?")

    st.write(
        "Stop searching your entire room for something you stored months ago."
    )

    if "inventory" not in st.session_state:

        st.session_state.inventory = []

    item_name = st.text_input(
        "What are you storing?",
        placeholder="Example: Arduino UNO",
        key="item_name"
    )

    location = st.text_input(
        "Where did you put it?",
        placeholder="Example: Blue box → Shelf 2",
        key="item_location"
    )

    item_notes = st.text_input(
        "Extra note",
        placeholder="Example: Inside small plastic bag",
        key="item_notes"
    )

    if st.button(
        "📦 SAVE LOCATION",
        key="save_item"
    ):

        if item_name and location:

            st.session_state.inventory.append(
                {
                    "item": item_name,
                    "location": location,
                    "notes": item_notes
                }
            )

            st.success(
                f"Saved location for {item_name}"
            )

        else:

            st.warning(
                "Enter both the item and location."
            )

    st.divider()

    search = st.text_input(
        "🔎 Search your stored items",
        key="inventory_search"
    )

    if st.session_state.inventory:

        for item in st.session_state.inventory:

            if (
                not search
                or search.lower()
                in item["item"].lower()
            ):

                st.markdown(
                    f"""
                    <div class="card">

                    <h3>📦 {item["item"]}</h3>

                    <p>
                    📍 <b>Location:</b>
                    {item["location"]}
                    </p>

                    <p>
                    📝 <b>Note:</b>
                    {item["notes"] or "No note"}
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info(
            "No items saved yet."
        )


# ============================================================
# 🔢 EVERYDAY CALCULATOR
# ============================================================

elif tool == "🔢 Everyday Calculator":

    st.subheader("🔢 Everyday Calculator")

    calculator = st.selectbox(
        "What do you want to calculate?",
        [
            "Percentage",
            "Discount",
            "Age",
            "Speed",
            "Time Needed"
        ],
        key="calculator_type"
    )

    if calculator == "Percentage":

        number = st.number_input(
            "Number",
            value=100.0,
            key="percentage_number"
        )

        percent = st.number_input(
            "Percentage",
            value=20.0,
            key="percentage_value"
        )

        if st.button(
            "Calculate",
            key="calc_percentage"
        ):

            result = number * percent / 100

            st.success(
                f"{percent}% of {number} = {result:.2f}"
            )

    elif calculator == "Discount":

        original = st.number_input(
            "Original price",
            min_value=0.0,
            value=100.0,
            key="discount_original"
        )

        discount = st.slider(
            "Discount %",
            0,
            100,
            20,
            key="discount_percent"
        )

        final = (
            original
            * (1 - discount / 100)
        )

        saved = original - final

        st.metric(
            "Final Price",
            f"{final:.2f}"
        )

        st.write(
            f"💰 You save {saved:.2f}"
        )

    elif calculator == "Age":

        birth_date = st.date_input(
            "Date of birth",
            value=date(2010, 1, 1),
            key="birth_date"
        )

        today = date.today()

        age = (
            today.year
            - birth_date.year
            - (
                (today.month, today.day)
                <
                (birth_date.month, birth_date.day)
            )
        )

        st.metric(
            "Your Age",
            f"{age} years"
        )

    elif calculator == "Speed":

        distance = st.number_input(
            "Distance",
            min_value=0.0,
            value=100.0,
            key="speed_distance"
        )

        time_taken = st.number_input(
            "Time",
            min_value=0.1,
            value=2.0,
            key="speed_time"
        )

        if st.button(
            "Calculate Speed",
            key="calc_speed"
        ):

            speed = distance / time_taken

            st.success(
                f"Speed = {speed:.2f} distance units/hour"
            )

    elif calculator == "Time Needed":

        work_amount = st.number_input(
            "Total work required (hours)",
            min_value=0.1,
            value=10.0,
            key="work_amount"
        )

        hours_per_day = st.number_input(
            "Hours available per day",
            min_value=0.1,
            value=2.0,
            key="hours_day"
        )

        days_needed = (
            work_amount / hours_per_day
        )

        st.metric(
            "Days Needed",
            f"{days_needed:.1f}"
        )


# ============================================================
# 💧 BREAK & WATER PLANNER
# ============================================================

elif tool == "💧 Break & Water Planner":

    st.subheader("💧 Break & Water Planner")

    st.write(
        "Plan your study/work session so you don't forget to take breaks."
    )

    session_hours = st.number_input(
        "How long will you work?",
        min_value=0.5,
        max_value=24.0,
        value=4.0,
        step=0.5,
        key="session_hours"
    )

    work_block = st.slider(
        "Work before a break (minutes)",
        20,
        120,
        50,
        key="work_block"
    )

    water_interval = st.slider(
        "Water reminder interval (minutes)",
        20,
        180,
        60,
        key="water_interval"
    )

    total_minutes = int(
        session_hours * 60
    )

    breaks = max(
        0,
        total_minutes // work_block
    )

    water_reminders = max(
        1,
        total_minutes // water_interval
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Work Time",
        f"{total_minutes} min"
    )

    c2.metric(
        "Suggested Breaks",
        breaks
    )

    c3.metric(
        "Water Reminders",
        water_reminders
    )

    if st.button(
        "🗓️ BUILD MY ROUTINE",
        key="build_routine"
    ):

        st.success(
            "Your routine is ready!"
        )

        elapsed = 0
        block_number = 1

        while elapsed < total_minutes:

            work_end = min(
                elapsed + work_block,
                total_minutes
            )

            st.write(
                f"### 🟢 Block {block_number}"
            )

            st.write(
                f"Work from minute "
                f"{elapsed} → {work_end}"
            )

            elapsed = work_end

            if elapsed < total_minutes:

                st.info(
                    "☕ Take a short break + 💧 drink water."
                )

            block_number += 1


# ============================================================
# 📊 LIFE FIX STATISTICS
# ============================================================

elif tool == "📊 LifeFix Statistics":

    st.subheader("📊 Your LifeFix Statistics")

    total_tasks = len(
        st.session_state.tasks
    )

    completed_tasks = sum(
        task["completed"]
        for task in st.session_state.tasks
    )

    total_hours = sum(
        task["hours"]
        for task in st.session_state.tasks
    )

    completed_hours = sum(
        task["hours"]
        for task in st.session_state.tasks
        if task["completed"]
    )

    if total_tasks:

        completion_rate = (
            completed_tasks
            / total_tasks
            * 100
        )

    else:

        completion_rate = 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📝 Total Tasks",
        total_tasks
    )

    c2.metric(
        "✅ Completed",
        completed_tasks
    )

    c3.metric(
        "⏱️ Total Hours",
        f"{total_hours:.1f}"
    )

    c4.metric(
        "📈 Completion",
        f"{completion_rate:.0f}%"
    )

    st.divider()

    if total_tasks:

        st.subheader("📈 Task Progress")

        st.progress(
            completion_rate / 100
        )

        st.write(
            f"You have completed "
            f"{completed_tasks} out of "
            f"{total_tasks} tasks."
        )

        if completion_rate == 100:

            st.balloons()

            st.success(
                "🏆 PERFECT! You completed everything!"
            )

        elif completion_rate >= 75:

            st.success(
                "🔥 Amazing progress!"
            )

        elif completion_rate >= 50:

            st.info(
                "💪 You're halfway there!"
            )

        else:

            st.warning(
                "🚀 Keep going!"
            )

    else:

        st.info(
            "Add tasks to see your statistics."
        )


# ============================================================
# 🏆 ACHIEVEMENTS
# ============================================================

st.divider()

st.header("🏆 LifeFix Achievements")

task_count = len(
    st.session_state.tasks
)

completed_count = sum(
    task["completed"]
    for task in st.session_state.tasks
)

achievements = [

    (
        "🌱 First Step",
        "Add your first task.",
        task_count >= 1
    ),

    (
        "📋 Organized",
        "Add 5 tasks.",
        task_count >= 5
    ),

    (
        "🔥 Getting Things Done",
        "Complete 3 tasks.",
        completed_count >= 3
    ),

    (
        "🏆 Productivity Master",
        "Complete 10 tasks.",
        completed_count >= 10
    ),

    (
        "⚡ LifeFixer",
        "Complete everything.",
        task_count > 0
        and completed_count == task_count
    )
]

achievement_columns = st.columns(
    len(achievements)
)

for i, achievement in enumerate(
    achievements
):

    title, description, unlocked = achievement

    with achievement_columns[i]:

        if unlocked:

            st.success(
                f"{title}\n\n{description}"
            )

        else:

            st.warning(
                f"🔒 {title}\n\n{description}"
            )


# ============================================================
# 💾 EXPORT DATA
# ============================================================

st.divider()

st.header("💾 Save Your LifeFix Data")

if st.session_state.tasks:

    export_text = "LIFEFIX TASK LIST\n"
    export_text += "=" * 30 + "\n\n"

    for task in st.session_state.tasks:

        status = (
            "COMPLETED"
            if task["completed"]
            else "NOT COMPLETED"
        )

        export_text += (
            f"Task: {task['name']}\n"
            f"Deadline: {task['deadline']}\n"
            f"Hours: {task['hours']}\n"
            f"Importance: {task['importance']}\n"
            f"Status: {status}\n"
            f"Priority Score: "
            f"{calculate_score(task)}\n"
            + "-" * 30
            + "\n"
        )

    st.download_button(
        label="📥 DOWNLOAD MY TASKS",
        data=export_text,
        file_name="lifefix_tasks.txt",
        mime="text/plain"
    )

else:

    st.info(
        "Add some tasks first to export your data."
    )


# ============================================================
# FINAL MESSAGE
# ============================================================

st.divider()

st.markdown("""
<div class="hero">

<h2>🧠 LifeFix Mission</h2>

<p style="font-size:20px;">

We started with one problem:
<br>
<strong>"I don't know what to do first."</strong>

<br><br>

Now LifeFix can help with planning,
decisions, packing, expenses, calculations,
organization and more.

<br><br>

⚡ <strong>Small Problems → Smart Solutions</strong>

</p>

</div>
""", unsafe_allow_html=True)


