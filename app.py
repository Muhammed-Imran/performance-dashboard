import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

ACCESS_KEY = os.getenv("ACCESS_KEY", "")
qk = st.query_params.get("k")
if ACCESS_KEY:
    if "ok" not in st.session_state:
        st.session_state.ok = (qk == ACCESS_KEY)
    if st.session_state.ok is False:
        st.write("Unauthorized. Append ?k=YOUR_KEY once to the URL.")
        st.stop()

st.set_page_config(page_title="Feedback Dashboard", layout="wide")
st.markdown("<style>div.block-container{padding-top:1rem;padding-bottom:1rem;max-width:1200px}</style>", unsafe_allow_html=True)

team_performance = pd.DataFrame({
    "name": ["Productivity","Knowledge","Collaboration","Innovation","Professionalism","Discipline","Learning"],
    "score": [8.7,7.9,7.3,7.3,8.3,7.6,8.0]
})

ind = pd.DataFrame({
    "name": ["Productivity","Knowledge","Collaboration","Innovation","Professionalism","Discipline","Learning"],
    "Imran": [8.5,7.9,7.2,7.8,8.6,7.9,8.3],
    "Hamza":   [8.0,7.5,8.5,6.9,8.1,7.4,7.8],
    "Haseeb": [7.8,8.1,6.8,7.2,8.3,7.5,8.1],
})

trend = pd.DataFrame({
    "month": ["Apr","May","Jun","Jul","Aug"],
    "Imran": [7.1,8.9,8.0,8.7,9.5],
    "Hamza":   [8.1,7.9,7.3,6.7,6.6],
    "Haseeb": [7.8,8.1,8.9,9.2,9.6],
})

bonus = pd.DataFrame({"name":["Imran","Hamza","Haseeb"], "value":[35,25,40]})

heatmap = pd.DataFrame([
    {"member":"Imran","Productivity":9,"Knowledge":8,"Collaboration":7,"Innovation":8,"Discipline":9},
    {"member":"Hamza","Productivity":8,"Knowledge":7,"Collaboration":9,"Innovation":6,"Discipline":8},
    {"member":"Haseeb","Productivity":8,"Knowledge":8,"Collaboration":6,"Innovation":7,"Discipline":7},
])

st.title("Team Dashboard")

left, right = st.columns([2.1, 1.0])
with left:
    st.subheader("Team Performance")
    view = st.radio("View", options=["Team","Individual","Compare"], index=0, key="perf_view", horizontal=True)
    h = 260
    if view == "Team":
        fig = px.bar(team_performance, x="name", y="score", range_y=[0,10], labels={"name":"","score":""})
        fig.update_traces(marker_line_width=0, hovertemplate="%{x}: %{y}")
        fig.update_layout(height=h, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)
    elif view == "Individual":
        long = ind.melt(id_vars="name", var_name="member", value_name="score")
        fig = px.bar(long, x="name", y="score", color="member", barmode="group", range_y=[0,10], labels={"name":"","score":""})
        fig.update_layout(height=h, margin=dict(l=10,r=10,t=10,b=10), legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)
    else:
        avg = ind.set_index("name").mean(axis=1).round(1)
        long = ind.melt(id_vars="name", var_name="member", value_name="score")
        fig = px.bar(long, x="name", y="score", color="member", barmode="group", range_y=[0,10], labels={"name":"","score":""})
        fig.add_scatter(x=avg.index, y=avg.values, mode="lines", name="TeamAvg", line=dict(width=3))
        fig.update_layout(height=h, margin=dict(l=10,r=10,t=10,b=10), legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Bonus Allocation")
    pie = px.pie(bonus, names="name", values="value", hole=0.25)
    pie.update_traces(textinfo="percent+label", hovertemplate="%{label}: %{value}%")
    pie.update_layout(height=260, margin=dict(l=10,r=10,t=10,b=10), legend_title_text="")
    st.plotly_chart(pie, use_container_width=True)

left2, right2 = st.columns(2)
with left2:
    st.subheader("Performance Trends")
    long_t = trend.melt(id_vars="month", var_name="member", value_name="score")
    line = px.line(long_t, x="month", y="score", color="member", range_y=[0,10], markers=True)
    line.update_layout(height=240, margin=dict(l=10,r=10,t=10,b=10), legend_title_text="")
    st.plotly_chart(line, use_container_width=True)
with right2:
    st.subheader("Team Heatmap")
    hm_long = heatmap.melt(id_vars="member", var_name="category", value_name="score")
    heat = px.density_heatmap(hm_long, x="category", y="member", z="score", color_continuous_scale="RdYlGn")
    heat.update_layout(height=240, margin=dict(l=10,r=10,t=10,b=10), coloraxis_colorbar=dict(title=""))
    st.plotly_chart(heat, use_container_width=True)

st.subheader("Member Feedback")
tabs = st.tabs(["Imran", "Hamza", "Haseeb"])
for tab, who, pct, strengths, improve in [
    (tabs[0], "Imran", 90, "Delivers on time with high code quality.", "Increase knowledge sharing."),
    (tabs[1], "Hamza",   82, "Excellent collaboration and problem solving.", "Improve documentation quality."),
    (tabs[2], "Haseeb", 84, "Innovative model optimizations.", "More consistent reporting."),
]:
    with tab:
        st.markdown(f"**Strengths:** {strengths}")
        st.markdown(f"**Improvement:** {improve}")
        st.progress(pct/100)

st.caption("Developed by AI Team.")