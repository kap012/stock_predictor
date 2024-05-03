import streamlit as st
import pandas as pd

DEFAULT_FILE_PATH = "./data/AAPL.csv"
DEFAULT_DATE_COL_NAME = 'date'

def get_df_from_csv(file):
    df = pd.read_csv(file)
    return df
    

def store_df_in_session(df):
    st.session_state.df = df       


def init_data():
    if 'df' not in st.session_state or st.session_state is None:
        load_default_data()

        
def load_default_data():
    default_df = get_df_from_csv(DEFAULT_FILE_PATH)
    default_df = columns_to_lowercase(default_df)    
    default_df = set_date_as_idx(default_df, DEFAULT_DATE_COL_NAME)
    store_df_in_session(default_df)        
    
    

def set_date_as_idx(df: pd.DataFrame, date_col_name: str):
    # 1. Convert the column to datetime (pd.to_datetime())
    datetime_col = pd.to_datetime(df[date_col_name], utc=True)  

    # 2. Make the idx equal to the date part of the datetime column 
    df.index = datetime_col
    
    # 3. Remove the date column
    df = df.drop(date_col_name, axis=1)

    # 4. Fill in the missing dates (run pd.asfreq('d'))
    df = df.asfreq('d')

    # 5. Fill in the missing values (run pd.fillna('ffill'))
    df = df.ffill()
    
    # 6. Get only the date part
    df.index = df.index.date
    
    return df

def columns_to_lowercase(df: pd.DataFrame):
    df.columns = df.columns.str.lower()
    return df

def get_comparison_df(test_set: pd.DataFrame, forecast: pd.DataFrame):   
    concated = pd.concat([test_set, forecast], keys=['Actual', 'Forecasted'], axis=1)
    concated["difference"] = concated["Actual"] - concated["Forecasted"]
    
    return concated
