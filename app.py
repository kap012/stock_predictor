import streamlit as st
from components.menu import sidebar_menu


st.set_page_config(page_title="Stock Predictor Website", page_icon = ":chart_with_upwards_trend:", layout="wide")

sidebar_menu()

st.subheader("Stock Predictor Website")

st.write("[Link](google.com)")

with st.echo(code_location="above"):
    st.write("Check")




