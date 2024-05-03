import pandas as pd
from src.calculations.train_test_split import get_test_subset, get_train_subset
import streamlit as st

def model_persistence(x):
    # return the current value as the prediction for the next value
    return x


def run_persistence_forecast(data: pd.DataFrame, split: float, shift = 1) -> pd.Series:
    
    train_df = get_train_subset(data, split)
    test_df = get_test_subset(data, split)
    
    
    forecast_series = pd.Series(name='persistence_forecast')
    
    test_values = train_df.values

    for i in range(shift, len(test_values)):
        last_actual = test_values[i - 1]
        
        forecast_value = model_persistence(last_actual)
       
        forecasted_idx = test_df.index[i - shift - 1]
        st.write(forecasted_idx)
        
        forecast_series[forecasted_idx] =  forecast_value
        
        #st.write(test_df.index[i+shift])
        
        #forecast_series[test_df.index[i+shift]] = yhat
        
    return forecast_series