import pandas as pd
import os
import datetime
from glob import glob

# Load multiple CSV files and combine them into a single DataFrame
def load_data(data_folder="data"):
    files = sorted(glob(os.path.join(data_folder, "apartments_pl_*.csv")))
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["source_file"] = os.path.basename(f)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

# Clean and preprocess raw apartment data
def clean_data(df):
    conveniences = ["hasBalcony", "hasElevator", "hasSecurity", "hasStorageRoom", "hasParkingSpace"]
    for col in conveniences:
        df[col] = df[col].astype(str).str.strip().str.lower() == 'yes' # Convert to boolean

    df['ownership'] = df['ownership'].astype(str).str.strip().str.lower()
    df['ownership'] = df['ownership'].replace({'udział': 'share'}) # Normalize ownership labels

    # Drop unnecessary or redundant columns
    columns_to_drop = [
        'latitude', 'longitude', 'poiCount', 'schoolDistance', 'clinicDistance',
        'postOfficeDistance', 'kindergartenDistance', 'restaurantDistance',
        'collegeDistance', 'pharmacyDistance', 'condition', 'buildingMaterial', 'type'
    ]
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Remove rows with missing essential values
    df = df.dropna(subset=['floor', 'floorCount', 'buildYear',])
    return df

# Add derived features for further analysis
def add_features(df):
        year_now = datetime.date.today().year
        df['priceperm2'] = df['price'] / df['squareMeters']
        df["priceperm2"] = pd.to_numeric(df["priceperm2"], errors="coerce")
        df['building_age'] = year_now - df['buildYear']

        # Extract month from filename and convert to datetime
        df['month'] = df['source_file'].str.extract(r"_(\d{4}_\d{2})")[0]
        df['month'] = pd.to_datetime(df['month'], format='%Y_%m')

        # Calculate relative floor height (low/medium/high
        rel = (df['floor'] - 1)/ (df['floorCount'] - 1)
        rel = rel.where(pd.notnull(rel) & (df['floorCount'] > 1), 0.0)
        df['floor_rel'] = pd.cut(rel, bins=[-1, 0.33, 0.66, 1.0], labels=['low', 'medium', 'high']).astype(str)
        return df

# Main pipeline: load, clean, add features, and save the final dataset
def main():
    data = load_data()
    data = clean_data(data)
    data = add_features(data)
    data.to_csv("data/data_dropped.csv", index=False)
    print("Dane zostały zapisane do data_dropped.csv")

if __name__ == "__main__":
    main()
