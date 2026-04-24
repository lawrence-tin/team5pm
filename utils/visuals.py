# utils/visuals.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# -------------------------------
# KPIs
# -------------------------------
def render_kpis(df):
    st.subheader("📊 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Videos", len(df))
    col2.metric("Avg Engagement", f"{df['engagement_rate_pct'].mean():.2f}%")
    col3.metric("Total Views", f"{df['raw_views'].sum():,.0f}")
    col4.metric("Best Engagement", f"{df['engagement_rate_pct'].max():.2f}%")

    st.markdown("---")


# -------------------------------
# DURATION CHART
# -------------------------------
def render_duration_chart(df):
    st.subheader("⏱️ Duration Performance")

    df = df.copy()  # avoid mutation issues

    df["duration_bucket"] = pd.cut(
        df["duration_seconds"],
        bins=[0, 300, 600, 900, 1200, 1800, 9999],
        labels=["<5", "5-10", "10-15", "15-20", "20-30", "30+"]
    )

    duration_perf = df.groupby("duration_bucket")["engagement_rate_pct"].mean()

    fig = go.Figure([
        go.Bar(
            x=duration_perf.index.astype(str),
            y=duration_perf.values
        )
    ])

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")


# -------------------------------
# TIME SERIES
# -------------------------------
def render_trends(df):
    st.subheader("📈 Trends")

    df = df.copy()

    df["month"] = df["published_at"].dt.to_period("M")

    trend = df.groupby("month").agg({
        "engagement_rate_pct": "mean",
        "raw_views": "mean"
    }).reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend["month"].astype(str),
        y=trend["engagement_rate_pct"],
        name="Engagement"
    ))

    fig.add_trace(go.Scatter(
        x=trend["month"].astype(str),
        y=trend["raw_views"] / 1e6,
        name="Views (M)",
        yaxis="y2"
    ))

    fig.update_layout(
        yaxis2=dict(overlaying="y", side="right")
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")


# -------------------------------
# TOP VIDEOS
# -------------------------------
def render_top_videos(df):
    st.subheader("🏆 Top Videos")

    top_videos = df.nlargest(10, "engagement_rate_pct")[
        ["video_title", "engagement_rate_pct", "raw_views"]
    ]

    st.dataframe(top_videos, use_container_width=True)

    st.markdown("---")