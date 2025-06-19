import pandas as pd
import os
import datetime
from glob import glob

def load_raw_data(folder="data"):
    files = sorted(glob(os.path.join(folder, "apartments_pl_*.csv")))
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["source_file"] = os.path.basename(f)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def prepare_data(df):
    df = df.dropna(subset=['floor', 'floorCount', 'buildYear'])
    df['priceperm2'] = df['price'] / df['squareMeters']
    df['month'] = df['source_file'].str.extract(r"_(\d{4}_\d{2})")[0]
    df['month'] = pd.to_datetime(df['month'], format='%Y_%m')
    df['building_age'] = datetime.date.today().year - df['buildYear']
    conveniences = ["hasBalcony", "hasElevator", "hasSecurity", "hasStorageRoom", "hasParkingSpace"]
    for col in conveniences:
        df[col] = df[col].astype(str).str.strip().str.lower() == 'yes'
    return df

def main():
    data = load_raw_data()
    data = prepare_data(data)
    data.to_csv("data/data_dropped.csv", index=False)
    print("✅ data_dropped.csv zapisany poprawnie z usuniętymi brakami.")

if __name__ == "__main__":
    main()
