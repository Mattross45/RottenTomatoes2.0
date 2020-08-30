# coding: utf-8
import pandas as pd
from textblob import TextBlob as tb
from sklearn.model_selection import train_test_split
from random import choice

def get_polarity_text_blob(text, version, seuil = 0.05):
    '''Renvoie la polarité du tweet selon textblob
    :input: le texte du tweet, la version i.e. si les polarités sont à -1 et 1 (version 1), ou à -1, 0 et 1 (version 0)
    :output: la polarité devinée'''
    if version == 0:
        if tb(text).sentiment.polarity < -1*seuil:
            return -1
        if tb(text).sentiment.polarity > seuil:
            return 1
        else:
            return 0
    else :
        if tb(text).sentiment.polarity < 0:
            return -1
        if tb(text).sentiment.polarity > 0:
            return 1
        else : return choice([-1,1])


def text_blob_treatement(df, test_size=0.2, version = 1):
    '''Renvoie les polarités d'un dataframe selon textblob
    :input: le dataframe des données, la taille du test, la version (cf. plus haut)
    :output: les dataframes data_train, data_test des données (texte et polarité), Y_guess_train et Y_guess_test des polarités calculées sur les données d'entraînement et de test'''
    data_train, data_test = train_test_split(df, test_size=test_size)
    data_train = data_train.reset_index().drop("index", axis=1)
    data_test = data_test.reset_index().drop("index", axis=1)
    Y_guess = {'Y_guess_test' : [], 'Y_guess_train' : []}
    for tweet in data_train['Text']:
        Y_guess['Y_guess_train'].append(get_polarity_text_blob(tweet, version))
    for tweet in data_test['Text']:
        Y_guess['Y_guess_test'].append(get_polarity_text_blob(tweet, version))
    Y_guess_train = pd.DataFrame(data={'Polarity' : Y_guess['Y_guess_train']})
    Y_guess_test = pd.DataFrame(data={'Polarity': Y_guess['Y_guess_test']})
    return data_train, data_test, Y_guess_train, Y_guess_test
