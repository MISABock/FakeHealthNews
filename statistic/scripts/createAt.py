import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
import numpy as np

# Datei einlesen
file_path = "C:/Users/micha/OneDrive/Desktop/Development/ZHAW/statistic/createdAt.json"
df = pd.read_json(file_path)

# "author_created_at" in datetime umwandeln und Zeitzone entfernen
df["author_created_at"] = pd.to_datetime(df["author_created_at"]).dt.tz_localize(None)

# Aktuelles Datum (ohne Zeitzone)
current_date = datetime.now()

# Alter der Accounts berechnen (in Jahren)
df["account_age_years"] = df["author_created_at"].apply(lambda x: (current_date - x).days / 365.25)

# Daten in "fake" und "real" aufteilen
fake_accounts = df[df["tweet_fact_check"] == "fake"]["account_age_years"]
real_accounts = df[df["tweet_fact_check"] == "real"]["account_age_years"]

# Stichprobengrößen und Gesamtgröße
fake_count = len(fake_accounts)
real_count = len(real_accounts)
total_count = fake_count + real_count
print(f"\nStichprobengröße:")
print(f"Fake-News Accounts: {fake_count}")
print(f"Real-News Accounts: {real_count}")
print(f"Gesamtgröße: {total_count}")

# Deskriptive Statistik
print("\nDeskriptive Statistik:")
print(f"Fake-News Accounts: Mittelwert: {fake_accounts.mean():.2f}, Median: {fake_accounts.median():.2f}")
print(f"Real-News Accounts: Mittelwert: {real_accounts.mean():.2f}, Median: {real_accounts.median():.2f}")

# Interquartilsabstand (IQR) und Ausreißer analysieren
def analyze_outliers(data, label):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    print(f"{label} Accounts: Q1: {q1:.2f}, Q3: {q3:.2f}, IQR: {iqr:.2f}")
    print(f"{label} Accounts: Untere Grenze: {lower_bound:.2f}, Obere Grenze: {upper_bound:.2f}")
    print(f"{label} Accounts: Ausreißer: {len(outliers)}, Werte: {outliers}\n")
    
analyze_outliers(fake_accounts, "Fake-News")
analyze_outliers(real_accounts, "Real-News")

# Statistischer Test: Mann-Whitney-U-Test
u_stat, p_value = mannwhitneyu(fake_accounts, real_accounts, alternative="two-sided")
print("\nMann-Whitney-U-Test:")
print(f"U-Statistik: {u_stat:.2f}, P-Wert: {p_value:.4f}")

# Interpretation
if p_value < 0.05:
    print("Ergebnis: Es gibt einen signifikanten Unterschied im Alter der Accounts zwischen Fake-News- und Real-News-Tweets.")
else:
    print("Ergebnis: Es gibt keinen signifikanten Unterschied im Alter der Accounts zwischen Fake-News- und Real-News-Tweets.")

# Visualisierung: Boxplot
plt.figure(figsize=(10, 6))
plt.boxplot([fake_accounts, real_accounts], labels=["Fake-News", "Real-News"], patch_artist=True)
plt.title("Boxplot des Account-Alters für Fake-News und Real-News")
plt.ylabel("Alter in Jahren")
plt.grid()
plt.show()

# Visualisierung: Histogramm
plt.figure(figsize=(10, 6))
plt.hist(fake_accounts, bins=15, alpha=0.5, label="Fake-News", color="red", edgecolor="black")
plt.hist(real_accounts, bins=15, alpha=0.5, label="Real-News", color="blue", edgecolor="black")
plt.title("Histogramm des Account-Alters für Fake-News und Real-News")
plt.xlabel("Alter in Jahren")
plt.ylabel("Anzahl Accounts")
plt.legend()
plt.grid()
plt.show()
