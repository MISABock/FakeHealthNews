import pandas as pd

# Datei laden und in ein DataFrame umwandeln
file_path = "C:/Users/micha/OneDrive/Desktop/Development/ZHAW/statistic/retweetFactChecklikeCount.json"
df = pd.read_json(file_path)

# Verschachtelte Daten extrahieren
df = pd.json_normalize(df["tweet"])

# Überprüfen, ob `fact_check` nur "real" oder "fake" enthält
valid_values = ["real", "fake"]
df = df[df["fact_check"].isin(valid_values)]

# Statistikwerte berechnen
minimum = df["retweet_count"].min()
maximum = df["retweet_count"].max()
q1 = df["retweet_count"].quantile(0.25)
median = df["retweet_count"].median()
q3 = df["retweet_count"].quantile(0.75)
percentile_90 = df["retweet_count"].quantile(0.90)
percentile_95 = df["retweet_count"].quantile(0.95)
percentile_98 = df["retweet_count"].quantile(0.98)

# Werte in der Konsole ausgeben
print("Statistik der Retweet-Werte:")
print(f"Minimum: {minimum}")
print(f"Q1 (25%): {q1}")
print(f"Median (50%): {median}")
print(f"Q3 (75%): {q3}")
print(f"Maximum: {maximum}")
print(f"90. Perzentil: {percentile_90}")
print(f"95. Perzentil: {percentile_95}")
print(f"98. Perzentil: {percentile_98}")
