import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from statsmodels.tools.eval_measures import rmse        
from sklearn.metrics import mean_absolute_percentage_error     


def dataframes_expander(data: pd.DataFrame):
    with st.expander("Dataframes", expanded=False):
        
        st.write(data)
    
  
def graph_expander(forecast: pd.DataFrame, actual: pd.DataFrame):  
    with st.expander("Graph", expanded=False):
        layout = go.Layout()
        res_fig = go.Figure(layout=layout)
        
        res_fig.add_trace(go.Scatter(x=forecast.index,
                                    y=forecast,
                                    line_color="red",
                                    mode='lines',
                                    name='Forecast'))
        
        res_fig.add_trace(go.Scatter(x=actual.index,
                                    y=actual,
                                    line_color="blue",
                                    mode='lines',
                                    name='Actual'))
        
        st.plotly_chart(res_fig, use_container_width=True)
    
    
    # ERRORS 
def errors_expander(test_set: pd.DataFrame, prediction: pd.DataFrame):
    with st.expander("Error metrics", expanded=False):


        error_cols = st.columns(2)
        
        rmse_result = rmse(test_set, prediction)
        rmse_rounded = round(rmse_result, 3)
        error_cols[0].metric(label="RMSE", help="rmse help text", value=rmse_rounded)
        
      
        
        mape_result = mean_absolute_percentage_error(test_set, prediction)
        mape_rounded = round(mape_result, 3)
        error_cols[1].metric(label="MAPE", help="rmse help text", value=mape_rounded)

