import streamlit as st
from components.sidebar_menu import sidebar_menu
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import pandas as pd
from src.models.exponential_smoothing import run_exponential_smoothing
from components.forms.date_forms import data_between_dates_form
from src.app_logic.session_state_util import init_processing_state, start_processing, stop_processing
from components.buttons.submit_button import submit_button, cancel_submit_button
from src.app_logic.data_util import init_data
from components.expanders.model_page_expanders import dataframes_expander, graph_expander, errors_expander
from src.calculations.train_test_split import get_test_subset, get_train_subset
from src.app_logic.data_util import get_comparison_df
from components.forms.selectboxes import select_column



page_name = "Exponential smoothing"
st.set_page_config(page_title="Exponential Smoothing", page_icon = ":chart_with_upwards_trend:", layout="wide")

init_processing_state(page_name)
init_data()


st.header(page_name)
sidebar_menu()


info_tab, model_tab = st.tabs(["Info", "Model"])


with info_tab:
    pass

with model_tab:
    df = st.session_state.df
    
    data_between_dates = data_between_dates_form(data=df, process_id=page_name)

    input_cols = st.columns(2)    
    smoothing_level = input_cols[0] .number_input('Smoothiing level',
                                            help="The alpha parameter of the model",
                                            min_value=0.0, 
                                            step = 0.01,
                                            max_value=10.0, 
                                            value = 0.10)
    
    split = input_cols[1].number_input('Train/Test split',
                                       help="Train/Test split help",
                                       min_value=0.0,
                                       max_value=1.0,
                                       step=0.01,
                                       value = 0.66)

    selected_column = select_column(df, page_name)

    

    submit_button(page_name)
    cancel_submit_button(page_name)
    
    
    prediction_series = None

    if st.session_state[f"processing_{page_name}"]:    
                with st.spinner('Training the model...'):
                    prediction_series = run_exponential_smoothing(data_between_dates[selected_column], split, smoothing_level)
                    st.toast('Model trained successfully!', icon="✅")
                    stop_processing(page_name=page_name)

    
    if prediction_series is None:
        st.caption("Press the button to see the results")
    else:    
        test_set = get_test_subset(data_between_dates[selected_column], split)
        
        comparison_df = get_comparison_df(test_set=test_set, forecast=prediction_series)

        dataframes_expander(comparison_df)
        graph_expander(actual=data_between_dates[selected_column], forecast=prediction_series)
        errors_expander(test_set, prediction_series)
        
    
    
        
        
        
    