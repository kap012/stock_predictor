import streamlit as st
from components.menu import sidebar_menu
from io import StringIO
import numpy as np
import pandas as pd

st.set_page_config(page_title="File upload with checkbox", page_icon = ":chart_with_upwards_trend:", layout="wide")

sidebar_menu()

file = st.file_uploader("Choose a file")


if file is not None:
    
    df = pd.read_csv(file)
    if 'df' not in st.session_state:
        st.session_state.df = df


if file is not None: 
    
    df = st.session_state.df
    st.write(df)
    # dataframe = load_data()
    
    # df = dataframe.set_index('date', inplace=True)


    # st.header(f"INDEX: \n {dataframe.index}")

    # st.header("DATAFRAME: ")
    # st.write(dataframe)
    
    # selected = st.multiselect(
    # "Select columns", 
    # dataframe.columns.values)

    # if selected:
    #     st.dataframe(dataframe[selected])
    
else:
    st.write("DF not loaded")    


     

