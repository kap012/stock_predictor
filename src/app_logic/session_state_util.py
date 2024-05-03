import streamlit as st

    
# init the variable in session state

def init_processing_state(process_id: str):
    key = f"processing_{process_id}" 
    
    if key not in st.session_state:
        st.session_state[key] = False          

def stop_processing(page_name: str):
    st.session_state[f"processing_{page_name}"] = False

def start_processing(page_name: str):
    st.session_state[f"processing_{page_name}"] = True
    

def store_in_session(var_name: str, data):
    st.session_state[var_name] = data
    