import streamlit as st
from components.menu import sidebar_menu
import pandas as pd
import time

st.set_page_config(page_title="Compare models", page_icon = ":chart_with_upwards_trend:", layout="wide")

sidebar_menu()

st.header("Compare models", divider = True)

use_default_data = st.checkbox('Use default data', value=True)

if use_default_data:
    df = pd.read_csv("./data/all_stocks_5yr.csv")
else:        
    if 'df' not in st.session_state:
        df = None
    else:
        df = st.session_state.df
    

if df is not None:
    st.caption("Dataframe loaded sucesfully")
    
    n_columns = st.select_slider(label = "Select the number of models to compare", options = (1, 2, 3, 4))

    st.subheader(f"Number of colums: {n_columns}")
    

    columns_list = st.columns(n_columns)
    models = [None] * len(columns_list)
    
    for index, column in enumerate(columns_list):
        column.subheader(f"Col number: {index + 1}")
        models[index] = column.selectbox(label="Select model", 
                         options=["ARIMA", "VAR", "RNN", "LSTM"], 
                         placeholder ="No model selected",
                         index=None,
                         key=index)
        
    if st.button(label="Train models", type="primary"):
        with st.spinner('Training the models...'):
            time.sleep(1)
            st.toast('Models trained succesfully!', icon="✅")
            for index, column in enumerate(columns_list):
                column.write(f"Model trained: {models[index]}")
            
else: 
    st.subheader("DF not loaded")
    st.write("Go to the File Upload tab to load your file")
    
    
   