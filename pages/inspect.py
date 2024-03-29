import streamlit as st
from components.menu import sidebar_menu
import pandas as pd
import time
import plotly.graph_objects as go


st.set_page_config(page_title="Inspect", page_icon = ":chart_with_upwards_trend:", layout="wide")

sidebar_menu()

st.header("Inspect and visualise data", divider = True)

use_default_data = st.checkbox('Use default data', value=True)

if use_default_data:
    df = pd.read_csv("./data/all_stocks_5yr.csv")
    df['date'] = pd.to_datetime(df['date'])
else:        
    if 'df' not in st.session_state:
        df = None
    else:
        df = st.session_state.df



st.subheader("Dataframe:")

earliest_date = df['date'].iloc[0]
latest_date = df['date'].iloc[-1]

#st.write(type(df['date'].iloc[0]))

st.write(f"Earliers date: {earliest_date}")
st.write(f"Latest date: {latest_date}")
# st.dataframe(df)

st.divider()

st.subheader("Select time perioid", divider=True)
start_date_col, end_date_col = st.columns(2)

start_date = start_date_col.date_input(label="Select start date", 
                                       min_value = earliest_date, 
                                       max_value = latest_date,
                                       value = earliest_date)

end_date = end_date_col.date_input(label="Select end date",
                                   min_value = earliest_date,
                                   max_value = latest_date,
                                   value = latest_date)    

if start_date is None or end_date is None: 
    st.caption("Select dates to display the graph")
    
else:
    layout = go.Layout(
                paper_bgcolor='rgba(164, 172, 231, 0.8)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
    fig = go.Figure(layout=layout)
        
    #prediciton
    fig.add_trace(go.Scatter(x=df.index, # needs to be coverted?
                            y=df.close,
                    line_color="red",
                    mode='lines',
                    name='Forecast'))

      
        
    st.plotly_chart(fig, use_container_width=True)
        