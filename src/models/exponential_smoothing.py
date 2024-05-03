
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np
from src.calculations.train_test_split import get_test_subset, get_train_subset
import streamlit as st
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt

    


def run_exponential_smoothing(data: pd.DataFrame, split: float, smoothing_level: float):
    
    train = get_train_subset(data, split)
    test = get_test_subset(data, split)
    
    
    # this is what the model will be trained on
    # values will be assigned gradutally to it
    # and the model retrained
    history = train.values
    
    # resulting list of predictions at each step
    predictions = list()

    # values that will gradually be added to the train set
    test_values = test.values

    for i in range(len(test_values)):
        # (re)train the model
        model = ExponentialSmoothing(history, trend='add',) #bounds={'smoothing_level': smoothing_level})
        model_fit = model.fit(smoothing_level=smoothing_level)
        output = model_fit.forecast()
                 
        yhat = output[0]
        predictions.append(yhat)
        
        actual = test_values[i]
        history = np.append(history, actual)
            
    predictions_series = pd.Series(predictions,
                               name = 'Exp. smoothin',
                                index=test.index)
    
    return predictions_series
        