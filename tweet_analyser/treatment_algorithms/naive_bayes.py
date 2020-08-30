import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from tweet_analyser.clean_text import *
from tweet_analyser.treatment_algorithms.vectorize_data import *

def construct_model(X_train, Y_train):
    '''Construit le modèle bayesien simple
    :input: les données d'entraînement, les labels correspondant
    :output: le modèle entraîné'''
    clf = MultinomialNB()
    clf.fit(X_train, Y_train)
    return clf

def simple_bayes_treatment(df, test_size=0.2, use_tf=False, min_df = 0.0001, ngram_range=(1,2), use_idf = True):
    '''Renvoie les polarités d'un dataframe selon un modèle bayesien simple
    :input: le dataframe des données, la taille du test, les ngrams (combien de mots par paquets, sous la forme (n_gram_min, n_gram_max)), si on utilise idf dans le cas du modèle avec tf
    :output: les dataframes data_train, data_test des données (texte et polarité), Y_guess_train et Y_guess_test des polarités calculées sur les données d'entraînement et de test'''
    data_train, data_test = train_test_split(df, test_size=test_size)
    data_train = data_train.reset_index().drop("index", axis=1)
    data_test = data_test.reset_index().drop("index", axis=1)
    if use_tf:
         vectorizer, X_train, X_test = vectorize_data_tfid_model(data_train, data_test, min_df, ngram_range, use_idf)
    else:
        vectorizer, X_train, X_test = vectorize_data_binary_model(data_train, data_test, min_df, ngram_range)
    Y_train = data_train['Polarity']
    clf = construct_model(X_train, Y_train)
    Y_guess_train = pd.DataFrame(clf.predict(X_train), columns = ["Polarity"])
    Y_guess_test = pd.DataFrame(clf.predict(X_test), columns = ["Polarity"])
    return data_train, data_test, Y_guess_train, Y_guess_test

def get_best_bayes_params(df, use_idf_list=[True, False], min_df_list = [0.0001, 0.0005, 0.001, 0.005], ngram_range_list=[(1,1), (1, 2), (1, 3)]):
    '''Renvoie les meilleurs paramètres pour la vectorisation du test, pour le modèle bayesien simple
    :input: le dataframe des données, s'il faut utiliser l'idf, la liste des df min à tester, la liste des ngrams à tester
    :output: les paramètres du meilleur modèle'''
    text_clf = Pipeline([('tfidf', TfidfVectorizer()), ('clf', MultinomialNB())])
    parameters = {'tfidf__use_idf':use_idf_list, 'tfidf__min_df':min_df_list, 'tfidf__ngram_range':ngram_range_list}
    gs_clf = GridSearchCV(text_clf, parameters)
    gs_clf = gs_clf.fit(df.Text, df.Polarity)
    return gs_clf.best_params_

#Pour tester
from tweet_analyser.get_data import *
from tweet_analyser.treatment_algorithms.text_blob_treatement import *
def f(use_tf, min_df, ngram_range):
    df = load_tweets_brands()
    a, b, c, d = simple_bayes_treatment(df, use_tf=use_tf, min_df = min_df, ngram_range = ngram_range)
    e = a.drop(['Text'], axis=1)
    f = b.drop(['Text'], axis=1)
    print((e==c).Polarity.value_counts(), (f==d).Polarity.value_counts())
