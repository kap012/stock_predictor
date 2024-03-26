import pandas as pd
from prophet import Prophet

def predict(df):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=360)
    forecast = model.predict(future)

    return forecast