import streamlit as st
from src.app_logic.session_state_util import init_processing_state, start_processing, stop_processing



def submit_button(process_id: str, text="Process", disabled = False):
  st.button(text, 
              on_click=lambda page_name: (start_processing(page_name), 
                                           st.toast("Processing started", icon="✅")),
              key=f"{process_id}_submit_btn",
              use_container_width=True,
              disabled=disabled,
              kwargs=dict(page_name=process_id))
  
  
  
def cancel_submit_button(process_id: str):
        if st.session_state[f"processing_{process_id}"]:
            st.button("Cancel",
                      on_click=lambda page_name: (stop_processing(page_name), 
                                                   st.toast("Processing cancelled", icon="❌")),
                      key=f"{process_id}_cancel_submit_btn",
                      use_container_width=True,
                      kwargs=dict(page_name=process_id))
