import streamlit as st
from components.menu import sidebar_menu
import pandas as pd
import plotly.graph_objects as go
from models.arima.util import run_arima
from models.model_util import get_test_subset
import numpy as np


st.set_page_config(page_title="Stocks", page_icon = ":chart_with_upwards_trend:", layout="wide")

sidebar_menu()

placeholder = st.empty()

ticker = st.selectbox(
    label='Select ticker',
    options=('AAPL', 'MSFT', 'AMZN'),
    index=0
    )

data = pd.read_csv('data/all_stocks_5yr.csv')


if ticker is None:
    placeholder.header("Select stock")
else:
    placeholder.header(f"Selected stock: {ticker}")
    data = data[data["Name"] == ticker]
    data = data.iloc[0:100]


basic, arima  = st.tabs(["Price", "ARIMA"])


with basic:
    import plotly.express as px
    
    fig  = go.Figure()
    fig.update_layout(paper_bgcolor="red")


    if ticker is not None: 
        fig = px.line(data, x='date', y='close')
        
        
    st.plotly_chart(fig, use_container_width=True)

    pass


with arima:
    cols = st.columns(4)
    lag_order = cols[0].number_input('Lag order', min_value=0, max_value=10, value = 1)
    diff_degree = cols[1].number_input('Degree of differencing', min_value=0, max_value=10, value = 1)
    ma_window = cols[2].number_input('Moving average window', min_value=0, max_value=10, value = 1)
    split = cols[3].number_input('Train/Test split', min_value=0.0, max_value=1.0, step=0.1, value = 0.66)
    
    key = ticker + str(lag_order) + str(diff_degree) + str(ma_window) + str(split)

    # init the session storage
    if 'processed' not in st.session_state:
        st.session_state.processed = {}

    # Process and save results
    if st.button('Process'):
        if key not in st.session_state.processed:
            with st.spinner('Training the model...'):
                result = run_arima(data, split, lag_order, diff_degree, ma_window)
                #result = data.iloc[int(len(data) * split):len(data)]
                # st.balloons()
                st.toast('Model trained successfully!', icon="✅")
                st.session_state.processed[key] = result
        
    
    # display if exists
    if key in st.session_state.processed:
        st.write(f'Option {key} processed with add ')
        predictions_series = st.session_state.processed[key]
        st.write(predictions_series)
        
        layout = go.Layout(
                paper_bgcolor='rgba(164, 172, 231, 0.8)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        res_fig = go.Figure(layout=layout)
        
        #prediciton
        res_fig.add_trace(go.Scatter(x=predictions_series.index, # needs to be coverted?
                                                              y=predictions_series,

                                         line_color="red",
                    mode='lines',
                    name='Forecast'))
        
        #actual
        res_fig.add_trace(go.Scatter(x=data['date'],
                                                    y=data.close,
                    line_color="blue",
                    mode='lines',
                    name='Actual'))

      
        
        st.plotly_chart(res_fig, use_container_width=True)
        
        
        
        # ERRORS 
        
        test = get_test_subset(data, split=split) 
        #st.write(test['close'])
        #st.write(predictions_series)
        errors = test['close'] - predictions_series
        st.write(errors)
        mae = np.mean(np.abs(errors))
        #st.write(mae)
        st.metric(label="MAE", value=mae)

    
    