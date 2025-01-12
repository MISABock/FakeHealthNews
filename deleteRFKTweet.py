import json

# Dateipfade definieren
input_file = "tweets_factchecked_Real_or_Fake/tweets_factchecked_Real_or_Fake17.json"   # Die Eingabe-JSON-Datei
output_file = "tweets_filtered16.json"  # Die bereinigte JSON-Datei

# Funktion zum Filtern der Tweets
def filter_tweets(input_path, output_path, exclude_original_id):
    try:
        # Eingabedatei laden
        with open(input_path, "r", encoding="utf-8") as infile:
            tweets = json.load(infile)
        
        # Tweets filtern: Entferne Tweets mit dem angegebenen original_tweet_id
        filtered_tweets = [
            tweet for tweet in tweets 
            if tweet.get("original_tweet_id") != exclude_original_id
        ]
        
        # Gefilterte Tweets in die Ausgabedatei speichern
        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(filtered_tweets, outfile, indent=4, ensure_ascii=False)
        
        print(f"Bereinigung abgeschlossen! {len(filtered_tweets)} Tweets gespeichert in '{output_path}'.")

    except Exception as e:
        print(f"Fehler: {e}")

# Parameter für die Filterung
EXCLUDE_ORIGINAL_ID = 1857182087683735972

# Funktion ausführen
filter_tweets(input_file, output_file, EXCLUDE_ORIGINAL_ID)
