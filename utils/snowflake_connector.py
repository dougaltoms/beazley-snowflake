import pandas as pd
import streamlit as st
import snowflake.connector


# Set global variables
TIME_TO_LIVE = 600

@st.experimental_singleton
def init_connection():

    '''
    Initiate connection to SF account
    Run only once as experimental_singleton
    Returns snowflake connector object
    '''

    snowflake_connector = snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive = True
    )

    if 'snowflake_connector' not in st.session_state:
        st.session_state['snowflake_connector'] = snowflake_connector

    return snowflake_connector

snowflake_connector = init_connection()

@st.experimental_memo(ttl=TIME_TO_LIVE)
def run_query(query):
    with snowflake_connector.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

@st.experimental_memo(ttl=TIME_TO_LIVE)
def query_to_df(query):
    df = pd.read_sql(query, snowflake_connector)
    return df