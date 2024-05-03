import streamlit as st
import pandas as pd 
    
def data_between_dates_form(data: pd.DataFrame, process_id: str):
    st.subheader("Select time period:")
    
    start_date_col, end_date_col = st.columns(2)
    
    earliest_date = data.index[0]
    latest_date = data.index[-1]


    with start_date_col:
        start_date = st.date_input(label="Select start date", 
                                            help="Start date help",
                                            key = f"{process_id}_start_date",
                                            min_value = earliest_date, 
                                            max_value = latest_date,
                                            value = earliest_date
                                            )

    with end_date_col:
        end_date = st.date_input(label="Select end date",
                                        help="End date help",
                                        key = f"{process_id}_end_date",
                                        min_value = earliest_date,
                                        max_value = latest_date,
                                        value = latest_date,
                                    ) 
    
    data_between_dates =  data[start_date:end_date]

    return  data_between_dates
