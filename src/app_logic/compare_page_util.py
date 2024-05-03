from components.model_column_views.arima_column_view import arima_column_view
from components.model_column_views.persisntence_column_view import persistence_column_view
from components.model_column_views.exp_smoothing_column_view import exp_smoothing_column_view
from src.models.arima import run_arima
from src.models.exponential_smoothing import run_exponential_smoothing
from src.models.persistence_forecast import run_persistence_forecast
import streamlit as st
import pandas as pd

def get_model_column_view(model_name: str, dict_name: dict, col_idx):
    match model_name:
        case "ARIMA":
            return arima_column_view(dict_name, col_idx)
        case "Exponential Smoothing":
            return exp_smoothing_column_view(dict_name, col_idx)
        case "Persisence Forecast":
            return persistence_column_view(dict_name, col_idx)
        
        
def run_model(model_name: str, dict_name: str, data: pd.DataFrame, split: float):

    data_dict = st.session_state[dict_name]
    
    match model_name:
        case "ARIMA":
            return run_arima(data, 
                            split,
                            data_dict['lag_order'],
                            data_dict['diff_degree'],
                            data_dict['ma_window']
                            )
        case "Exponential Smoothing":
            return run_exponential_smoothing(data,
                                             split,
                                             data_dict["smoothing_level"])
        case "Persisence Forecast":
            return run_persistence_forecast(data,
                                            split, 
                                            data_dict["shift"])