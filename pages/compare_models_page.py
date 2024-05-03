import streamlit as st
from components.sidebar_menu import sidebar_menu
import pandas as pd
from src.app_logic.data_util import init_data
import plotly.graph_objects as go
from src.app_logic.session_state_util import init_processing_state, start_processing, stop_processing
from components.forms.date_forms import data_between_dates_form
from components.buttons.submit_button import submit_button, cancel_submit_button
from components.expanders.model_page_expanders import dataframes_expander, graph_expander, errors_expander
from src.calculations.train_test_split import get_test_subset
from components.forms.selectboxes import select_column
from src.app_logic.compare_page_util import get_model_column_view, run_model
from src.calculations.errors_metrics import rmse, mape, mae


MODELS = ["Persisence Forecast", "Exponential Smoothing", "ARIMA"]

st.set_page_config(page_title="Compare models", page_icon = ":chart_with_upwards_trend:", layout="wide")

init_data()
sidebar_menu()

st.header("Compare models", divider = True)

df = st.session_state.df

page_name = "compare"
init_processing_state(page_name)

data_between_dates = data_between_dates_form(df, process_id=page_name)

split = st.number_input('Select Train/Test split',help="Train/Test split help", min_value=0.0, max_value=1.0, step=0.01, value = 0.66)
selected_column = select_column(df, page_name)




        

# Columns
st.subheader("Select models", divider=True)
n_columns = st.select_slider(label = "Select the number of models to compare", options = (1, 2, 3, 4))   

for col_number in range(n_columns):
    dict_name = f"col{col_number}_dict"
    if  dict_name not in st.session_state:
        st.session_state[dict_name] = dict()
        
columns_list = st.columns(n_columns)
model_name_list = [None] * len(columns_list)

for col_idx, column in enumerate(columns_list):
    dict_name = f"col{col_idx}_dict"
    
    with column:
        subheader_placeholder = st.empty().subheader(f"Model {col_idx + 1 }")
   
        model_name = column.selectbox(label="Select model", 
                    options=MODELS, 
                    placeholder ="No model selected",
                    index=None,
                    key=col_idx)
        
        if col_idx == 0:
            st.caption("Your baseline algorithm")
        
        if model_name is not None:
            model_name_list[col_idx] = model_name
            subheader_placeholder.empty()
            subheader_placeholder.subheader(model_name)
        
        get_model_column_view(model_name, dict_name, col_idx)
    
 
def check_if_any_model_selected():
    for model in model_name_list:
        if model is not None:
            return True
    return False

if not check_if_any_model_selected():
    stop_processing(page_name)
    

# Create a dictionary for each model in the columnns
# store them in the session state

# then add a switch satement that based on the model_name will select the appropriate function
# and then get the values from the dictionary
 
#predictions = [None] * n_columns

predictions = list()

 
# Buttons
st.divider() 
submit_button(text="Train models", disabled=not check_if_any_model_selected() or select_column is None, process_id=page_name)
cancel_submit_button(page_name)

if selected_column is None:
    st.caption("Select column to see the results")
    st.stop()
elif n_columns == len(model_name_list) and None in model_name_list:
    st.caption("Select model or change the number of models ")
    st.stop()

    
if st.session_state[f"processing_{page_name}"]:    
    with st.spinner('Training the models...'):
        for col_idx, column in enumerate(columns_list):
            
            model_name = model_name_list[col_idx]
            dict_name = f"col{col_idx}_dict"
            
            pred = run_model(model_name, dict_name, data_between_dates[selected_column], split)
            predictions.append(pred)     
            
            
        st.toast('Models trained succesfully!', icon="✅")
        stop_processing(page_name)
   
if not predictions:
    st.caption("Train the models to see the results")
    st.stop()

# Results

test_set = get_test_subset(data_between_dates[selected_column], split=split)


# dataframes_expander()
# graph_expander()
# errors_expander()

# Dataframes
with st.expander("Dataframes", expanded=False):
    st.write("Results:")
    test_set = test_set.rename('Actual')
    
    res = pd.DataFrame(test_set)
    
    for col_idx, column in enumerate(columns_list):
        predictions_series = predictions[col_idx]
        old_col_name = predictions_series.name
        
        predictions_series = predictions_series.rename(f'{col_idx+1}_{old_col_name}')
                       
        res = pd.concat([res,predictions_series], axis=1)
    
    st.write(res)        
        
        
        


# GRAPHS

with st.expander("Graph", expanded=False):
    layout = go.Layout()
    res_fig = go.Figure(layout=layout)
    res_fig.add_trace(go.Scatter(x=data_between_dates.index,
                                    y=data_between_dates[selected_column],
                                    showlegend=True,
                                    mode='lines',
                                    name='Actual'))
    
    for col_idx, column in enumerate(columns_list):
            predictions_series = predictions[col_idx]
            
            
            if predictions_series is not None:
                res_fig.add_trace(go.Scatter(x=predictions_series.index,
                                            y=predictions_series,
                                            mode='lines',
                                            name=  f"{col_idx}_{model_name_list[col_idx]}_forecast"))
    
            
    st.plotly_chart(res_fig, use_container_width=True)
    
    
        


            
with st.expander("Error metrics"):
    mode_name_col, rmse_col, mape_col, mae_col = st.columns(4)
    
    pred = predictions[0]
    baseline_rmse = round(rmse(test_set, pred), 3)
    baseline_mape = round(mape(test_set, pred), 3)
    baseline_mae = round(mae(test_set, pred), 3)

    mode_name_col.write(model_name_list[0])
    mode_name_col.caption('Baseline model')
    
    mode_name_col.container(border=False, height=30) 
    rmse_col.metric(value=baseline_rmse, label = "RMSE")
    mape_col.metric(value=baseline_mape, label = "MAPE")
    mae_col.metric(value=baseline_mape, label = "MAE")
    
    for idx in range(1, len(predictions)):
        
        pred = predictions[idx]
        rmse_result = round(rmse(test_set, pred), 3)
        mape_result = round(mape(test_set, pred), 3)
        mae_result = round(mae(test_set, pred), 3)

        mode_name_col.write(model_name_list[idx])

        mode_name_col.container(border=False, height=25) 
    
        
        rmse_col.metric(value=rmse_result, 
                        delta= round(baseline_rmse - rmse_result, 3) if baseline_rmse != rmse_result else None,
                        label = "RMSE")
        
        mape_col.metric(value=mape_result, 
                        delta = round(baseline_mape - mape_result, 3) if baseline_mape != mape_result else None,
                        label = "MAPE")
        
        mae_col.metric(value=mae_result,
                       delta= round(baseline_mae - mae_result, 3) if baseline_mae != mae_result else None,
                       label = "MAE")
      