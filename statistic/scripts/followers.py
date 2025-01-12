import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import json

# Dateipfad
file_path = "C:/Users/micha/OneDrive/Desktop/Development/ZHAW/statistic/Followers.json"

# Gesamte JSON-Datei als Liste von Objekten laden
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 'rowData'-Einträge extrahieren
entries = [entry["rowData"] for entry in data if "rowData" in entry]

# DataFrame aus der Liste der rowData-Objekte erstellen
df = pd.DataFrame(entries)

# NaN-Werte und ungültige Einträge entfernen
df = df.dropna(subset=["FollowersCount", "FactCheck"])
df = df[df["FactCheck"].isin(["real", "fake"])]

# 90%-Perzentil für Fake- und Real-Tweets berechnen
followers_fake = df[df["FactCheck"] == "fake"]["FollowersCount"]
followers_real = df[df["FactCheck"] == "real"]["FollowersCount"]

fake_90_percentile = followers_fake.quantile(0.9)
real_90_percentile = followers_real.quantile(0.9)

# Maximalen 90%-Perzentilwert für Filterung verwenden
max_90_percentile = max(fake_90_percentile, real_90_percentile)

# Filterung auf Basis des 90%-Perzentils
df_filtered = df[df["FollowersCount"] <= max_90_percentile]

# Zielvariable binär kodieren: "real" -> 1, "fake" -> 0
df_filtered["FactCheck_numeric"] = df_filtered["FactCheck"].apply(lambda x: 1 if x == "real" else 0)

# Features und Zielvariable definieren
X = df_filtered[["FollowersCount"]].values
y = df_filtered["FactCheck_numeric"].values

# Logistische Regression trainieren
log_reg = LogisticRegression()
log_reg.fit(X, y)

# Ergebnisse der logistischen Regression
intercept = log_reg.intercept_[0]
coefficient = log_reg.coef_[0][0]
print(f"Logistische Regression nach Filtern:\nIntercept: {intercept}\nCoefficient: {coefficient}")

# Wahrscheinlichkeiten für den Plot berechnen
X_plot = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)
y_prob = log_reg.predict_proba(X_plot)[:, 1]

# Boxplot-Daten nach der Filterung
followers_fake_filtered = df_filtered[df_filtered["FactCheck"] == "fake"]["FollowersCount"]
followers_real_filtered = df_filtered[df_filtered["FactCheck"] == "real"]["FollowersCount"]

def get_boxplot_stats(data):
    stats = {
        "Minimum": data.min(),
        "1. Quartil": data.quantile(0.25),
        "Median": data.median(),
        "3. Quartil": data.quantile(0.75),
        "90%": data.quantile(0.9),
        "95%": data.quantile(0.95),
        "Maximum": data.max(),
    }
    return stats

fake_stats = get_boxplot_stats(followers_fake_filtered)
real_stats = get_boxplot_stats(followers_real_filtered)

print("\nBoxplot-Werte für Fake-Tweets:")
for key, value in fake_stats.items():
    print(f"{key}: {value}")

print("\nBoxplot-Werte für Real-Tweets:")
for key, value in real_stats.items():
    print(f"{key}: {value}")

# Anzahl der Tweets nach der Filterung
total_tweets_filtered = len(df_filtered)
print(f"\nGesamte Anzahl der berücksichtigten Tweets nach Filterung: {total_tweets_filtered}")

# Plot erstellen
plt.figure(figsize=(10, 6))
plt.scatter(df_filtered["FollowersCount"], df_filtered["FactCheck_numeric"], alpha=0.3, label="Datenpunkte", color="gray")
plt.plot(X_plot, y_prob, color="blue", label="Logistische Regression")
plt.title("Logistische Regression: Wahrscheinlichkeit 'real' vs. FollowersCount (gefiltert)")
plt.xlabel("FollowersCount")
plt.ylabel("Wahrscheinlichkeit 'real'")
plt.legend()
plt.grid()
plt.show()
