import streamlit as st
from src.app_logic.data_util import init_data
import plotly.graph_objects as go
from components.sidebar_menu import sidebar_menu
from statsmodels.tsa.stattools import acf
from components.forms.selectboxes import select_column
from components.buttons.submit_button import submit_button, cancel_submit_button
from src.app_logic.session_state_util import init_processing_state, stop_processing
from components.expanders.model_page_expanders import dataframes_expander, graph_expander, errors_expander
from statsmodels.tsa.statespace.tools import diff
from statsmodels.tsa.stattools import adfuller
from components.forms.date_forms import data_between_dates_form



st.set_page_config(page_title="Autocorrelation plots",
                   page_icon=":chart_with_upwards_trend:", layout="wide")

ar_process_key = "AR"
adf_process_id = "ADF"

init_data()
init_processing_state(ar_process_key)
init_processing_state(adf_process_id)
sidebar_menu()


st.header("Autocorrelation")

info_tab, acf_tab, diff_tab ,adf_tets_tab = st.tabs(["Info", "ACF", "Difference", "ADF Test"])

df = st.session_state.df

with info_tab:
    st.subheader("Autocorrelation info")
    
with acf_tab:
    acf_process_id = "acf"
    acf_result = None
    st.subheader("Autocorrelation function")


    data_between_dates = data_between_dates_form(data=df, process_id=acf_process_id)

    selected_column  = select_column(df, ar_process_key)
    
    n_lags = st.number_input('Number of lags',
                help="Number of lags help",
                min_value=0, 
                max_value=len(df.index), 
                value = 10)
    
    submit_button(process_id=ar_process_key)
    
    if st.session_state[f"processing_{ar_process_key}"]:
        with st.spinner("Processing..."):
            acf_result = acf(df[selected_column], nlags=n_lags)
        
    cancel_submit_button(process_id=ar_process_key)
        

    if acf_result is not None:

        dataframes_expander(acf_result)
    
        with st.expander("Graph"): 
            
            # makes the lollipop chart
            layout = go.Layout(
                shapes=[dict(
                    type='line',
                    xref='x',
                    yref='y',
                    x0=i,
                    y0=0,
                    x1=i,
                    y1=acf_result[i],
                    line=dict(
                        color='grey',
                        width=1
                    )
                ) for i in range(len(acf_result))],
                title='ACF Lollipop shape'
            )
                
            fig = go.Figure(layout=layout)
            
            fig.add_trace(go.Scatter(
                                        x= [i for i in range(n_lags)],
                                        y=acf_result,
                                        mode='markers',
                                        name='ACF')
                                    )
            
            fig.update_layout(
                yaxis_title = "Autocorrelation",
                xaxis_title = "Time lag",
            )
        
            st.plotly_chart(fig, use_container_width=True)

with diff_tab:
    diff_proces_id = "diff"
    init_processing_state(process_id=diff_proces_id)
    st.subheader("Difference the time series")
    
    data_between_dates = data_between_dates_form(data=df, process_id=adf_process_id)
    
    selected_column = select_column(df=data_between_dates, proces_id=diff_proces_id)
    
    d_of_differencing = st.number_input(label="Degree of differencing:",
                    help = "Degree of diff help",
                    value = 1,
                    min_value=1 
                    )
    
    submit_button(process_id=diff_proces_id)
    
    cancel_submit_button(process_id=diff_proces_id)
    
    differenced = None
    if st.session_state[f"processing_{diff_proces_id}"]:
        differenced = diff(data_between_dates[selected_column], k_diff=d_of_differencing)
    
    if differenced is not None:
        with st.expander("Original"):
            layout = go.Layout()
            res_fig = go.Figure(layout=layout)
            res_fig.add_trace(go.Scatter(x=data_between_dates.index,
                                        y=data_between_dates[selected_column],
                                        mode='lines',
                                        name='Original'))
            st.plotly_chart(res_fig, use_container_width=True)
        
        with st.expander("Differenced"):
            layout = go.Layout()
            res_fig = go.Figure(layout=layout)
            res_fig.add_trace(go.Scatter(x=data_between_dates.index,
                                        y=differenced,
                                        mode='lines',
                                        name='Differenced'))
            st.plotly_chart(res_fig, use_container_width=True)


with adf_tets_tab:
    st.subheader("Augmented Dickey-Fuller test")

    st.caption("You can choose to take the difference of your data before the test:")
    diff_order = st.number_input('Difference order',
                        help="How many times will the differencing be performe on the data",
                        min_value=0, 
                        max_value=100, 
                        value = 0)

    significance_lvl = st.number_input('Significance level',
                    help="The condition value for the test to use",
                    min_value=0.0, 
                    max_value=1.0, 
                    step=0.01,
                    value = 0.05)
    
    selected_column = select_column(df=df, proces_id=adf_process_id)
    
    adf_result = None
    submit_button(process_id=adf_process_id)
    cancel_submit_button(process_id=adf_process_id)

    if st.session_state[f"processing_{adf_process_id}"]:
        ts =  df[selected_column]
        ts_differenced = diff(ts, k_diff=diff_order)
        adf_result = adfuller(ts_differenced)

        # adfuller() returns a tuple
        # the second value is the p-value
        
    
    
    if adf_result is not None:
        st.subheader("Test results")
        sign_lvl_col, test_stat_col, p_val_col = st.columns(3) 
        
        sign_lvl_col.metric(label="Selected siginificance level", 
                            value= significance_lvl)
        
        test_stat = adf_result[0]
        test_stat_col.metric(label="Test statistic",
                            value= round(test_stat, 3))
        
        p_val = adf_result[1]
        p_val_col.metric(label="Test p-value",
                         value = round(p_val, 3),
                         delta = "p-value is smaller than the significance level!" if p_val < significance_lvl 
                                else "p-value is greater than the significance level!",
                         delta_color = 'inverse'
                         )

        if p_val < significance_lvl:
            st.subheader("Null hypothesis rejected!")
            st.write("The data is stationary")
        else:   
            st.subheader("Null hypothesis failed to reject!")
            st.write("The data is not stationary")