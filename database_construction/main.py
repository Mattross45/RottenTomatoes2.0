# coding: utf-8
import pandas as pd
from database_filter import *
from hand_construction import *

databases_names = ["Marvel", "MIB", "X-men", "Toy Story", "Aladin", "Harry "]

def tokenize_database(name, epurateur_and_polarity = True, start = 0, stop = -1):
    '''Compile les différentes fonctions pour tokeniser les tweets, et enregistre le résultat
    :input: le nom de la db à tokeniser, si on part de 0 ou si une partie a déjà été faite, l'indice de début, l'indice de fin
    :output: le dataframe filtré avec la polarisation'''
    if epurateur_and_polarity:
        complete_name = "databases/database " + name + ".csv"
        df = pd.read_csv(complete_name, sep="\t")
        df = epurateur(df)
        df['polarity'] = 0
    else:
        complete_name = "databases_with_polarity/database " + name + "with polarity.csv"
        df = pd.read_csv(complete_name, sep="\t")
    df_with_polarity = construction_by_hand(df, start, stop)
    complete_name_with_polarity = "databases_with_polarity/database " + name + " with polarity.csv"
    df_with_polarity.to_csv(complete_name_with_polarity, sep="\t")
    df_with_polarity_filtered = df_with_polarity[['tweet_textual_content', 'polarity']].rename(columns={'tweet_textual_content':'Text', 'polarity':'Polarity'})
    complete_name_with_polarity_filtered = "databases_with_polarity_filtered/database " + name + " with polarity filtered.csv"
    df_with_polarity_filtered.to_csv(complete_name_with_polarity_filtered, sep="\t")
    return df_with_polarity_filtered

#tokenize_database(databases_names[4])

#jarvis, thanos, Steve rogers, avengers

