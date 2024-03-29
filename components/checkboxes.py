import streamlit as st 
import pandas as pd

DEFAULT_FILE_PATH = "./data/all_stocks_5yr.csv"



def store_data_in_session(file):
    df = pd.read_csv(file)
    if 'df' not in st.session_state or st.session_state.df is None:
        st.session_state.df = df

def use_default_data_checkbox():
    use_default_data = st.checkbox('Use default data', value=True)

    if not use_default_data:
        if 'df' not in st.session_state:
            st.subheader("DF not loaded")
            st.write("Go to the File Upload tab to load your file")
            exit() 
        else:
            st.write("not using default data")
        

def use_default_data_or_upload_checkbox():
    use_default_data = st.checkbox('Use default data', value=True)

    if use_default_data:   
        store_data_in_session(DEFAULT_FILE_PATH)
    else:     
        st.session_state.df = None
        file = st.file_uploader("Choose a file")
        if file: 
            store_data_in_session(file)
            
            
            
            

           
        
    
