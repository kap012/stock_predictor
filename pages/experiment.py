import streamlit as st
from components.menu import sidebar_menu
import pandas as pd
from pages.file_upload import load_data

#st.set_page_config(page_title="Experiment", page_icon = ":chart_with_upwards_trend:", layout="wide")


sidebar_menu()

st.header("Caching experiment")

df = st.session_state.df

if df is not None:
    st.write(df)
else: 
    st.write("DF not loaded")