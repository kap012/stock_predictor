import streamlit as st
from components.menu import sidebar_menu
from io import StringIO
import numpy as np
import pandas as pd

st.set_page_config(page_title="File upload with checkbox", page_icon = ":chart_with_upwards_trend:", layout="wide")

sidebar_menu()

st.header("Upload file", divider = True)

def store_df_in_session(file):
    df = pd.read_csv(file)
    if 'df' not in st.session_state:
        st.session_state.df = df


use_default_data = st.checkbox('Use default data', value=True)

if use_default_data:
    df = pd.read_csv("./data/all_stocks_5yr.csv")
else:        
    file = st.file_uploader("Choose a file")
    df = store_df_in_session(file)


if df is not None: 
    #df = dataframe.set_index('date', inplace=True)
    
    selected = st.multiselect(
    "Select columns to display", 
    placeholder="No columns selected",
    options = df.columns.values)

    if selected:
        st.dataframe(df[selected])
    


     

