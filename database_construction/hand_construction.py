# coding: utf-8
import pandas as pd

def construction_by_hand(dataframe, start = 0, stop = -1):
    '''Pour construire à la main la bdd
    :input: le dataframe des tweets (avec la colonne polarity), l'indice pour lequel on commence, l'indice pour lequel on termine
    :output: le dataframe avec les polarités rajoutées'''
    dataframe = dataframe.copy()
    stop = len(dataframe) if stop == -1 else stop
    indexes = []
    for i in range(start, stop):
        print(dataframe.loc[i, 'tweet_textual_content'])
        polarity = "a"
        while polarity not in [-1, 0, 1, 2]:
            try:
                polarity = int(input("Polarity (1, 2 ou 3 ou 4) ? "))-2
                if polarity == 2:
                    indexes.append(i)
            except:
                polarity = "a"
        dataframe.loc[i, 'polarity'] = polarity
        print()
    dataframe = dataframe.drop(indexes, axis=0).reset_index().drop("index", axis=1)
    return dataframe

#df = pd.read_csv("../tweet_collector/database X-men.csv", sep="\t")
