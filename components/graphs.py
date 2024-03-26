import streamlit as st
import pandas as pd


def simple_graph(header_txt: str, ticker: str, data: pd.Series):
    st.header(header_txt)
    st.subheader("Ticker " + ticker)
    st.scatter_chart(data)


def double_graph(header_txt: str, ticker: str, data: pd.DataFrame, prediction: pd.DataFrame):
    st.header(header_txt)
    st.subheader("Ticker " + ticker)

    #combined = pd.concat([data, prediction], axis=1, join='inner')
    st.write(data)
    st.write(prediction)


    #prediction = prediction[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    st.line_chart(prediction, x='ds', y=['yhat', 'yhat_lower', 'yhat_upper',])
    # chart_data = pd.DataFrame(
    #     {
    #         "col1": data["y"],
    #         "col2": prediction['yhat'],
    #         "col3": data.index
    #     }
    # )
    # st.line_chart(chart_data, x="col1", y="col2", color="col3")
