import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load processed data from CSV
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv("data/data_dropped.csv")
    return df

# Ensure proper data types for key columns
def format_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['month'] = pd.to_datetime(df['month'], format='%Y-%m-%d', errors='coerce')
    df['priceperm2'] = pd.to_numeric(df['priceperm2'], errors='coerce')
    return df

# Count number of listings per city
def city_counts(df: pd.DataFrame) -> pd.Series:
    return df['city'].value_counts()

# Calculate average price per sqm by month
def avg_price_by_month(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(df['month'].dt.to_period('M'))['priceperm2'].mean().sort_index()

# Calculate average price per sqm by city
def avg_price_by_city(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('city')['priceperm2'].mean().sort_values(ascending=False)

# Calculate average building age by city
def avg_building_age_by_city(df):
    return df.groupby('city')['building_age'].mean().sort_values()

# Count buildings constructed before or in 2001
def count_21st_century_buildings(df: pd.DataFrame) -> pd.Series:
    df_21 = df[df['buildYear'] <= 2001]
    return df_21.groupby('city')['buildYear'].count().sort_values(ascending=False)

# Calculate share of older buildings (built ≤ 2001) by city
def new_building_share_by_city(df: pd.DataFrame) -> pd.Series:
    total = city_counts(df)
    counts21 = count_21st_century_buildings(df)
    share = counts21 / total
    return share.sort_values()

# Compile multiple city-level metrics into a DataFrame
def build_city_metrics(df: pd.DataFrame) -> pd.DataFrame:
    total = city_counts(df)
    counts21 = count_21st_century_buildings(df)
    share = counts21 / total
    price = avg_price_by_city(df)
    building_age = avg_building_age_by_city(df)
    priceperm2 = df.groupby('city')['priceperm2'].mean()

    dfm = pd.DataFrame({
        'total': total,
        'counts21': counts21,
        'share': share,
        'priceperm2': priceperm2,
        'building_age': building_age,
        'price': price
    })
    return dfm.dropna()

# Calculate correlation between distance from city center and price
def distance_price_corr(df: pd.DataFrame) -> float:
    dist = df['centreDistance']
    price = df['priceperm2']
    return dist.corr(price)

# Compute correlation (distance vs. price) per city
def corr_per_city(df: pd.DataFrame):
    out = {}
    for city, group in df.groupby('city'):
        out[city] = group['centreDistance'].corr(group['priceperm2'])
    return pd.Series(out).sort_values(ascending=False)

# Calculate average price per sqm in bins of distance from city center
def avg_price_by_dist_from_centre_bins(df: pd.DataFrame, cities: list[str], bin_width: float = 1.0) -> pd.DataFrame:
    df_sel = df[df['city'].isin(cities)].copy()
    maxd = df_sel['centreDistance'].max()
    bins = np.arange(0, maxd + bin_width, bin_width)
    df_sel['dist_bin'] = pd.cut(df_sel['centreDistance'], bins, right=False)
    result = (
        df_sel.groupby(['city', 'dist_bin'])['priceperm2'].mean().unstack('city')
    )
    return result

# Calculate average price per sqm by ownership type
def avg_price_by_ownership(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('ownership')['priceperm2'].mean().sort_values(ascending=False)

# Calculate average price per sqm by relative floor level
def avg_price_by_floor(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('floor_rel')['priceperm2'].mean().sort_values(ascending=False)

# Run all key analytics and print results to the console
def main():
    df = load_data("data/data_dropped.csv")
    df = format_data(df)

    monthly = avg_price_by_month(df)
    print("Average price per sqm by month:")
    print(monthly)

    by_city = avg_price_by_city(df)
    print("\nAverage price per sqm by city:")
    print(by_city.head(15))

    by_age = avg_building_age_by_city(df)
    print("\nAverage building age by city:")
    print(by_age)

    counts21 = count_21st_century_buildings(df)
    print("\nNumber of buildings built ≤ 2001 by city:")
    print(counts21)

    share21 = new_building_share_by_city(df)
    print("\nShare of older buildings by city:")
    print(share21)

    city_metrics = build_city_metrics(df)
    print("\nCity-level metrics:")
    print(city_metrics)

    corr = city_metrics['share'].corr(city_metrics['price'])
    print(f"\nCorrelation (older building share vs average price): {corr:.3f}")

    corr_dist = distance_price_corr(df)
    print(f"\nCorrelation (distance to center vs price): {corr_dist:.3f}")

    print("\nCorrelation per city (distance vs price):")
    print(corr_per_city(df))

    cities_to_analyze = ['krakow', 'warszawa', 'lodz', 'szczecin']
    dist_price_bins = avg_price_by_dist_from_centre_bins(df, cities=cities_to_analyze, bin_width=1.0)
    print("\nAverage price per sqm by 1-km distance bins (selected cities):")
    print(dist_price_bins)

    ownership_avg = avg_price_by_ownership(df)
    print("\nAverage price per sqm by ownership type:")
    print(ownership_avg)

    floor_avg = avg_price_by_floor(df)
    print("\nAverage price per sqm by floor level:")
    print(floor_avg)

if __name__ == "__main__":
    main()
