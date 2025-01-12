import pandas as pd
from datetime import datetime

# Datei einlesen
file_path = "C:/Users/micha/OneDrive/Desktop/Development/ZHAW/statistic/ActivityAuthor.json"
data = pd.read_json(file_path)

# "tweet_time" in datetime umwandeln
data["tweet_time"] = pd.to_datetime(data["tweet_time"])

# Autoren gruppieren und Daten sortieren
data = data.sort_values(by=["author_id", "tweet_time"])

# Cluster-Logik für jeden Autor definieren
def cluster_author(group):
    # Initialisiere eine Zählung für Tweets innerhalb von 1 Stunde
    tweet_count_in_window = 0
    cluster_flag = False
    # Iteriere über alle Tweets des Autors
    for i in range(len(group)):
        # Zähle Tweets im 1-Stunden-Fenster
        tweet_count_in_window += 1
        if i > 0 and (group["tweet_time"].iloc[i] - group["tweet_time"].iloc[i - tweet_count_in_window + 1]).total_seconds() / 3600 > 1:
            tweet_count_in_window -= 1  # Entferne Tweets außerhalb des 1-Stunden-Fensters
        # Wenn mehr als 5 Tweets innerhalb von 1 Stunde existieren
        if tweet_count_in_window > 5:
            cluster_flag = True
            break
    return "Cluster 1: >5 Tweets innerhalb 1 Stunde" if cluster_flag else "Cluster 2: Keine >5 Tweets innerhalb 1 Stunde"

# Cluster für jeden Autor bestimmen
author_clusters = data.groupby("author_id").apply(cluster_author).reset_index()
author_clusters.columns = ["author_id", "cluster"]

# Daten mit Clusterinformationen zusammenführen
data = data.merge(author_clusters, on="author_id")

# Statistik für die beiden Cluster berechnen
cluster_stats = data.groupby("cluster")["author_id"].nunique()
print("\nCluster-Statistik:")
print(cluster_stats)

# Deskriptive Statistik für Zeitdifferenzen in beiden Clustern
for cluster, group in data.groupby("cluster"):
    print(f"\nStatistik für {cluster}:")
    time_diffs = group["tweet_time"].diff().dropna().dt.total_seconds() / 60  # Zeitdifferenz in Minuten
    print(f"Minimum: {time_diffs.min():.2f} Minuten")
    print(f"Q1 (25%): {time_diffs.quantile(0.25):.2f} Minuten")
    print(f"Median (50%): {time_diffs.median():.2f} Minuten")
    print(f"Q3 (75%): {time_diffs.quantile(0.75):.2f} Minuten")
    print(f"Maximum: {time_diffs.max():.2f} Minuten")

# Verteilung des fact_check-Attributs
for cluster, group in data.groupby("cluster"):
    fact_check_counts = group["fact_check"].value_counts()
    print(f"\nVerteilung des fact_check-Attributs für {cluster}:")
    print(fact_check_counts)

    # Prozentuale Verteilung
    fact_check_proportions = group["fact_check"].value_counts(normalize=True) * 100
    print(f"\nProzentuale Verteilung des fact_check-Attributs für {cluster}:")
    print(fact_check_proportions)
