import streamlit as st
from src.models.arima import run_arima
from src.app_logic.session_state_util import init_processing_state, stop_processing
from src.app_logic.data_util import init_data, get_comparison_df
from src.models.arima import run_arima 
from src.calculations.train_test_split import get_test_subset
from components.sidebar_menu import sidebar_menu
from components.expanders.model_page_expanders import dataframes_expander, graph_expander, errors_expander
from components.forms.date_forms import data_between_dates_form
from components.forms.selectboxes import select_column
from components.buttons.submit_button import submit_button, cancel_submit_button
        

st.set_page_config(page_title="ARIMA", page_icon = ":chart_with_upwards_trend:", layout="wide")

page_name = "ARIMA"
st.header("ARIMA model")
init_data()
sidebar_menu()

info_tab, model_tab = st.tabs(["Info", "Run the model"])

with info_tab:
    st.subheader("Details about the ARIMA model")
    

with model_tab:
    init_processing_state(page_name)
    df = st.session_state.df
    data_between_dates = data_between_dates_form(data=df, process_id=page_name)
    
    cols = st.columns(4)
    lag_order = cols[0].number_input('Lag order', help="Lag order help", min_value=0, max_value=10, value = 1)
    diff_degree = cols[1].number_input('Degree of differencing', help="Degree of differencing help",  min_value=0, max_value=10, value = 1)
    ma_window = cols[2].number_input('Moving average window', help="Moving average window help", min_value=0, max_value=10, value = 1)
    split = cols[3].number_input('Train/Test split',help="Train/Test split help", min_value=0.0, max_value=1.0, step=0.01, value = 0.66)
    
    selected_column = select_column(df, page_name)
    


    key = str(lag_order) + str(diff_degree) + str(ma_window) + str(split) + str(data_between_dates.index[0]) + str(data_between_dates.index[-1])

    # init the session storage
    if 'processed' not in st.session_state:
        st.session_state.processed = {}
    
    submit_button(page_name, disabled= selected_column is None)
    cancel_submit_button(page_name)
            
    if st.session_state[f"processing_{page_name}"]:    
        if key not in st.session_state.processed:    
                with st.spinner('Training the model...'):
                    result = run_arima(data_between_dates[selected_column],
                                    split,
                                    lag_order,
                                    diff_degree,
                                    ma_window)
                    st.toast('Model trained successfully!', icon="✅")
                    st.session_state.processed[key] = result
                    stop_processing(page_name=page_name)
            
    if selected_column is None:
        st.caption("The column is not selected")
    elif key not in st.session_state.processed:
        st.caption("Train the model to see the results")
        st.stop()
    else:
        forecast_series = st.session_state.processed[key]
        
        test_set = get_test_subset(data_between_dates[selected_column], split=split)
        
        comparison_df = get_comparison_df(test_set=test_set, forecast=forecast_series)
        
        dataframes_expander(data=comparison_df)
        graph_expander(actual= data_between_dates[selected_column], forecast=forecast_series)
        errors_expander(test_set=test_set, prediction=forecast_series)





    



            
   