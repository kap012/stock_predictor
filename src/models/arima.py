from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np
from src.calculations.train_test_split import get_test_subset, get_train_subset
import streamlit as st
    

def run_arima(data: pd.DataFrame, split: float, lag_order: int, diff_degree: int, ma_window: int) -> pd.Series:
    train = get_train_subset(data, split)
    test = get_test_subset(data, split)
    
    # this is what the model will be trained on in the first run
    # values will be assigned gradutally to it
    # and the model retrained
    history = train.values
    
    # resulting list of predictions at each step
    predictions = list()

    # values that will gradually be added to the train set
    test_values = test.values

    for i in range(len(test_values)):
        # (re)train the model
        model = ARIMA(history, order=(lag_order, diff_degree, ma_window))
        model_fit = model.fit()
        output = model_fit.forecast()
                
        yhat = output[0]
        predictions.append(yhat)
        
        actual = test_values[i]
        history = np.append(history, actual)
            
    predictions_series = pd.Series(predictions,
                               name = 'arima',
                                index=test.index)
        
    return predictions_series
        