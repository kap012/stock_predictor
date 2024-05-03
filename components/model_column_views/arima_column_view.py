import streamlit as st

def arima_column_view(dict_name, column_number):
    data_dict = st.session_state[dict_name]

    data_dict['lag_order'] = st.number_input('Lag order',
                                             help="Lag order help",
                                             key=f"col_view_lag_{column_number}", 
                                             min_value=0, 
                                             max_value=10, 
                                             value = 1)
    
    data_dict['diff_degree'] = st.number_input('Degree of differencing', 
                                               help="Degree of differencing help", 
                                               key=f"col_view_diff_{column_number}" , 
                                               min_value=0,
                                               max_value=10, 
                                               value = 1)
    
    data_dict['ma_window']= st.number_input('Moving average window',
                                            help="Moving average window help", 
                                            key=f"col_view_ma_{column_number}" ,
                                            min_value=0, 
                                            max_value=10, 
                                            value = 1)

    #key = "col" + str(st.session_state.lag_order) + str(st.session_state.diff_degree) + str(st.session_state.ma_window) + str(st.session_state.split) + str(start_date) + str(end_date)
    
    