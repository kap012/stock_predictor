import streamlit as st
import pandas as pd

def select_column(df: pd.DataFrame, proces_id: str):
    column_name = st.selectbox(label='Select the column:',
                                    key = f"{proces_id}_select_column",
                                    options=df.columns,
                                    index=None
                                )   
    return column_name
