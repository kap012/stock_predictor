import streamlit as st
from pages.file_upload import get_uploaded_file
from components.menu import sidebar_menu
import pandas as pd

#st.set_page_config(page_title="Experiment", page_icon = ":chart_with_upwards_trend:", layout="wide")


sidebar_menu()

st.header("Compare two models")
