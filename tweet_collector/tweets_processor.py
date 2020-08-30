# coding: utf-8
import pandas as pd
import numpy as np
from collector import *

def collect_to_pandas_dataframe(tweet_list, path = "tweets_from_tweet_list.csv", mode = 'w'):
    """Pour enregistrer les données utiles en format csv
    :input: une liste de tweets au format json, le nom du fichier, et le mode d'écriture
    :output: le dataframe"""
    data = pd.DataFrame(data=[tweet['text'] for tweet in tweet_list], columns=['tweet_textual_content'])
    data['len'] = np.array([len(tweet['text']) for tweet in tweet_list])
    data['ID'] = np.array([tweet['id'] for tweet in tweet_list])
    data['Date'] = np.array([tweet['created_at'] for tweet in tweet_list])
    data['Source'] = np.array([tweet['source'] for tweet in tweet_list])
    data['Likes'] = np.array([tweet['favorite_count'] for tweet in tweet_list])
    data['RTs'] = np.array([tweet['retweet_count'] for tweet in tweet_list])
    data.to_csv(path, sep = "\t", mode = mode, encoding="utf-8")
    return data

#print(collect_to_pandas_dataframe(get_tweets_from_candidates_search_queries_liste(["MIB"])).head())

collect_to_pandas_dataframe(update_tweet_list(collect_tweet_streaming(["John Wick"], 1000)))