import pandas as pd
import matplotlib.pyplot as plt

# 1. Wczytanie danych
data_filled = pd.read_csv("data/merged_data.csv")
data_dropped = pd.read_csv("data/data_dropped.csv")

# 2. Konwersja kolumny 'month' na datetime
for df in [data_filled, data_dropped]:
    df["month"] = pd.to_datetime(df["month"], format="%Y_%m")

# 3. Konwersja udogodnień na bool
conveniences = ["hasBalcony", "hasElevator", "hasSecurity", "hasStorageRoom", "hasParkingSpace"]

for col in conveniences:
    data_dropped[col] = data_dropped[col].astype(str).str.strip().str.lower() == 'yes'

# 4. Obliczenie średniej ceny za m² wg miesiąca
avg_price_by_month_filled = data_filled.groupby("month")["priceperm2"].mean().sort_index()
avg_price_by_month_dropped = data_dropped.groupby("month")["priceperm2"].mean().sort_index()

# 5. Formatowanie indeksu na YYYY-MM
avg_price_by_month_filled.index = avg_price_by_month_filled.index.strftime("%Y-%m")
avg_price_by_month_dropped.index = avg_price_by_month_dropped.index.strftime("%Y-%m")

# 6. Wydrukowanie wyników do porównania
print("📊 Średnia cena za m² (UZUPEŁNIONE DANE – fillna):")
print(avg_price_by_month_filled)

print("\n📉 Średnia cena za m² (USUNIĘTE BRAKI – dropna):")
print(avg_price_by_month_dropped)

# 7. Wykres porównawczy
# plt.figure(figsize=(10, 6))
# plt.plot(avg_price_by_month_filled, marker='o', label='Uzupełnione medianą (fillna)')
# plt.plot(avg_price_by_month_dropped, marker='o', label='Usunięte braki (dropna)')

# plt.title("Porównanie średniej ceny za m² – fillna vs dropna")
# plt.xlabel("Miesiąc")
# plt.ylabel("Średnia cena za m²")
# plt.legend()
# plt.grid(True)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# 7. Porównanie udziału udogodnień (True/False) w obu zbiorach

def oblicz_udzial(df, kolumny):
    wyniki = {}
    for col in kolumny:
        true_pct = df[col].mean() * 100  # bo True = 1, False = 0
        wyniki[col] = round(true_pct, 2)
    return wyniki

# Obliczenie udziałów
udzial_filled = oblicz_udzial(data_filled, conveniences)
udzial_dropped = oblicz_udzial(data_dropped, conveniences)

# Tabela porównawcza
df_udogodnienia = pd.DataFrame({
    "Uzupełnione (fillna)": udzial_filled,
    "Usunięte braki (dropna)": udzial_dropped
})

# 8. Wyświetlenie wyników
print("\n📊 Udział mieszkań z udogodnieniem (%):")
print(df_udogodnienia)

