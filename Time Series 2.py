import streamlit as st
import pandas as pd
import numpy as np
from tensorflow import keras
from PIL import Image

# Load the saved models
models = {}
for product in ['Bread(400g)', 'Vegetable Oil (1L)','Milk (500ML)','Diesel (1L)','Maize meal (2kg)','Gasoline (1L)','Inflation','Exchange Rate (USD)']:
    model = keras.models.load_model(f"{product}_time_series_model.h5")
    models[product] = model

# Define the forecast periods and dates
forecast_periods = 12
forecast_dates = pd.date_range(start='2023-04-01', periods=forecast_periods, freq='MS')

# Define the commodities and their corresponding indices
commodities = ['Bread(400g)', 'Vegetable Oil (1L)','Milk (500ML)','Diesel (1L)','Maize meal (2kg)','Gasoline (1L)','Inflation','Exchange Rate (USD)']
commodity_indices = {commodity: i for i, commodity in enumerate(commodities)}

# Define the default values for the commodity, month, and year
default_commodity = 'Bread(400g)'
default_month = 'April'
default_year = '2023'

def get_forecast_price(commodity, month, year):
    # Get the index of the commodity
    commodity_index = commodity_indices[commodity]

    # Get the last n_steps values from the training set
    last_n_steps = train_data[commodity][-n_steps:].values.reshape(-1, 1)

    # Calculate the number of months between the start date and the selected date
    selected_date = pd.to_datetime(f"{month} {year}")
    months_since_start = (selected_date - forecast_dates[0]) // pd.Timedelta(days=30)

    # Make predictions for the selected date
    forecast = models[commodity].predict(last_n_steps)[0][0]
    for i in range(months_since_start):
        last_n_steps = np.vstack([last_n_steps[1:], [[forecast]]])
        forecast = models[commodity].predict(last_n_steps)[0][0]

    # Return the forecasted price
    return forecast

# Load the data from the file
train_data = pd.read_csv("Time Series Data.csv")

# Define the number of steps to use for input to the model
n_steps = 12

# Set the title of the app
st.title('PriceWise AI')

# Add images to the UI
maize_img = Image.open("maize.jpg")
bread_img = Image.open("bread.jpg")
oil_img = Image.open("oil.jpg")
milk_img = Image.open("milk.jpg")
diesel_img = Image.open("diesel.jpg")
gasoline_img = Image.open("gasoline.jpg")
inflation_img = Image.open('inflation.jpg')
buy_img = Image.open("dollar.jpg")

# Create a sidebar for selecting the commodity, month, and year
commodity = st.sidebar.selectbox('Commodity/ Economic Indicator:', commodities, index=commodity_indices[default_commodity], format_func=lambda x: x.split('(')[0])

# Add images to the UI
if commodity == "Maize meal (2kg)":
   st.image(maize_img, width=300)
elif commodity == "Bread(400g)":
   st.image(bread_img, width=300)
elif commodity == "Vegetable Oil (1L)":
   st.image(oil_img, width=300)
elif commodity == "Milk (500ML)":
   st.image(milk_img, width=300)
elif commodity == "Diesel (1L)":
   st.image(diesel_img, width=300)
elif commodity == "Gasoline (1L)":
   st.image(gasoline_img, width=300)
elif commodity == "Inflation":
   st.image(inflation_img, width=600)
elif commodity == "Exchange Rate (USD)":
   st.image(buy_img, width=300)

# Define the default start date
default_start_date = pd.Timestamp('2023-04-01')

# Create a date picker for selecting the start date
start_date = st.sidebar.date_input('Start Date:', value=default_start_date, min_value=default_start_date, max_value=pd.Timestamp('now'))

# Get the available months based on the selected start date
end_date = start_date + pd.DateOffset(months=forecast_periods)
available_months = pd.date_range(start=start_date, end=end_date, freq='MS').strftime('%B')

# Create dropdowns for selecting the month and year
month = st.sidebar.selectbox('Month:', available_months, index=0)
year = st.sidebar.selectbox('Year:', [start_date.year, start_date.year+1])

# Get the forecasted price for the selected commodity, month, and year
forecasted_price = get_forecast_price(commodity, month, year)

# Define the forecasted price string with Markdown syntax
if commodity == "Inflation":
    forecasted_price_str = f"**Forecasted {commodity.capitalize()}: {forecasted_price:.2f}**"
elif commodity == "Exchange Rate (USD)":
    forecasted_price_str = f"**Forecasted {commodity.capitalize()}: {forecasted_price:.2f}**"
else:
    forecasted_price_str = f"**Forecasted Price for {commodity.capitalize()}: Ksh {forecasted_price:.2f}**"

# Display the forecasted price with increased font size and bold formatting
st.header(forecasted_price_str)
