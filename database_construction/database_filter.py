# coding: utf-8
import re
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
tok = WordPunctTokenizer()
import numpy as np
import sys
import pandas as pd
from langdetect import DetectorFactory
from langdetect import detect
DetectorFactory.seed = 0

def tweet_cleaner(text, new_stop_words = []):
    '''Permet de nettoyer les textes des tweets (enlève les sites web, les @, les rt et éventuellement les références aux films)
    :input: le texte du tweet
    :output: le texte filtré'''
    pat1 = r'@[A-Za-z0-9_]+'        # remove @ mentions from tweets
    pat2 = r'https?://[^ ]+'        # remove URL's from tweets
    combined_pat = r'|'.join((pat1, pat2)) #addition of pat1 and pat2
    www_pat = r'www.[^ ]+'         # remove URL's from tweets
    contracted_words_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",   # converting words like isn't to is not
                    "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                    "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                    "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                    "mustn't":"must not", "it's":"it is", "i'm":"i am", "you're":"you are", "he's":"he is", "we're":"we are", "they're":"they are", "would've":"would have"}
    contrac_pattern = re.compile(r'\b(' + '|'.join(contracted_words_dic.keys()) + r')\b')

    stripped = re.sub(combined_pat, '', text) # calling combined_pat
    stripped = re.sub(www_pat, '', stripped) #remove URL's
    lower_case = stripped.lower()      # converting all into lower case
    neg_handled = contrac_pattern.sub(lambda x: contracted_words_dic[x.group()], lower_case) # converting word's like isn't to is not
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)       # will replace # by space
    stop_words = new_stop_words[:]
    stop_words.extend(['s', 'rt'])
    words = [x for x in tok.tokenize(letters_only) if x not in stop_words]
    return (" ".join(words)).strip() # join the words


def epurateur(dataframe):
    '''Pour chaque row, clean le texte et supprmie si pas en anglais. Premier filtre avant de trier
    :input: le dataframe des tweets
    :output: le dataframe filtré'''
    dataframe_copy = dataframe.copy()
    DetectorFactory.seed = 0
    dataframe_copy = dataframe_copy.drop_duplicates()
    indexes = []
    for index, row in dataframe_copy.iterrows():
        text = str(row['tweet_textual_content'])
        text = tweet_cleaner(text)
        text_copy = tweet_cleaner(text, ["ht", "amp", "dp", "toyota", "lexus", "inasoft", "d", "h", "t", "f", "xh", "m", "bd", "rt", "marvel", "endgame", "spiderman", "x-men", "mib", "aladdin", "jasmine", "jafar", "marvelcomics", "mibinternational", "meninblack", "teammibinternational"])
        dataframe_copy.loc[index, 'tweet_textual_content'] = text
        try:
            assert text_copy != ""
            assert detect(text) == 'en'
        except:
            indexes.append(index)
    dataframe_copy = dataframe_copy.drop(indexes, axis=0).reset_index().drop("index", axis=1).drop("Unnamed: 0", axis=1)
    return dataframe_copy
