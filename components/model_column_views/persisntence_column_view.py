import streamlit as st


def persistence_column_view(dict_name, col_idx):
    data_dict = st.session_state[dict_name]

    data_dict['shift'] = st.number_input('Data shift',
                                         help="Shift help",
                                         key=f"shift_col_{col_idx}",
                                         min_value=1,
                                         max_value=10,
                                         value = 1)
 