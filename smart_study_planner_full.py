import streamlit as st
import pandas as pd
import numpy as np
import pytz
from datetime import datetime, timedelta, time
from ics import Calendar
import plotly.figure_factory as ff
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(layout="wide", page_title="Smart Study Planner (No Overlap Mode)")

# -------------------------------------------------
# STEP 1 — Completion Time Prediction (fast)
# -------------------------------------------------
st.title("⚡ Step 1: Quick Study Time Estimator")

col1, col2, col3 = st.columns(3)
with col1:
    mark = st.slider("Student Mark (%)", 40, 100, 75)
with col2:
    interactions = st.slider("Interaction Count", 0, 200, 50)
with col3:
    watch_time = st.slider("Video Watching Time (minutes)", 0, 600, 300)

# Train a dummy regressor (fast, local)
df_train = pd.DataFrame({
    "MARK": np.linspace(40, 100, 20),
    "TOTAL_MINUTES_DELIVERED": np.linspace(0, 600, 20),
    "INTERACTION_COUNT": np.linspace(0, 200, 20)
})
df_train["HOURS"] = 10 - (df_train["MARK"] - 40) / 15 + df_train["TOTAL_MINUTES_DELIVERED"]/300 + df_train["INTERACTION_COUNT"]/200
reg = RandomForestRegressor(random_state=42)
reg.fit(df_train[["MARK", "TOTAL_MINUTES_DELIVERED", "INTERACTION_COUNT"]], df_train["HOURS"])

X_pred = pd.DataFrame([[mark, watch_time, interactions]],
                      columns=["MARK", "TOTAL_MINUTES_DELIVERED", "INTERACTION_COUNT"])
pred_time = max(1, round(reg.predict(X_pred)[0], 1))
st.success(f"🧠 Estimated Completion Time: **{pred_time} hours**")
st.session_state["predicted_hours"] = pred_time

st.markdown("---")
st.title("🧩 Step 2: Study Planner & Visualization (No Overlap)")

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def parse_ics_bytes(ics_bytes, start_date, end_date):
    cal = Calendar(ics_bytes.decode("utf-8"))
    events = []
    for ev in cal.events:
        s, e = ev.begin.datetime, ev.end.datetime
        if s.tzinfo is None: s = pytz.UTC.localize(s)
        else: s = s.astimezone(pytz.UTC)
        if e.tzinfo is None: e = pytz.UTC.localize(e)
        else: e = e.astimezone(pytz.UTC)
        if s.date() < start_date or s.date() > end_date:
            continue
        events.append((s, e, ev.name or "Event"))
    events.sort(key=lambda x: x[0])
    return events

def compute_free_slots(events, start_date, end_date):
    free = []
    day = start_date
    while day <= end_date:
        day_start = datetime.combine(day, time(8, 0)).replace(tzinfo=pytz.UTC)
        day_end = datetime.combine(day, time(23, 0)).replace(tzinfo=pytz.UTC)
        busy = [(s, e) for (s, e, _) in events if s.date() == day]
        busy.sort()
        cur = day_start
        for s, e in busy:
            if s > cur:
                free.append((cur, min(s, day_end)))
            cur = max(cur, e)
        if cur < day_end:
            free.append((cur, day_end))
        day += timedelta(days=1)
    return free

def allocate_no_overlap(free_slots, hours, ddl):
    """Greedy allocation: fill earliest available slots before ddl, update free_slots dynamically"""
    allocated, remain = [], hours
    i = 0
    while i < len(free_slots) and remain > 0:
        s, e = free_slots[i]
        if s >= ddl:
            break
        dur = (min(e, ddl) - s).total_seconds()/3600
        if dur <= 0.25:
            i += 1
            continue
        use = min(remain, dur)
        start, end = s, s + timedelta(hours=use)
        allocated.append((start, end))
        remain -= use
        if use < dur:
            free_slots[i] = (end, e)
        else:
            free_slots.pop(i)
    return allocated, remain, free_slots

# -------------------------------------------------
# UI SECTION
# -------------------------------------------------
colA, colB = st.columns([1, 2])

with colA:
    st.header("📅 Calendar & Assignments")
    start_date = st.date_input("Start Date", pd.to_datetime("today").date())
    end_date = st.date_input("End Date", (pd.to_datetime("today")+timedelta(days=6)).date())
    ics = st.file_uploader("Upload Outlook .ics File", type=["ics"])

    if "assignments" not in st.session_state:
        st.session_state.assignments = []

    st.markdown("### ➕ Add Assignment")
    with st.form("add_assign"):
        name = st.text_input("Assignment Name")
        ddl_date = st.date_input("Deadline Date", pd.to_datetime("today")+timedelta(days=3))
        ddl_time = st.time_input("Deadline Time (UTC)", time(23, 59))
        hrs = st.number_input("Estimated Hours", 0.0, 100.0, st.session_state["predicted_hours"], 0.5)
        submit = st.form_submit_button("Add")
        if submit:
            st.session_state.assignments.append({
                "name": name or f"Assignment {len(st.session_state.assignments)+1}",
                "deadline": datetime.combine(ddl_date, ddl_time).replace(tzinfo=pytz.UTC),
                "hours": hrs
            })
            st.success(f"Added {name or 'Assignment'} ✅")

    st.markdown("### Current Assignments")
    for i, a in enumerate(st.session_state.assignments):
        st.write(f"{i+1}. {a['name']} — {a['deadline']} — {a['hours']}h")
        if st.button(f"Remove {i+1}", key=f"rm{i}"):
            st.session_state.assignments.pop(i)
            st.experimental_rerun()

with colB:
    st.header("📊 Optimized Planner & Urgency")

    if ics:
        events = parse_ics_bytes(ics.read(), start_date, end_date)
        free = compute_free_slots(events, start_date, end_date)
        results = []

        # Sort assignments by earliest deadline
        for a in sorted(st.session_state.assignments, key=lambda x: x["deadline"]):
            allocs, rem, free = allocate_no_overlap(free, a["hours"], a["deadline"])
            days_left = (a["deadline"] - datetime.now(pytz.UTC)).days
            urgency = "green" if days_left > 5 else "orange" if days_left > 2 else "red"
            results.append({**a, "allocs": allocs, "remain": rem, "urgency": urgency, "done": [False]*len(allocs)})

        # Display each course with progress
        for r in results:
            st.subheader(f"📘 {r['name']} — DDL: {r['deadline'].strftime('%a %Y-%m-%d %H:%M')} UTC")
            st.markdown(f"- Required: **{r['hours']}h**, Remaining unscheduled: **{r['remain']:.1f}h**")
            for j, (s, e) in enumerate(r["allocs"]):
                r["done"][j] = st.checkbox(
                    f"✅ {s.strftime('%a %H:%M')} → {e.strftime('%H:%M')} UTC",
                    value=r["done"][j], key=f"{r['name']}_{j}")
            progress = sum(r["done"])/len(r["done"]) if r["allocs"] else 0
            st.progress(progress)
            st.caption(f"Progress: {progress*100:.0f}% — Urgency: {r['urgency'].upper()}")
            latest_start = r["deadline"] - timedelta(hours=r["hours"])
            st.info(f"⏰ Start by **{latest_start.strftime('%a %H:%M')} UTC** to finish before the deadline!")

        # Timeline Visualization
        tl = []
        for s, e, _ in events:
            tl.append(dict(Task="Busy", Start=s, Finish=e, Resource="Busy"))
        for r in results:
            for s, e in r["allocs"]:
                tl.append(dict(Task=r["name"], Start=s, Finish=e, Resource=r["urgency"]))

        if tl:
            fig = ff.create_gantt(
                tl, index_col="Resource", show_colorbar=False, group_tasks=True,
                title="📆 Optimized Schedule (No Overlap)"
            )
            for r in results:
                fig.add_vline(x=r["deadline"], line_width=2, line_dash="dot", line_color=r["urgency"])
            st.plotly_chart(fig, use_container_width=True)

        # -------------------------------------------------
        # 📈 FINAL FREE TIME SUMMARY (bottom of page)
        # -------------------------------------------------
        st.markdown("---")
        st.header("📊 Free Time Summary")

        # Aggregate free hours per day
        free_summary = {}
        for s, e in free:
            day = s.strftime("%a")
            dur = (e - s).total_seconds() / 3600
            free_summary[day] = free_summary.get(day, 0) + dur

        weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        df_free = pd.DataFrame({
            "Day": weekday_order,
            "Free Hours": [free_summary.get(d, 0) for d in weekday_order]
        })

        # Display daily summary table
        st.subheader("🗓️ Daily Free Hours Overview")
        st.dataframe(df_free, use_container_width=True)

        # Plot line chart (smooth trend)
        fig2 = px.line(
            df_free,
            x="Day",
            y="Free Hours",
            markers=True,
            title="Free Time Availability Trend",
            line_shape="spline"
        )
        fig2.update_layout(
            yaxis_title="Free Hours",
            xaxis_title=None,
            showlegend=False,
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("Upload a .ics file to compute your available time.")
