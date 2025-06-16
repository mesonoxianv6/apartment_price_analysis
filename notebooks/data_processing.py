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

data['hasBalcony'] = data['hasBalcony'].str.lower() == 'yes'
data['hasElevator'] = data['hasElevator'].str.lower() == 'yes'
data['hasSecurity'] = data['hasSecurity'].str.lower() == 'yes'
data['hasStorageRoom'] = data['hasStorageRoom'].str.lower() == 'yes'
data['hasParkingSpace'] = data['hasParkingSpace'].str.lower() == 'yes'

columns_to_drop = [
    'latitude', 'longitude', 'poiCount', 'schoolDistance', 'clinicDistance', 'postOfficeDistance', 'kindergartenDistance', 'restaurantDistance', 'collegeDistance', 'pharmacyDistance', 'condition', 'buildingMaterial', 'type'
]
data.drop(columns=columns_to_drop, axis=1, inplace=True)

for col in ['floor', 'floorCount', 'buildYear']:
    data[col] = data[col].fillna(data[col].median())

data['priceperm2'] = data['price'] / data['squareMeters']
data['building_age'] = rok - data['buildYear']
data['month'] = data['source_file'].str.split('_').str[2] + '_' + \
                data['source_file'].str.split('_').str[3].str.replace('.csv', '')


# print(data.head())
# print(data.info())
# print(data.columns)
data.to_csv("data/merged_data.csv", index=False)
# print(data.isnull().sum().sort_values(ascending=False))
# print(data[['floor','floorCount', 'building_age' ]].median())
