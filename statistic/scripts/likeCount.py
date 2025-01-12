import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# Daten laden
file_path = "C:/Users/micha/OneDrive/Desktop/Development/ZHAW/statistic/FollowersAndTweetCountOfAllTweetsRealAndFake.json"
df = pd.read_json(file_path)

# Verschachtelte Daten extrahieren
df = pd.json_normalize(df["tweet"])

# Spalten überprüfen und NaN-Werte entfernen
df = df.dropna(subset=["retweet_count", "fact_check"])

# Zielvariable binär kodieren: "real" -> 1, "fake" -> 0
df["fact_check_numeric"] = df["fact_check"].apply(lambda x: 1 if x == "real" else 0)

# Tweets mit RetweetCount > 0 filtern
filtered_df = df[df["retweet_count"] > 0]

# Anzahl der verbleibenden Tweets
data_count = len(filtered_df)
print(f"Anzahl der für die Analyse berücksichtigten Tweets: {data_count}")

# Features und Zielvariable definieren
X = filtered_df[["retweet_count"]].values
y = filtered_df["fact_check_numeric"].values

# Logistische Regression trainieren
log_reg = LogisticRegression()
log_reg.fit(X, y)

# Ergebnisse der logistischen Regression
intercept = log_reg.intercept_[0]
coefficient = log_reg.coef_[0][0]
print(f"Logistische Regression:\nIntercept: {intercept}\nCoefficient: {coefficient}")

# Wahrscheinlichkeiten für den Plot berechnen
X_plot = np.linspace(filtered_df["retweet_count"].min(), filtered_df["retweet_count"].max(), 300).reshape(-1, 1)
y_prob = log_reg.predict_proba(X_plot)[:, 1]

# Boxplot-Daten für RetweetCount
retweet_counts_fake = filtered_df[filtered_df["fact_check"] == "fake"]["retweet_count"]
retweet_counts_real = filtered_df[filtered_df["fact_check"] == "real"]["retweet_count"]

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

fake_stats = get_boxplot_stats(retweet_counts_fake)
real_stats = get_boxplot_stats(retweet_counts_real)

print("\nBoxplot-Werte für Fake-Tweets:")
for key, value in fake_stats.items():
    print(f"{key}: {value}")

print("\nBoxplot-Werte für Real-Tweets:")
for key, value in real_stats.items():
    print(f"{key}: {value}")

# Plot erstellen
plt.figure(figsize=(10, 6))
plt.scatter(filtered_df["retweet_count"], filtered_df["fact_check_numeric"], alpha=0.3, label="Datenpunkte", color="gray")
plt.plot(X_plot, y_prob, color="blue", label="Logistische Regression")
plt.title("Logistische Regression: Wahrscheinlichkeit 'real' vs. RetweetCount (gefiltert)")
plt.xlabel("RetweetCount")
plt.ylabel("Wahrscheinlichkeit 'real'")
plt.legend()
plt.grid()
plt.show()
