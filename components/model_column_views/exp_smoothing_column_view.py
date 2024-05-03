import streamlit as st

def exp_smoothing_column_view(dict_name, column_number):
    data_dict = st.session_state[dict_name]

    data_dict['smoothing_level'] = st.number_input('Smoothin level',
                                             help="Smoothin level help",
                                             key=f"col_view_smoothing_{column_number}", 
                                             min_value=0, 
                                             max_value=10, 
                                             value = 1)