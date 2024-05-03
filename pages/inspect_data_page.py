import streamlit as st
from components.sidebar_menu import sidebar_menu
import pandas as pd
import time
import plotly.graph_objects as go
from src.app_logic.data_util import init_data
from components.forms.selectboxes import select_column

st.set_page_config(page_title="Inspect Data", page_icon = ":chart_with_upwards_trend:", layout="wide")


init_data()
sidebar_menu()

page_name = "Inspect data"

# load default data:

st.header("Inspect and visualise data", divider = True)
df = st.session_state.df
st.subheader("Select time perioid", divider=True)

earliest_date = df.index[0]
latest_date = df.index[-1]

start_date_col, end_date_col = st.columns(2)

with start_date_col:
    start_date = st.date_input(label="Select start date", 
                                        min_value = earliest_date, 
                                        max_value = latest_date,
                                        value = earliest_date
                                        )

with end_date_col:
    end_date = st.date_input(label="Select end date",
                                    min_value = earliest_date,
                                    max_value = latest_date,
                                    value = latest_date 
                                )   



column_to_display = select_column(df, page_name)

if start_date is None or end_date is None: 
    st.caption("Select dates to display the graph")
elif column_to_display is None:
    st.caption("Select column to display the graph")
else:
    df = df.loc[start_date:end_date]
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.index,
                            y=df[column_to_display],
                            mode='lines',
                            name=column_to_display))
  
    st.plotly_chart(fig, use_container_width=True)
        