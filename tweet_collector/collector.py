# coding: utf-8
# Prend et les rend à l'état brut
from tweepy import *
from connection_setup import *
import time
import json


def get_tweets_from_candidates_search_queries_liste(queries):
    """Renvoie des tweets à propos d'une liste de termes
    :input: les termes
    :output: une liste contenant tous les tweets faisant référence aux termes sous format json"""
    try :
        connexion = twitter_setup() #on se connecte au compte twitter
        liste = []
        for mot_clef in queries:       #pour chaque mot-clef
            tweets = connexion.search(mot_clef, rpp=100) #on cherche les tweets selon les mots clefs
            for tweet in tweets:   # et on les met dans une liste
                data = tweet._json
                # Pour enlever les tweets ne respectant pas la casse
                print(data)
                if mot_clef.lower() in data['text'].lower():
                    liste.append(data)
            return liste
    except TweepError:
        return "erreur"
    except RateLimitError:
        return "erreur"

def collect_tweet_streaming(queries, temps = 120):
    """Renvoie tous les tweets à propos d'une liste de termes émis pendant le temps temps
    :input: les termes, le temps pendant lequel on fait tourner la fonction
    :output: une liste contenant tous les tweets faisant référence aux termes pendant le temps 'temps' sous format json"""

    #Définition du listener
    class ListenerTweets(StreamListener):

        def on_data(self, data):
            try:
                data = json.loads(data) #Les données renvoyées sont des fichiers text, qu'il faut transformer en json
                print(data)
                a = data["in_reply_to_status_id"] #Pour vérifier que l'objet est bien un tweet
                # Pour enlever les tweets ne respectant pas la casse
                for query in queries:
                    if query.lower() in data['text'].lower():
                        tweets.append(data)
                        raise TweepError
            except:
                pass
            return True

        def on_error(self, status):
            if str(status) == "420":
                print(status)
                print("You exceed a limited number of attempts to connect to the streaming API")
                return False
            else:
                return True

    #Initialisation des données
    tweets = [] #Une liste stockant les twwets du candidat

    #Définition des listeners
    connexion = twitter_setup()
    listener = ListenerTweets()
    stream_tweets = tweepy.Stream(auth = connexion.auth, listener=listener)
    stream_tweets.filter(track=queries, is_async=True)

    #Attente avant fin du stream
    time.sleep(temps)
    stream_tweets.disconnect()

    return tweets


def update_tweet_list(tweet_list):
    """Pour mettre à jour une liste de tweets
    :input: une liste de tweets au format json
    :output: la liste des tweets mise à jour, au format json"""
    connexion = twitter_setup()
    i = 0
    updated_tweets = []
    while i<len(tweet_list):
        #On peut mettre à jour jusqu'à 100 tweets en même temps
        updated_tweets.extend(connexion.statuses_lookup([tweet_list[j]["id"] for j in range(i, i+100) if j<len(tweet_list)]))
        i += 100
    return [tweet._json for tweet in updated_tweets]



#print(get_tweets_from_candidates_search_queries_liste(["MIB"]))
#print(len(get_tweets_from_candidates_search_queries_liste(["MIB"])))
#print(collect_tweet_streaming(["Men in Black", "MIB"]))

