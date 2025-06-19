import os
import pandas as pd
import matplotlib.pyplot as plt

conveniences = ["hasBalcony", "hasElevator", "hasSecurity", "hasStorageRoom", "hasParkingSpace"]

def load_and_prepare():
    df_filled = pd.read_csv("data/merged_data.csv")
    df_dropped = pd.read_csv("data/data_dropped.csv")

    for df in (df_filled, df_dropped):
        df["month"] = pd.to_datetime(df["month"], format="%Y-%m-%d")
        df["priceperm2"] = pd.to_numeric(df["priceperm2"], errors="coerce")
    return df_filled, df_dropped

def calculate_monthly_avg(df):
    result = df.groupby("month")["priceperm2"].mean().sort_index()
    result.index = result.index.strftime("%Y-%m-%d")
    return result

def calculate_convenience_share(df, columns):
    return {
        col: round(df[col].eq(True).mean() * 100, 2)
        for col in columns
    }

def plot_price_comparison(avg_filled, avg_dropped):
    plt.figure(figsize=(10, 6))
    plt.plot(avg_filled, marker='o', label='Uzupełnione medianą (fillna)')
    plt.plot(avg_dropped, marker='o', label='Usunięte braki (dropna)')
    plt.title("Porównanie średniej ceny za m² – fillna vs dropna")
    plt.xlabel("Miesiąc")
    plt.ylabel("Średnia cena za m²")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_comparison_table(filled, dropped, columns):
    filled_pct = calculate_convenience_share(filled, columns)
    dropped_pct = calculate_convenience_share(dropped, columns)

    df_compare = pd.DataFrame({
        "Uzupełnione medianą": filled_pct,
        "Usunięte braki": dropped_pct
    })

    print("\n📊 Udział mieszkań z udogodnieniem (%):")
    print(df_compare)

def main():
    filled, dropped = load_and_prepare()
    avg_filled = calculate_monthly_avg(filled)
    avg_dropped = calculate_monthly_avg(dropped)

    print("\n📈 Średnia cena za m² (fillna):")
    print(avg_filled)

    print("\n📉 Średnia cena za m² (dropna):")
    print(avg_dropped)

    plot_price_comparison(avg_filled, avg_dropped)
    show_comparison_table(filled, dropped, conveniences)

if __name__ == "__main__":
    main()
