import streamlit as st

def ticker_dropdown():
    return st.selectbox(
        options=('MSFT', 'AAPL'),
        placeholder="Select ticker:",
        label='Select ticker',
    )