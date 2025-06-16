import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data/merged_data.csv")

from data_processing import data

# data['month'] = pd.to_datetime(data['month'], format = "%Y_%m")
# avg_price_by_month = data.groupby("month")['priceperm2'].mean().sort_index()
# avg_price_by_month.index = avg_price_by_month.index.strftime('%Y-%m')

# avg_price_by_month.plot(kind="bar", title="Średnia cena za m² wg miesiąca")
# plt.xlabel("Miesiąc")
# plt.ylabel("Cena za m²")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# avg_price_by_city = data.groupby('city')['priceperm2'].mean().sort_values(ascending=False)

# avg_price_by_city.plot(kind='bar', title='Średnia cena za m² w miastach')
# plt.xlabel("Miasto")
# plt.ylabel("Cena za m²")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

conveniences = ["hasBalcony", "hasElevator", "hasParkingSpace", "hasSecurity", "hasStorageRoom"]
# data["feature_score"] = data[conveniences].astype(int).sum(axis=1)
# feature_score_grouped = data.groupby("feature_score")["priceperm2"].mean()

# feature_score_grouped.plot(kind='bar', title='Udogodnienia vs cena za m2')
# plt.xlabel("Liczba udogodnień")
# plt.ylabel("Cena za m²")
# plt.xticks(rotation=0)
# plt.tight_layout()
# plt.show()

results = {}

# for col in conveniences:
#     mean_true = data[data[col] == True]["priceperm2"].mean()
#     mean_false = data[data[col] == False]["priceperm2"].mean()
#     results[col] = {"Tak": mean_true, "Nie": mean_false}

# df_results = pd.DataFrame(results).T  # T → transpozycja
# print(df_results)

# df_results.plot(kind="bar", title="Średnia cena za m² – z i bez udogodnienia")
# plt.xlabel("Udogodnienie")
# plt.ylabel("Cena za m²")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# for col in conveniences:
#     true_pct = data[col].mean() * 100
#     false_pct = 100 - true_pct
#     print(f"{col}: Tak = {true_pct:.2f}%, Nie = {false_pct:.2f}%")

print(data.shape)
print(data["hasBalcony"].value_counts(dropna=False))


