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
    
    # Select time
    # TODO read the time limits from the data
    
    st.subheader("Select time perioid", divider=True)
    start_date_col, end_date_col = st.columns(2)
    
    start_date = start_date_col.date_input(label="Select start date")
    
    end_date = end_date_col.date_input(label="Select end date")    
    
    
    # Columns
    st.subheader("Select models", divider=True)
    n_columns = st.select_slider(label = "Select the number of models to compare", options = (1, 2, 3, 4))    
    columns_list = st.columns(n_columns)
    models = [None] * len(columns_list)
    
    for index, column in enumerate(columns_list):
        column.subheader(f"Model {index + 1}")
        models[index] = column.selectbox(label="Select model", 
                         options=["ARIMA", "VAR", "RNN", "LSTM"], 
                         placeholder ="No model selected",
                         index=None,
                         key=index)
        
    # Train models button     
    if st.button(label="Train models", type="secondary", use_container_width=True):
        with st.spinner('Training the models...'):
            time.sleep(1)
            st.toast('Models trained succesfully!', icon="✅")
            for index, column in enumerate(columns_list):
                column.divider()
                column.write(f"Model trained: {models[index]}")
            
else: 
    st.subheader("DF not loaded")
    st.write("Go to the File Upload tab to load your file")
    
    
   