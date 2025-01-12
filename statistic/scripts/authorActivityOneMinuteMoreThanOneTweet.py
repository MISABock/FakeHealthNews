import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Datei einlesen
file_path = "C:/Users/micha/OneDrive/Desktop/Development/ZHAW/statistic/ActivityAuthor.json"
data = pd.read_json(file_path)

# "tweet_time" in datetime umwandeln
data["tweet_time"] = pd.to_datetime(data["tweet_time"])

# Autoren gruppieren und Zeitdifferenzen berechnen
data = data.sort_values(by=["author_id", "tweet_time"])
data["time_diff"] = data.groupby("author_id")["tweet_time"].diff().dt.total_seconds() / 60

# Cluster-Logik für jeden Autor definieren
def cluster_author(group):
    recent_activity = (group["time_diff"] <= 1).sum()
    if recent_activity > 1:
        return "Cluster 1: >1 Tweet innerhalb 1 Minute (Post/Repost)"
    else:
        return "Cluster 2: <=1 Tweet innerhalb 1 Minute (Post/Repost)"

# Cluster für jeden Autor bestimmen
author_clusters = data.groupby("author_id").apply(cluster_author).reset_index()
author_clusters.columns = ["author_id", "cluster"]

# Daten mit Clusterinformationen zusammenführen
data = data.merge(author_clusters, on="author_id")

# Stichprobengröße für jeden Cluster berechnen
cluster_sample_size = data.groupby("cluster")["author_id"].nunique()

# Verteilung des fact_check-Attributs für beide Cluster berechnen
cluster_fact_check = data.groupby(["cluster", "fact_check"]).size().unstack(fill_value=0)

# Chi-Quadrat-Test
chi2, p, dof, expected = chi2_contingency(cluster_fact_check)

# Balkendiagramm erstellen
ax = cluster_fact_check.plot(
    kind="bar",
    figsize=(12, 7),
    stacked=True,
    color=["pink", "orange"],
    edgecolor="black"
)

# Titel und Beschriftungen anpassen
plt.title("Vergleich der Cluster: Autoren, die innerhalb von 1 Minute posten oder reposten", fontsize=14)
plt.xlabel("Cluster", fontsize=12)
plt.ylabel("Anzahl der Tweets", fontsize=12)
plt.xticks(rotation=0)
plt.legend(title="Fact Check", labels=["Fake-News", "Real-News"], fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Stichprobengröße auf die Balken schreiben
for i, cluster in enumerate(cluster_fact_check.index):
    total_authors = cluster_sample_size.loc[cluster]
    ax.text(
        i,  # X-Position
        cluster_fact_check.sum(axis=1)[cluster] + 10,  # Y-Position leicht oberhalb der Balken
        f"Authors: n={total_authors}",  # Text anpassen, um die Anzahl Autoren zu verdeutlichen
        ha="center", fontsize=10, color="black"
    )

# Korrekte Werte (Anzahl Tweets) auf die Balken schreiben
for p in ax.patches:
    height = p.get_height()
    if height > 0:  # Nur Werte anzeigen, wenn Höhe > 0
        ax.annotate(
            f'{int(height)}',  # Höhe (Wert) der Balken
            (p.get_x() + p.get_width() / 2., p.get_y() + height / 2),  # Position: Mitte des Balkens
            ha='center', va='center', fontsize=10, color='black'
        )

plt.tight_layout()
plt.show()
