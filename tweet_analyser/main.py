import pandas as pd
import numpy as np
from get_data import *
from clean_text import *
from tweet_analyser.treatment_algorithms.text_blob_treatement import text_blob_treatement
from tweet_analyser.treatment_algorithms.vader_treatment import vader_treatment
from tweet_analyser.treatment_algorithms.naive_bayes import simple_bayes_treatment
from tweet_analyser.treatment_algorithms.regression_neural_network import regression_neural_network_treatment
from tweet_analyser.graphics.visualize_data import graph_matrice
from tweet_analyser.graphics.ROC import compute_ROC_AUC
from tweet_analyser.graphics.model_score import show_score

datasets_names = ['film_tweets', 'general_tweets', 'brand_tweets']

clean_text_names = ['stop_word_list_light', 'stop_word_list_normal', 'stop_word_list_heavy', 'lemmatize']

def apply_clean_text(df, f):
    df_copy = df.copy()
    df_copy.Text = df_copy.Text.apply(f)
    return df_copy

treatments_names = ['text_blob', 'vader', 'naive_bayes', 'neural_network']

graphics = ["ROC", "visualize_data"]

