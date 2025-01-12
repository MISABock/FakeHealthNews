import pandas as pd
import matplotlib.pyplot as plt
import json
import scipy.stats as stats

# Pfad zur JSON-Datei
file_path = "C:/Users/micha/OneDrive/Desktop/Development/ZHAW/statistic/Followers.json"

# JSON-Datei laden und DataFrame erstellen
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = [entry["rowData"] for entry in data if "rowData" in entry]
df = pd.DataFrame(entries)

# Gruppen für Fake- und Real-Tweets definieren
followers_fake = df[df["FactCheck"] == "fake"]["FollowersCount"]
followers_real = df[df["FactCheck"] == "real"]["FollowersCount"]

# Histogramme erstellen
plt.figure(figsize=(10, 6))
plt.hist(followers_fake, bins=50, alpha=0.5, label='Fake')
plt.hist(followers_real, bins=50, alpha=0.5, label='Real')
plt.legend()
plt.title("Histogramm der Follower-Anzahlen")
plt.xlabel("Anzahl der Follower")
plt.ylabel("Häufigkeit")
plt.show()

# Optional: Q-Q-Plots zur Überprüfung der Normalverteilung
plt.figure(figsize=(6, 6))
stats.probplot(followers_fake, dist="norm", plot=plt)
plt.title("Q-Q-Plot für Fake-Tweets")
plt.show()

plt.figure(figsize=(6, 6))
stats.probplot(followers_real, dist="norm", plot=plt)
plt.title("Q-Q-Plot für Real-Tweets")
plt.show()
