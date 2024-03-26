import streamlit as st
from components.menu import sidebar_menu


st.set_page_config(page_title="Stock Predictor Website", page_icon = ":chart_with_upwards_trend:", layout="wide")

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




