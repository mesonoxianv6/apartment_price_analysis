import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import datetime
import statsmodels as sm
from data_analysis import (
    load_data, format_data, avg_price_by_month, avg_price_by_city,
    avg_building_age_by_city, count_21st_century_buildings,
    new_building_share_by_city, build_city_metrics,
    distance_price_corr, corr_per_city, avg_price_by_dist_from_centre_bins
)

st.set_page_config(
    page_title="Apartment Prices Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load and preprocess data
df = load_data("data/data_dropped.csv")
df = format_data(df)

st.title("Apartment Prices Dashboard")

# Average price over time
monthly = avg_price_by_month(df)
monthly_df = monthly.reset_index()
monthly_df["month"] = monthly_df["month"].dt.to_timestamp()
monthly_df = monthly_df.dropna(subset=["priceperm2"])

plt.style.use("dark_background")
sns.set_theme(style="darkgrid")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=monthly_df, x="month", y="priceperm2", marker='o', color='deepskyblue', linewidth=2, ax=ax)
ax.set_title("Average Price per m² Over Time", fontsize=16, fontweight='bold', color='white')
ax.set_xlabel("Month", fontsize=12, color='white')
ax.set_ylabel("Price per m²", fontsize=12, color='white')
ax.tick_params(axis='both', colors='white', labelsize=10)
plt.setp(ax.get_xticklabels(), rotation=45, ha='right', color='white')
plt.setp(ax.get_yticklabels(), color='white')
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#0E1117')
ax.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
st.pyplot(fig)

# Average price per city
chart_data = avg_price_by_city(df).reset_index()
chart_data.columns = ['City', 'Average Price per sqm']
chart_data = chart_data.sort_values(by='Average Price per sqm', ascending=False).round(0)
chart_data["Color"] = "lightblue"
chart_data.loc[chart_data['Average Price per sqm'] == chart_data['Average Price per sqm'].max(), 'Color'] = 'crimson'
chart_data.loc[chart_data['Average Price per sqm'] == chart_data['Average Price per sqm'].min(), 'Color'] = 'seagreen'

fig = px.bar(
    chart_data,
    x='City',
    y='Average Price per sqm',
    text='Average Price per sqm',
    color='Color',
    color_discrete_map="identity",
    title="Average Price per m² by City"
)
fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
fig.update_layout(
    xaxis_tickangle=-45,
    showlegend=False,
    yaxis_title="Average Price per m²",
    xaxis_title="City",
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# Interactive city filter
selected_city = st.selectbox("Select City", df['city'].unique())
city_df = df[df['city'] == selected_city].copy()
city_df['building_age'] = datetime.date.today().year - city_df['buildYear']

min_age, max_age = int(city_df['building_age'].min()), int(city_df['building_age'].max())
age_range = st.slider("Building Age Range", min_age, max_age, (min_age, max_age))

min_price, max_price = int(city_df['priceperm2'].min()), int(city_df['priceperm2'].max())
price_range = st.slider("Price per m² Range", min_price, max_price, (min_price, max_price))

filtered_df = city_df[
    (city_df['building_age'].between(age_range[0], age_range[1])) &
    (city_df['priceperm2'].between(price_range[0], price_range[1]))
]

fig = px.scatter(
    filtered_df,
    x='building_age',
    y='priceperm2',
    title=f"Building Age vs Price per m² – {selected_city}",
    trendline='ols'
)
fig.update_traces(marker=dict(size=6, opacity=0.6, line=dict(width=0.5, color='red')))
st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""
**Number of Listings:** {len(filtered_df)}  
**Correlation (Age vs Price):** {filtered_df['building_age'].corr(filtered_df['priceperm2']):.2f}
""")

# Anomalies in Warsaw and Krakow
st.header("City-specific Building Age Analysis")
selected_city = st.selectbox("Choose City", ["warszawa", "krakow"])

city_df = df[df['city'] == selected_city].copy()
city_df['building_age'] = datetime.date.today().year - city_df['buildYear']
city_df = city_df[city_df['building_age'].between(0, 150)]
city_df = city_df[city_df['priceperm2'].between(3000, 25000)]
city_df['age_bin'] = pd.cut(
    city_df['building_age'],
    bins=[0, 20, 40, 60, 80, 100, 200],
    labels=["0–20", "21–40", "41–60", "61–80", "81–100", "100+"]
)

fig_box = px.box(
    city_df,
    x='age_bin',
    y='priceperm2',
    title=f"Price Distribution by Building Age – {selected_city.capitalize()}",
    labels={"priceperm2": "Price per m²", "age_bin": "Building Age Group"}
)
st.plotly_chart(fig_box, use_container_width=True)

fig_hist = px.histogram(
    city_df,
    x='priceperm2',
    color='age_bin',
    barmode='overlay',
    nbins=50,
    title=f"Price Distribution by Age Group – {selected_city.capitalize()}",
    labels={"priceperm2": "Price per m²"}
)
st.plotly_chart(fig_hist, use_container_width=True)

median_table = city_df.groupby('age_bin')['priceperm2'].median().reset_index().round(0)
median_table.columns = ["Building Age Group", "Median Price per m²"]
st.dataframe(median_table)

# Ownership vs Floor heatmap
heat_data = df[df['ownership'] != 'share'].groupby(['ownership', 'floor'])['priceperm2'].mean().reset_index()
pivot = heat_data.pivot(index='ownership', columns='floor', values='priceperm2')

fig = px.imshow(
    pivot,
    text_auto=".0f",
    color_continuous_scale='plotly3',
    labels=dict(color="Avg Price per m²")
)
fig.update_layout(
    title="Average Price per m² by Ownership Type and Floor",
    xaxis_title="Floor",
    yaxis_title="Ownership"
)
st.plotly_chart(fig, use_container_width=True)

# Distance vs Price scatter with regression
correlations = {
    'warszawa': -0.480,
    'krakow': -0.546,
    'gdynia': -0.438
}

top_cities = list(correlations.keys())
subset = df[df['city'].isin(top_cities)].copy()

fig = px.scatter(
    subset,
    x='centreDistance',
    y='priceperm2',
    color='city',
    trendline='ols',
    trendline_scope='trace',
    title="Price per m² vs Distance to City Center",
    labels={
        'centreDistance': 'Distance to City Center (km)',
        'priceperm2': 'Price per m²',
        'city': 'City'
    }
)
fig.update_traces(marker=dict(size=5, opacity=0.6, line=dict(width=0.5, color='black')))
fig.update_layout(template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)

# Footer description
st.write("Explore apartment prices across Polish cities. Analyze trends over time, compare average prices by city, inspect the influence of building age and ownership, and examine spatial correlations with city centers.")
