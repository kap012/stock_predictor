
from components.sidebar_menu import sidebar_menu
import streamlit as st
from src.app_logic.data_util import init_data, get_comparison_df
import pandas as pd
from statsmodels.tools.eval_measures import rmse        
from sklearn.metrics import mean_absolute_percentage_error 
import plotly.graph_objects as go
from src.calculations.train_test_split import get_test_subset, get_train_subset
from src.models.persistence_forecast import run_persistence_forecast
from components.forms.selectboxes import select_column
from components.buttons.submit_button import submit_button, cancel_submit_button
from src.app_logic.session_state_util import init_processing_state, stop_processing
from components.forms.date_forms import data_between_dates_form
from components.expanders.model_page_expanders import dataframes_expander, graph_expander, errors_expander



st.set_page_config(page_title="Persistence forcast",
                   page_icon=":chart_with_upwards_trend:", layout="wide")

st.header("Persistence forcast")

process_id = "pers_forecast"
init_data()
init_processing_state(process_id)
sidebar_menu()

df = st.session_state.df

info_tab, model_tab = st.tabs(["Info", "Run the model"])


with info_tab:
    st.subheader("Persitence forecast info")
    
with model_tab:        
    prediction_series = None    
    
    data_between_dates = data_between_dates_form(df, process_id)
    
    selected_column = select_column(df, proces_id=process_id)
    
    cols = st.columns(2)
    shift = cols[0].number_input('Data shift', help="Shift help", min_value=1, max_value=10, value = 1)
    split = cols[1].number_input('Train/Test split',help="Train/Test split help", min_value=0.0, max_value=1.0, step=0.01, value = 0.66)


    submit_button(process_id=process_id)
    cancel_submit_button(process_id=process_id)

    if selected_column is None:
        st.caption("Select the column to see the results")
        st.stop()
    
    if st.session_state[f"processing_{process_id}"]:        
        prediction_series = run_persistence_forecast(data=data_between_dates[selected_column], split=split, shift=shift)
    
    
    if prediction_series is None:
        st.caption('Press the button to see the results')
     


    if prediction_series is not None:
        # DATAFRAMES
        test_set = get_test_subset(data_between_dates[selected_column], split=split)
        comparison_df = get_comparison_df(test_set=test_set, forecast=prediction_series)
        dataframes_expander(comparison_df)
    

            

        # GRAPHING
        with st.expander("Graphs", expanded=False):
            st.caption(f"Note that the {shift} value(s) at the start of the prediction isn't there as in the test set there's no previous data in the test set")
            layout = go.Layout(
                    # paper_bgcolor='rgba(164, 172, 231, 0.8)',
                    # plot_bgcolor='rgba(0,0,0,0)'
                )
            res_fig = go.Figure(layout=layout)
            
            test_fig = go.Figure(layout=layout)
            
            test_fig.add_trace(go.Scatter(x=data_between_dates.index,
                                        y=data_between_dates[selected_column].values,
                                    
                                        mode='lines',
                                        name='Actual'))
            
            test_fig.add_trace(go.Scatter(x=prediction_series.index    ,
                                    y=prediction_series.values,
                                    line_color="red",
                                    mode='lines',
                                    name='Prediction'))
            
            st.plotly_chart(test_fig, use_container_width=True)



        errors_expander(test_set, prediction_series)

            