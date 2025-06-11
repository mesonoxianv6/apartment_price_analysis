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
aktualny_data = datetime.date.today()
rok = aktualny_data.year



data['hasBalcony'] = data['hasBalcony'] == 'True'
data['hasElevator'] = data['hasElevator'] == 'True'
data['hasSecurity'] = data['hasSecurity'] == 'True'
data['hasStorageRoom'] = data['hasStorageRoom'] == 'True'
data['hasParkingSpace'] = data['hasParkingSpace'] == 'True'

columns_to_drop = [
    'latitude', 'longitude', 'poiCount', 'schoolDistance', 'clinicDistance', 'postOfficeDistance', 'kindergartenDistance', 'restaurantDistance', 'collegeDistance', 'pharmacyDistance'
]
data.drop(columns=columns_to_drop, axis=1, inplace=True)

data['priceperm2'] = data['price'] / data['squareMeters']
data['building_age'] = rok - data['buildYear']
data['month'] = data['source_file'].str.split('_').str[2] + '_' + \
                data['source_file'].str.split('_').str[3].str.replace('.csv', '')
print(data['month'])


pd.set_option('display.max_columns', None)
print(data.head())
# print(data.info())
# print(data.columns)
