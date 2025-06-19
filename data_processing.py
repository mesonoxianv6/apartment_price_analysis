import pandas as pd
import os
import datetime
from glob import glob


def load_data(data_folder="data"):
    files = sorted(glob(os.path.join(data_folder, "apartments_pl_*.csv")))
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["source_file"] = os.path.basename(f)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def clean_data(df):
    conveniences = ["hasBalcony", "hasElevator", "hasSecurity", "hasStorageRoom", "hasParkingSpace"]
    for col in conveniences:
        df[col] = df[col].astype(str).str.strip().str.lower() == 'yes'

    columns_to_drop = [
        'latitude', 'longitude', 'poiCount', 'schoolDistance', 'clinicDistance',
        'postOfficeDistance', 'kindergartenDistance', 'restaurantDistance',
        'collegeDistance', 'pharmacyDistance', 'condition', 'buildingMaterial', 'type'
    ]
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')
    return df

    for col in ['floor', 'floorCount', 'buildYear']:
        df[col] = df[col].fillna(df[col].median())
    return df

def add_features(df):
        year_now = datetime.date.today().year
        df['priceperm2'] = df['price'] / df['squareMeters']
        df["priceperm2"] = pd.to_numeric(df["priceperm2"], errors="coerce")
        df['building_age'] = year_now - df['buildYear']
        df['month'] = df['source_file'].str.extract(r"_(\d{4}_\d{2})")[0]
        df['month'] = pd.to_datetime(df['month'], format='%Y_%m')
        return df

def main():
    data = load_data()
    data = clean_data(data)
    data = add_features(data)
    data.to_csv("data_merged_data.csv", index=False)
    print("Dane zostały zapisane do data/merged_data.csv")

if __name__ == "__main__":
    main()
