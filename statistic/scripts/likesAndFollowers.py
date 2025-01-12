import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt

# Datei einlesen
file_path = "C:/Users/micha/OneDrive/Desktop/Development/ZHAW/statistic/Data/likeAndFollowers.json"
data = pd.read_json(file_path)

# Like-to-Follower-Verhältnis berechnen
data["like_to_follower_ratio"] = data["like_count"] / data["followers_count"]

# Entfernen von NaN-Werten und Filtern auf mindestens 1 Like und 1 Follower
data = data.dropna(subset=["like_to_follower_ratio", "fact_check"])
data = data[(data["like_count"] > 0) & (data["followers_count"] > 0)]

# Debugging: Werte überprüfen
print("\nÜberprüfung der ersten Zeilen der gefilterten Daten:")
print(data[["like_count", "followers_count", "like_to_follower_ratio"]].head())

# Debugging: Werte mit Verhältnis <= 0 prüfen
invalid_ratios = data[data["like_to_follower_ratio"] <= 0]
if not invalid_ratios.empty:
    print("\nDatensätze mit ungültigem Verhältnis (<= 0):")
    print(invalid_ratios[["like_count", "followers_count", "like_to_follower_ratio"]])

# Aufteilen nach "fact_check"
fake_data = data[data["fact_check"] == "fake"]
real_data = data[data["fact_check"] == "real"]

# Werte extrahieren
ratio_fake = fake_data["like_to_follower_ratio"]
ratio_real = real_data["like_to_follower_ratio"]

# Deskriptive Statistik
fake_mean = ratio_fake.mean()
fake_std = ratio_fake.std()
real_mean = ratio_real.mean()
real_std = ratio_real.std()

print("\nDeskriptive Statistik für Like-to-Follower-Verhältnis:")
print(f"\nFake-News: Mittelwert = {fake_mean:.4f}, Standardabweichung = {fake_std:.4f}")
print(f"Real-News: Mittelwert = {real_mean:.4f}, Standardabweichung = {real_std:.4f}")

# Mann-Whitney-U-Test
u_stat, p_value = mannwhitneyu(ratio_fake, ratio_real, alternative="two-sided")
print("\nMann-Whitney-U-Test für Like-to-Follower-Verhältnis:")
print(f"U-Statistik: {u_stat:.2f}")
print(f"p-Wert: {p_value:.4f}")

# Anzahl der Tweets, die die Bedingung erfüllen
anzahl_tweets = data.shape[0]
print(f"Anzahl der berücksichtigten Tweets: {anzahl_tweets}")

# Balkendiagramm erstellen
labels = ["Fake-News", "Real-News"]
means = [fake_mean, real_mean]
errors = [fake_std, real_std]

plt.figure(figsize=(10, 6))
plt.bar(labels, means, yerr=errors, color=["lightcoral", "lightgreen"], capsize=10, alpha=0.7, edgecolor="black")
plt.title("Durchschnittliches Like-to-Follower-Verhältnis")
plt.ylabel("Durchschnittliches Like-to-Follower-Verhältnis")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
