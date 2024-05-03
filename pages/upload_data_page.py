import streamlit as st
from components.sidebar_menu import sidebar_menu
from io import StringIO
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from src.app_logic.data_util import init_data, load_default_data, set_date_as_idx, get_df_from_csv, columns_to_lowercase
from src.app_logic.session_state_util import store_in_session

st.set_page_config(page_title="Upload data", page_icon = ":chart_with_upwards_trend:", layout="wide")

init_data()
sidebar_menu()


st.header("Upload file", divider = True)

data_usage_placeholder = st.empty()
upload_data_col, reload_default_data_col = st.columns(2)

loaded_data = None
date_col_name = None
    
with upload_data_col:
    file = st.file_uploader("Choose a file", type='csv')
    if file: 
        data_usage_placeholder.caption("Using custom data")
        loaded_data = get_df_from_csv(file)
        
        
        
with reload_default_data_col:
    container = st.container(height=30, border=False)
    container.write("... or reload the default dataset:")
    
    if st.button('Reload default data', use_container_width=True):
        load_default_data()      
        loaded_data = st.session_state.df
        data_usage_placeholder.caption("Using default data")   

        
if loaded_data is None:
    st.write("Load data to proceed")
    st.stop()
    
    
date_col_name = st.selectbox(label='Select the date column',
                                help="Select the column storing the date string, it will be used as the new index of the dataframe",
                                options=loaded_data.columns,
                                index=None
                            )   

if st.button("Load the data",
                disabled= date_col_name is None,
                use_container_width=True
                ):

    try:
        loaded_data = set_date_as_idx(df=loaded_data, date_col_name=date_col_name)
        
        # rename to date if different name
        if date_col_name != 'Date':
            loaded_data = loaded_data.rename(columns={date_col_name: 'date'})
            
        
        loaded_data = columns_to_lowercase(loaded_data)
        
  
        
        store_in_session(var_name='df', data=loaded_data)
        
        st.toast("Stored succesfully")
        
    except Exception as e:
        st.warning("There was a problem, try selecting a different column.?!?")
        st.write(e)
        st.session_state.df = None



with st.expander("Dataframe"): 
    if  'df' in st.session_state and st.session_state.df is not None: 
        st.write(st.session_state.df.columns)
        st.dataframe(st.session_state.df)
    else:
        st.caption("Load the file to see the dataframe")
        

