#coding: utf-8
import pandas as pd
import numpy as np
from random import choice

def build_data_tweets_of_films(path = "../database_construction/databases_with_polarity_filtered", list_films = ['Aladdin', 'MIB', 'X-men']):
    '''Charge, rassemble et enregistre les tweets collectés sur les différents films
    :input: le chemin d'accès au dossier contenant les databases, le nom des films
    :output: le dataframe collecté'''
    dataframes = [pd.read_csv(path + "/database " + x + " with polarity filtered.csv") for x in list_films]
    df_tot = pd.concat(dataframes).reset_index().drop("index", axis=1).drop("Unnamed: 0", axis=1)
    df_tot.to_csv("datasets/tweets_from_films.csv", sep="\t")
    return df_tot

def load_tweets_films():
    '''Charge et renvoie les tweets collectés sur les différents films
    :input: rien
    :output: le dataframe collecté'''
    return pd.read_csv("datasets/tweets_from_films.csv", sep="\t").drop('Unnamed: 0', axis=1)

def load_tweets_general(number_of_rows = 12500):
    '''Charge, traite et renvoie les tweets de la base de donnée générale
    :input: le nombre de tweets
    :output: le dataframe collecté'''
    data = pd.read_csv('datasets/training.csv', encoding='latin-1', names=["Polarity", "ID", "Date", "Unknown", "Name", "Text"])
    data = data[['Text', 'Polarity']]
    data = data.sample(n = number_of_rows).reset_index().drop("index", axis=1)
    data['Polarity'] = data['Polarity']/2 - 1
    return data

def load_tweets_brands(number_of_rows = 9000, get_list = False):
    '''Charge, traite et renvoie les tweets de la base de donnée sur les marques
    :input: le nombre de tweets
    :output: le dataframe collecté'''
    def get_label(words):
        if words == "Negative emotion":
            return -1
        elif words == "Positive emotion":
            return 1
        elif words == "No emotion toward brand or product":
            return 0
        else:
            i = choice([0, 1, -1])
            return i

    def merge_list(x):
        if x == []:
            return []
        else:
            y = x.pop()
            y = y.split(' ')
            return merge_list(x) + y

    data = pd.read_csv('datasets/database2.csv', encoding='latin-1', names=["Text", "Brand", "Polarity"])
    data = data.sample(n=number_of_rows).reset_index().drop("index", axis=1)
    liste = list(set(data["Brand"]))
    new_list = []
    for x in liste:
        new_list.extend(str(x).split())
    data = data[['Text', 'Polarity']]
    data = data[data.Polarity.isnull() == False]
    data["Polarity"] = data["Polarity"].apply(get_label)
    data = data[data.Text.isnull() == False]
    liste = list(set(new_list))
    if get_list:
        return liste
    else:
        return data


#print(load_tweets_brands())

