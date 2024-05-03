import streamlit as st
from components.sidebar_menu import sidebar_menu
from src.app_logic.data_util import init_data 


st.set_page_config(page_title="Stock Predictor Website", page_icon = ":chart_with_upwards_trend:", layout="wide")


init_data()
sidebar_menu()

st.header("Stock Predictor Website", divider = True)

st.subheader("Pages: ")

st.markdown(
"""
- Main page
- See stocks
- Load data
- Compare models
"""
)