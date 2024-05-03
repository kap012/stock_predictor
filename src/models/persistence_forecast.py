import pandas as pd
from src.calculations.train_test_split import get_test_subset, get_train_subset
import streamlit as st
import math

def model_persistence(x):
    # return the current value as the prediction for the next value
    return x


def run_persistence_forecast(data: pd.DataFrame, split: float, shift ) -> pd.Series:
    test_df = get_test_subset(data, split)
    
    
    test_values = test_df.values

    predictions = []
    
    for i in range(len(test_values)):
        if i == 0:
            pred = model_persistence(test_values[i])
        else:
            pred = model_persistence(test_values[i-shift])

        predictions.append(pred)
    
    forecast_series = pd.Series(name='persistence_forecast',
                                data=predictions,
                                index=test_df.index)
        
    return forecast_series