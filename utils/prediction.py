import joblib
import streamlit as st

@st.cache_resource
def load_model():
    return joblib.load("models/engagement_model.joblib.gz")