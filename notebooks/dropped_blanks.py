import pandas as pd
import os
import datetime

files = [
    "apartments_pl_2023_09.csv",
    "apartments_pl_2023_12.csv",
    "apartments_pl_2024_03.csv",
    "apartments_pl_2024_06.csv"
]

dfs = []
for f in files:
    path = os.path.join("data", f)
    df = pd.read_csv(path)
    df["source_file"] = f
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)

# Obliczenia bazowe (bez czyszczenia):
rok = datetime.date.today().year
data['priceperm2'] = data['price'] / data['squareMeters']
data['month'] = data['source_file'].str.split('_').str[2] + '_' + data['source_file'].str.split('_').str[3].str.replace('.csv', '')

# Zostawiamy tylko wiersze z pełnymi danymi w istotnych kolumnach:
columns_istotne = ['floor', 'floorCount', 'buildYear']
data = data.dropna(subset=columns_istotne)

data['building_age'] = rok - data['buildYear']

# Zapis do pliku
data.to_csv("data/data_dropped.csv", index=False)

data['month'] = pd.to_datetime(data['month'], format = "%Y_%m")
avg_price_by_month = data.groupby("month")['priceperm2'].mean().sort_index()
avg_price_by_month.index = avg_price_by_month.index.strftime('%Y-%m')
print(avg_price_by_month)

