import streamlit as st
from components.menu import sidebar_menu
from io import StringIO
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from components.checkboxes import use_default_data_or_upload_checkbox


st.set_page_config(page_title="File upload with checkbox", page_icon = ":chart_with_upwards_trend:", layout="wide")

sidebar_menu()

st.header("Upload file", divider = True)

use_default_data_or_upload_checkbox()

if 'df' in st.session_state and st.session_state.df is not None:     
   
   
    popover = st.popover("Inspect")
    show_dataframe = popover.checkbox("Show the dataframe.", False)
    show_graph = popover.checkbox("Show the graph.", False)
    
    if show_dataframe or show_graph:
        columns = st.multiselect("Select columns to display", 
                                placeholder="No columns selected",
                                options = st.session_state.df.columns.values)
        
        if columns is None: 
            st.caption("Select columns to display")    
            
        if show_dataframe and columns:
            st.dataframe(st.session_state.df [columns])
            
        if show_graph and columns:
            layout = go.Layout(
                paper_bgcolor='rgba(164, 172, 231, 0.8)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            fig = go.Figure(layout=layout)

            for col in columns:
                fig.add_trace(go.Scatter(x=st.session_state.df.index, 
                                        y=st.session_state.df[col],
                                mode='lines',
                                name=col))
            
            st.plotly_chart(fig, use_container_width=True)
