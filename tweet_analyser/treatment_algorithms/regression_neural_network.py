import keras
import pandas as pd
from keras.models import Sequential, Model
from keras import regularizers
from keras.layers import Dense
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from tweet_analyser.treatment_algorithms.vectorize_data import *

def construct_neural_network(X_train, Y_train, lambda2, version):
    '''Renvoie le modèle neuronal entraîné
    :input: les données de test, la valeur de l'hyperparamètre (pénalisation Ridge), les bonnes classes, la version
    :output: le modèle entraîné'''
    model = Sequential()
    nb_voc = X_train.shape[1]
    model.add(Dense(500, activation = 'relu', kernel_regularizer = regularizers.l2(lambda2), input_dim = nb_voc))
    model.add(Dense(200, activation = 'relu',kernel_regularizer = regularizers.l2(lambda2)))
    model.add(Dense(100, activation = 'relu',kernel_regularizer = regularizers.l2(lambda2)))
    model.add(Dense(3-version, activation = 'sigmoid',kernel_regularizer = regularizers.l2(lambda2)))
    model.compile(loss = 'mean_squared_error', optimizer = Adam())
    model.fit(X_train, Y_train, epochs=3, batch_size=32, verbose=400)
    return model

def transform_answer(Y_nn, version):
    '''Prend la sortie du modèle (à chaque entrée on associe un nombre entre 0 et 1 pour chaque classe) et la transforme en associant à chaque entrée la bonne classe
    :input: un dataframe contenant une réponse du modèle
    :output: le dataframe correspondant avec les classes'''
    Y = []
    for tab in Y_nn:
        if max(tab) == tab[0]:
            Y.append(-1)
        elif max(tab) == tab[1]:
            if version == 0:
                Y.append(0)
            else:
                Y.append(1)
        else:
            Y.append(1)
    return pd.DataFrame(Y, columns = ["Polarity"])


def regression_neural_network_treatment(df, test_size=0.2, version=1, use_tf=False, min_df=0.0001, ngram_range=(1,2), use_idf = True, lambda2 = 0.00001):
    '''Renvoie les polarités d'un dataframe selon un modèle neuronal
    :input: le dataframe des données, la taille du test, la version, si on utilise tf, le df minimum pour lequel on garde les termes, les ngrams (combien de mots par paquets, sous la forme (n_gram_min, n_gram_max)), si on utilise idf dans le cas d'un modèle avec tf, la valeur de l'hyperparamètre (pénalisation Ridge)
    :output: les dataframes data_train, data_test des données (texte et polarité), Y_guess_train et Y_guess_test des polarités calculées sur les données d'entraînement et de test'''
    data_train, data_test = train_test_split(df, test_size=test_size)
    data_train = data_train.reset_index().drop("index", axis=1)
    data_test = data_test.reset_index().drop("index", axis=1)
    if use_tf:
         vectorizer, X_train, X_test = vectorize_data_tfid_model(data_train, data_test, min_df, ngram_range, use_idf)
    else:
        vectorizer, X_train, X_test = vectorize_data_binary_model(data_train, data_test, min_df, ngram_range)
    Y_train = data_train['Polarity']
    Y_train_binarized = pd.get_dummies(Y_train)
    model = construct_neural_network(X_train, Y_train_binarized, lambda2, version)
    Y_guess_train = transform_answer(model.predict(X_train, batch_size=32), version)
    Y_guess_test = transform_answer(model.predict(X_test, batch_size=32), version)
    return data_train, data_test, Y_guess_train, Y_guess_test
