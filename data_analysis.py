import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv("data/data_dropped.csv")
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['month'] = pd.to_datetime(df['month'], format='%Y-%m-%d', errors='coerce')
    df['priceperm2'] = pd.to_numeric(df['priceperm2'], errors='coerce')
    return df

def city_counts(df: pd.DataFrame) -> pd.Series:
    return df['city'].value_counts()

def avg_price_by_month(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(df['month'].dt.to_period('M'))['priceperm2'].mean().sort_index()

def avg_price_by_city(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('city')['priceperm2'].mean().sort_values(ascending = False)

def avg_building_age_by_city(df):
    return df.groupby('city')['building_age'].mean().sort_values()

def count_21st_century_buildings(df: pd.DataFrame) -> pd.Series:
    df_21 = df[df['buildYear'] <=2001]
    return df_21.groupby('city')['buildYear'].count().sort_values(ascending = False)

def new_building_share_by_city(df: pd.DataFrame) -> pd.Series:
    total = city_counts(df)
    counts21 = count_21st_century_buildings(df)
    share = counts21 / total
    return share.sort_values()

def build_city_metrics(df: pd.DataFrame) -> pd.DataFrame:
    total = city_counts(df)
    counts21 = count_21st_century_buildings(df)
    share = counts21 / total
    price = avg_price_by_city(df)

    dfm = pd.DataFrame({
        'total': total,
        'counts21': counts21,
        'share': share,
        'price': price
    })
    return dfm.dropna()

def distance_price_corr(df: pd.DataFrame) -> float:
    dist = df['centreDistance']
    price = df['priceperm2']
    return dist.corr(price)

def corr_per_city(df: pd.DataFrame):
    out = {}
    for city, group in df.groupby('city'):
        out[city] = group['centreDistance'].corr(group['priceperm2'])
    return pd.Series(out).sort_values(ascending=False)

def avg_price_by_dist_from_centre_bins(df: pd.DataFrame, cities: list[str], bin_width: float = 1.0) -> pd.DataFrame:
    df_sel = df[df['city'].isin(cities)].copy()
    maxd = df_sel['centreDistance'].max()
    bins = np.arange(0, maxd + bin_width, bin_width)
    df_sel['dist_bin'] = pd.cut(df_sel['centreDistance'], bins, right=False)
    result = (
        df_sel.groupby(['city', 'dist_bin'])['priceperm2'].mean().unstack('city')
    )
    return result

if __name__ == "__main__":
    df = load_data(("data/data_dropped.csv"))
    df = preprocess_data(df)

    monthly = avg_price_by_month(df)
    print("Średnia cena za m² wg miesiąca:")
    print(monthly)

    by_city = avg_price_by_city(df)
    print("\n Średnia cena za m² wg miasta:")
    print(by_city.head(15))

    by_age = avg_building_age_by_city(df)
    print("\n Średni wiek budynku w poszczególnych miastach:")
    print(by_age)

    counts21 = count_21st_century_buildings(df)
    print("\n Liczba mieszkań wybudowanych po 2001 roku wg miast:")
    print(counts21)

    share21 = new_building_share_by_city(df)
    print("\n Udział nowych mieszkań w miastach:")
    print(share21)

    city_metrics = build_city_metrics(df)
    print("\n Metryki miast:")
    print(city_metrics)

    corr = city_metrics['share'].corr(city_metrics['price'])
    print(f"\n Korelacja udziału nowych mieszkań vs średnia cena: {corr:.3f}")

    corr_dist = distance_price_corr(df)
    print(f"\n Korelacja distance vs price: {corr_dist:.3f}")

    print("\n Korelacja distance vs price w poszczególnych miastach:")
    print(corr_per_city(df))

    cities_to_analyze = ['krakow', 'warszawa', 'lodz', 'szczecin']
    dist_price_bins = avg_price_by_dist_from_centre_bins(df, cities=cities_to_analyze, bin_width=1.0)
    print("\n Średnia cena za m² w 1-km binach odległości (top miasta):")
    print(dist_price_bins)
