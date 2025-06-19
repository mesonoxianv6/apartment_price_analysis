import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from data_analysis import (load_data, preprocess_data, avg_price_by_month, avg_price_by_city, avg_building_age_by_city,
count_21st_century_buildings, new_building_share_by_city, build_city_metrics, distance_price_corr, corr_per_city, 
avg_price_by_dist_from_centre_bins)

df = load_data("data/data_dropped.csv")
df = preprocess_data(df)

st.title("Apartments prices")
st.write("x")

st.header("Average price per sqm over time")
monthly = avg_price_by_month(df)
fig, ax = plt.subplots()
monthly.plot(ax=ax, marker='o', linestyle='-', color='blue', markersize=4, linewidth=3)
ax.set_title("Average price per sqm over time")
ax.set_xlabel("Month")
ax.set_ylabel("Price per sqm")
st.pyplot(fig)  

st.header("Average price per sqm by city")
cities = avg_price_by_city(df)
fig, ax = plt.subplots()
cities.plot(kind='bar', ax=ax, color='orange')
ax.set_title("Average price per sqm by city")
ax.set_xlabel("City")
ax.set_ylabel("Price per sqm") 
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.header("Average building age by city")
ages = avg_building_age_by_city(df)
fig, ax = plt.subplots()
ages.plot(kind='bar', ax=ax, color='purple')
ax.set_title("Average building age by city")
ax.set_xlabel("City")
ax.set_ylabel("Building age (years)")
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.header("Share of 21st century buildings by city")
share = new_building_share_by_city(df)
fig, ax = plt.subplots()
share.plot(kind='bar', ax=ax, color='green')
ax.set_title("Share of 21st century buildings by city")
ax.set_xlabel("City")
ax.set_ylabel("Share (%)")
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.header("City metrics")
city_metrics = build_city_metrics(df)
st.write(city_metrics) 
st.header("Correlation between distance to city center and price per sqm")
corr = distance_price_corr(df)
st.write(corr)

st.header("Correlation between distance to city center and price per sqm by city")
city_corr = corr_per_city(df)
st.write(city_corr)

st.header("Average price per sqm by distance from city center")
cities = df['city'].unique()
bin_width = st.slider("Select bin width for distance from city center", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
avg_price_dist = avg_price_by_dist_from_centre_bins(df, cities, bin_width)
fig, ax = plt.subplots(figsize=(10, 6))
avg_price_dist.plot(kind='bar', ax=ax)
ax.set_title("Average price per sqm by distance from city center")
ax.set_xlabel("Distance from city center (bins)")
ax.set_ylabel("Average price per sqm")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

st.write("This application provides insights into apartment prices in various cities, including trends over time, comparisons between cities, and the impact of distance from city centers on prices.")
st.write("You can interact with the data by adjusting the bin width for distance from city center, which will update the average price per sqm accordingly.")