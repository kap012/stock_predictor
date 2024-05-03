import streamlit as st
from components.sidebar_menu import sidebar_menu
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.app_logic.data_util import init_data
from statsmodels.tsa.seasonal import seasonal_decompose
from components.buttons.submit_button import submit_button, cancel_submit_button
from src.app_logic.session_state_util import init_processing_state, stop_processing
from components.forms.date_forms import data_between_dates_form
from components.forms.selectboxes import select_column
import numpy as np



st.set_page_config(page_title="Decompose timeseries",
                   page_icon=":chart_with_upwards_trend:", layout="wide")

st.header("Decompose timeseries")
placeholder = st.empty()

sidebar_menu()
init_data()

df = st.session_state.df


def decompose_tab_content(decompose_tab_type: str):
    init_processing_state(decompose_tab_type)
    
    decomposed = None
    data_between_dates = None
        
        
    data_between_dates = data_between_dates_form(df, process_id=decompose_tab_type)
   
    selected_column = select_column(df, proces_id=decompose_tab_type)

            
    seasonal_period_help_text = """
                                The frequency of the seasonal component examinated:
                                Annual     1\n
                                Quarterly  4\n
                                Monthly   12\n
                                Weekly    52\n
                                Daily     365
                                """
    seasonal_period = st.number_input('Seasonal period of interest:',
                                      help=seasonal_period_help_text,
                                      key = decompose_tab_type,
                                      min_value=0,
                                      max_value= len(data_between_dates.index)//2,#len(data_between_dates.index)//2,
                                      value = 365 if 365 < len(data_between_dates.index) else len(data_between_dates.index)//2
                                      )

    st.caption("Note: the seasonal period is set to daily by default!")
    
    submit_button(process_id=decompose_tab_type,)
    cancel_submit_button(process_id=decompose_tab_type)
    
        
    if st.session_state[f"processing_{decompose_tab_type}"]:
        decomposed = seasonal_decompose(x=data_between_dates[selected_column], model=decompose_tab_type, period=seasonal_period)

        
    if data_between_dates is not None and decomposed is not None and selected_column is not None:
        # Default data 
        st.subheader("The raw data:")
        fig = go.Figure()
        fig.update_layout(paper_bgcolor="red")
        fig = px.line(x=data_between_dates.index, y=data_between_dates[selected_column])
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Trend", expanded=False):
            fig = go.Figure()
            fig.update_layout(paper_bgcolor="red")
            fig = px.line(x=data_between_dates.index, y=decomposed.trend)
            st.plotly_chart(fig, use_container_width=True)


        with st.expander("Seasonality", expanded=False):
            fig = go.Figure()
            fig.update_layout(paper_bgcolor="red")
            fig = px.line(x=data_between_dates.index, y=decomposed.seasonal)
            st.plotly_chart(fig, use_container_width=True)
            
        with st.expander("Residual", expanded=False):
            fig = go.Figure()
            fig.update_layout(paper_bgcolor="red")
            fig = px.line(x=data_between_dates.index, y=decomposed.resid)
            st.plotly_chart(fig, use_container_width=True)

     

additive_tab, multiplicative_tab = st.tabs(["Additive", "Multiplicative"])

with additive_tab:    
    st.subheader("Additive decompose")
    decompose_tab_content("additive")

with multiplicative_tab:    
    st.subheader("Multiplicative decompose")
    decompose_tab_content("multiplicative")

