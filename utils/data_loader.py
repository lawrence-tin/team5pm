import pandas as pd
import snowflake.connector
import streamlit as st

@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
        role=st.secrets["snowflake"]["role"]
    )

def load_silver_data(conn):
    query = """
    SELECT * 
    FROM TEAM5PM_PROTOTYPE.SILVER.CANONICAL_PERFORMANCE
    """
    df = pd.read_sql(query, conn)
    df.columns = df.columns.str.lower()
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
    return df


def load_gold_data(conn):
    query = """
    SELECT * 
    FROM TEAM5PM_PROTOTYPE.GOLD.AI_TRAINING_DATASET
    """
    df = pd.read_sql(query, conn)
    df.columns = df.columns.str.lower()
    return df
