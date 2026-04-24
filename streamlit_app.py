import streamlit as st
import pandas as pd
from datetime import datetime

from utils.data_loader import get_connection, load_silver_data, load_gold_data
from utils.prediction import load_model
from utils.features import build_input
from utils.visuals import (
    render_kpis,
    render_duration_chart,
    render_trends,
    render_top_videos
)

# --------------------
# CONFIG
# --------------------
st.set_page_config(
    page_title="MrBeast Analyzer",
    layout="wide",
    page_icon="🎬"
)

st.title("🎬 MrBeast Creative Performance Analyzer")
st.markdown("---")

# --------------------
# CONNECTION + DATA
# --------------------
conn = get_connection()

@st.cache_data(ttl=3600)
def load_data():
    df_silver = load_silver_data(conn)
    df_gold = load_gold_data(conn)
    return df_silver, df_gold

df_silver, df_gold = load_data()

# --------------------
# SAFETY CHECK
# --------------------
if df_silver.empty:
    st.error("No data loaded from Snowflake")
    st.stop()

# --------------------
# LOAD MODEL
# --------------------
model = load_model()

# --------------------
# SIDEBAR FILTERS
# --------------------
with st.sidebar:
    st.markdown("## Filters")

    min_date = df_silver["published_at"].min()
    max_date = df_silver["published_at"].max()

    date_range = st.date_input(
        "Date Range",
        value=[min_date.date(), max_date.date()]
    )

# --------------------
# FILTER DATA
# --------------------
filtered_silver = df_silver[
    (df_silver["published_at"].dt.date >= date_range[0]) &
    (df_silver["published_at"].dt.date <= date_range[1])
].copy()

if filtered_silver.empty:
    st.warning("No data for selected filters")
    st.stop()

# --------------------
# VISUALS (NEW LAYER)
# --------------------
render_kpis(filtered_silver)
render_duration_chart(filtered_silver)
render_trends(filtered_silver)
render_top_videos(filtered_silver)

# --------------------
# PREDICTOR UI
# --------------------
st.subheader("🔮 AI Performance Predictor")

col1, col2, col3 = st.columns(3)

with col1:
    pred_duration = st.slider("Duration (seconds)", 30, 1800, 480)
    pred_title = st.text_input("Video Title")

with col2:
    pred_money = st.checkbox("Contains $", True)
    pred_question = st.checkbox("Contains ?")
    pred_numbers = st.checkbox("Contains numbers")

with col3:
    pred_hour = st.selectbox("Publish Hour (UTC)", list(range(24)), index=17)
    pred_weekend = st.checkbox("Weekend")

# --------------------
# PREDICT BUTTON
# --------------------
if st.button("🚀 Predict Performance", use_container_width=True):

    try:
        input_data = build_input(
            pred_duration,
            pred_title,
            pred_money,
            pred_question,
            pred_numbers,
            pred_hour,
            pred_weekend,
            filtered_silver  # IMPORTANT: use filtered data
        )

        prediction = float(model.predict(input_data)[0])

        # Clamp unrealistic values
        prediction = max(0, min(prediction, 10))

        st.success(f"🎯 Predicted Engagement Rate: {prediction:.2f}%")

        avg = float(filtered_silver["engagement_rate_pct"].mean())
        best = float(filtered_silver["engagement_rate_pct"].max())

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "vs Channel Avg",
                f"{((prediction - avg) / avg * 100):+.1f}%"
            )

        with col2:
            st.metric(
                "vs Best Video",
                f"{((prediction - best) / best * 100):+.1f}%"
            )

        # --------------------
        # INSIGHT BOX (NEW)
        # --------------------
        st.markdown("### 💡 Insight")

        if prediction > avg:
            st.success("This video is predicted to outperform your channel average.")
        else:
            st.warning("This video may underperform compared to your average.")

    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")

# --------------------
# FOOTER
# --------------------
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")