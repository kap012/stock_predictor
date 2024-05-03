from sklearn.metrics import root_mean_squared_error 
from sklearn.metrics import mean_absolute_percentage_error 
from sklearn.metrics import mean_absolute_error 
import pandas as pd

def rmse(test_set: pd.DataFrame, forecast: pd.DataFrame):
    return root_mean_squared_error(test_set, forecast)
    
def mape(test_set: pd.DataFrame, forecast: pd.DataFrame):
    return mean_absolute_percentage_error(test_set, forecast)

def mae(test_set: pd.DataFrame, forecast: pd.DataFrame):
    return mean_absolute_error(test_set, forecast)