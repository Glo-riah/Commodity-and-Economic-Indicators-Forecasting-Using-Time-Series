import streamlit as st
import pandas as pd
import numpy as np
from tensorflow import keras
from PIL import Image

# Load the saved models
models = {}
for product in ['Bread(400g)', 'Vegetable Oil (1L)', 'Milk (500ML)', 'Diesel (1L)', 'Maize meal (2kg)', 'Gasoline (1L)', 'Inflation', 'Exchange Rate (USD)']:
    model = keras.models.load_model(f"{product}_time_series_model.h5")
    models[product] = model

# Define the forecast periods and dates
forecast_periods = 12
forecast_dates = pd.date_range(start='2023-04-01', periods=forecast_periods, freq='MS')

# Define the commodities, months, and years
commodities = ['Bread(400g)', 'Vegetable Oil (1L)', 'Milk (500ML)', 'Diesel (1L)', 'Maize meal (2kg)', 'Gasoline (1L)', 'Inflation', 'Exchange Rate (USD)']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
years = [2023, 2024]

# Display the title of the app
st.title('PriceWise AI')

# Load the data from the file
train_data = pd.read_csv("Time Series Data.csv")

n_steps = 3

# Create a dictionary to store the forecasted prices for each commodity
forecast_prices_dict = {}

# Create image objects for each commodity
maize_img = Image.open("maize.jpg")
bread_img = Image.open("bread.jpg")
oil_img = Image.open("oil.jpg")
milk_img = Image.open("milk.jpg")
diesel_img = Image.open("diesel.jpg")
gasoline_img = Image.open("gasoline.jpg")
inflation_img = Image.open('inflation.jpg')
buy_img = Image.open("dollar.jpg")

# Create a sidebar for selecting the commodity, month, and year
commodity = st.sidebar.selectbox('Commodity/ Economic Indicator:', commodities, index=0, format_func=lambda x: x.split('(')[0])

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


# Create a sidebar for selecting the month and year
month = st.sidebar.selectbox('Month:', months, index=0)
year = st.sidebar.selectbox('Year:', years, index=0)

# Combine the selected month and year into a single datetime object
selected_date = pd.to_datetime(f'{month} {year}', format='%B %Y')

# Create a dictionary to store the forecasted prices for each commodity
forecast_prices_dict = {}

# Get the last n_steps values from the training set
last_n_steps = train_data[commodity][-n_steps:].values.reshape(-1, 1)

# Create an empty list to store the forecasted prices
forecast_prices = []

# Loop through the forecast periods and make predictions
for i in range(forecast_periods):
    # Reshape the last_n_steps array for input into the model
    last_n_steps = last_n_steps.reshape(1, n_steps, 1)

    # Make a prediction using the model
    forecast = models[commodity].predict(last_n_steps)[0][0]

    # Append the forecast to the list of forecasted prices
    forecast_prices.append(forecast)

    # Update the last_n_steps array with the new forecasted value
    last_n_steps = np.vstack([last_n_steps[0][1:], [[forecast]]])

# Add the forecasted prices to the dictionary
forecast_prices_dict[commodity] = forecast_prices

# Find the index of the selected month in the forecast dates
index = months.index(month)

# Get the forecasted price for the selected month and year
forecast_price = forecast_prices_dict[commodity][index]

if commodity == "Inflation":
    forecasted_price_str = f"**Forecasted {commodity.capitalize()}: {forecast_price:.2f}**"
elif commodity == "Exchange Rate (USD)":
    forecasted_price_str = f"**Forecasted {commodity.capitalize()}: {forecast_price:.2f}**"
else:
    forecasted_price_str = f"**Forecasted Price for {commodity.capitalize()}: Ksh {forecast_price:.2f}**"

st.subheader(forecasted_price_str)