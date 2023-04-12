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
forecast_dates = pd.date_range(start='2023-03-01', periods=forecast_periods, freq='MS')

# Define the commodities and their corresponding indices
commodities = ['Bread(400g)', 'Vegetable Oil (1L)','Milk (500ML)','Diesel (1L)','Maize meal (2kg)','Gasoline (1L)','Inflation','Exchange Rate (USD)']
commodity_indices = {commodity: i for i, commodity in enumerate(commodities)}

# Define the default values for the commodity, month, and year
default_commodity = 'Bread(400g)'
default_month = 'April'
default_year = '2023'

def get_forecast_prices(commodity):
    # Get the index of the commodity
    commodity_index = commodity_indices[commodity]

    # Get the last n_steps values from the training set
    last_n_steps = train_data[commodity][-n_steps:].values.reshape(-1, 1)

    # Create an empty list to store the forecasted prices
    forecast_prices = []

    # Make predictions for the forecast periods
    for i in range(forecast_periods):
        # Make a prediction using the model
        forecast = models[commodity].predict(last_n_steps)[0][0]

        # Append the forecast to the list of forecasted prices
        forecast_prices.append(forecast)

        # Update the last_n_steps array with the new forecasted value
        last_n_steps = np.vstack([last_n_steps[1:], [[forecast]]])

    # Return the forecasted prices
    return forecast_prices


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

def get_forecast_price(commodity, month, year):
    # Get the forecasted prices for the selected commodity
    forecast_prices = get_forecast_prices(commodity)

    # Get the index of the selected month
    available_months = pd.date_range(start=pd.Timestamp('2023-04-01'), periods=12, freq='MS').strftime('%B').tolist()
    month_index = available_months.index(month)

    # Get the index of the selected year
    available_years = [pd.Timestamp('2023-04-01').year + i for i in range(12)]
    year_index = available_years.index(int(year))

    # Get the forecasted price for the selected month and year
    forecasted_price = forecast_prices[year_index*12 + month_index]

    # Return the forecasted price
    return forecasted_price

# Define the default values for the month and year
months = pd.date_range(start='2023-01-01', end='2023-12-31', freq='MS').strftime('%B').tolist()
default_month = months[0]
default_year = '2023'

# Define the sidebar
st.sidebar.header('Select Commodity and Date')
selected_commodity = st.sidebar.selectbox('Commodity', commodities, index=commodity_indices[default_commodity], format_func=lambda x: x.split('(')[0])
selected_month = st.sidebar.selectbox('Month', months, index=pd.to_datetime(default_month, format='%B').month-1)
selected_year = st.sidebar.selectbox('Year', forecast_dates.year.unique(), index=0)

# Get the forecasted price for the selected commodity, month, and year
forecasted_price = get_forecast_price(selected_commodity, selected_month, selected_year)

# Display the forecasted price
st.write(f"Forecasted price for {selected_commodity} in {selected_month} {selected_year}: {forecasted_price:.2f}")

# Add images to the UI
if selected_commodity == "Maize meal (2kg)":
   st.image(maize_img, width=300)
elif selected_commodity == "Bread(400g)":
   st.image(bread_img, width=300)
elif selected_commodity == "Vegetable Oil (1L)":
   st.image(oil_img, width=300)
elif selected_commodity == "Milk (500ML)":
   st.image(milk_img, width=300)
elif selected_commodity == "Diesel (1L)":
   st.image(diesel_img, width=300)
elif selected_commodity == "Gasoline (1L)":
   st.image(gasoline_img, width=300)
elif selected_commodity == "Inflation":
   st.image(inflation_img, width=600)
elif selected_commodity == "Exchange Rate (USD)":
   st.image(buy_img, width=300)


# Define the forecasted price string with Markdown syntax
if selected_commodity == "Inflation":
    forecasted_price_str = f"**Forecasted {selected_commodity.capitalize()}: {forecasted_price:.2f}**"
elif selected_commodity == "Exchange Rate (USD)":
    forecasted_price_str = f"**Forecasted {selected_commodity.capitalize()}: {forecasted_price:.2f}**"
else:
    forecasted_price_str = f"**Forecasted Price for {selected_commodity.capitalize()}: Ksh {forecasted_price:.2f}**"

# Display the forecasted price with increased font size and bold formatting
st.header(forecasted_price_str)
