import json

# Eingabedatei und Ausgabedatei definieren
input_file = "tweets_factchecked/tweets_factchecked16.json"
output_file = "tweets_factchecked_Real_or_Fake17.json"

def filter_tweets(input_file, output_file):
    """Filtert Tweets, die nur als 'real' oder 'fake' klassifiziert sind."""
    with open(input_file, "r", encoding="utf-8") as infile:
        tweets = json.load(infile)

    # Filtere die Tweets
    filtered_tweets = [tweet for tweet in tweets if tweet.get("factCheck") in ["real", "fake"]]

    # Speichere die gefilterten Tweets in die neue Datei
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(filtered_tweets, outfile, indent=4, ensure_ascii=False)

    print(f"Filtered tweets saved to {output_file}")

if __name__ == "__main__":
    # Funktion ausführen
    filter_tweets(input_file, output_file)
