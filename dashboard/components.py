# dashboard/components.py
from pathlib import Path
import pandas as pd
import streamlit as st
from PIL import Image

def kpi_row(d):
    baseline = d.get("baseline_avg_travel_time") or 1e-9
    delta = (1 - d["avg_travel_time"]/baseline) * 100
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg travel time (s)", f"{d['avg_travel_time']:.1f}", f"{delta:.1f}% vs baseline")
    c2.metric("Avg wait time (s)", f"{d['avg_wait_time']:.1f}")
    c3.metric("Vehicles", d["vehicles_in_system"])

def intersection_panel(d):
    ints = list(d["intersections"].keys())
    picked = st.selectbox("Intersection", ints, index=ints.index(d.get("selected_intersection", ints[0])))
    node = d["intersections"][picked]
    st.write(f"**Current phase:** {node['current_phase']}")
    df = pd.DataFrame({"lane": range(len(node["queues"])), "waiting": node["queues"]}).set_index("lane")
    st.bar_chart(df)

def time_series_panel(d):
    ts = d.get("time_series", {})
    if ts and ts.get("t"):
        df = pd.DataFrame({
            "t": ts["t"],
            "RL avg travel": ts["rl_avg_travel_time"],
            "Baseline": ts["baseline_avg_travel_time"],
        }).set_index("t")
        st.line_chart(df)
    else:
        st.info("No time-series yet.")

def video_panel(d):
    p = d.get("latest_frame_path")
    if p and Path(p).exists():
        st.image(Image.open(p), caption="Live frame", use_column_width=True)
    else:
        st.info("No frame available yet.")
