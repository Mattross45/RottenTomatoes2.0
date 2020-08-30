import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
from sklearn import metrics

def compute_ROC_AUC(Y, Y_guessed, version) :
    '''Calcule et affiche la courbe ROC et l'AUC
    :input: Y les labels, Y_guessed les labels calculés, la version i.e. si les polarités sont à -1 et 1 (version 1), ou à -1, 0 et 1 (version 0)
    :output: l'AUC si deux classes, les deux AUC (sur les données positives et négatives) si 3 classes'''
    if version == 1:
        fpr, tpr, _ = metrics.roc_curve(Y, Y_guessed)
        AUC = metrics.auc(fpr, tpr)
        plot_ROC(fpr, tpr)
        print("AUC :", AUC)
        return AUC
    else:
        def to_pos(x):
            return pd.Series([1 if x[1] == 1 else 0], index=['Polarity'])
        Y_pos = Y.apply(to_pos, axis=1)
        Y_guessed_pos = Y_guessed.apply(to_pos, axis=1)
        def to_neg(x):
            return pd.Series([-1 if x[1] == -1 else 0], index=['Polarity'])
        Y_neg = Y.apply(to_neg, axis=1)
        Y_guessed_neg = Y_guessed.apply(to_neg, axis=1)
        fpr, tpr, _ = metrics.roc_curve(Y_pos, Y_guessed_pos)
        AUC_pos = metrics.auc(fpr, tpr)
        plot_ROC(fpr, tpr, 1)
        print("AUC positif :", AUC_pos)
        fnr, tnr, _ = metrics.roc_curve(Y_neg, Y_guessed_neg)
        AUC_neg = metrics.auc(fnr, tnr)
        plot_ROC(fnr, tnr)
        print("AUC négatif :", AUC_neg)
        return AUC_pos, AUC_neg

def plot_ROC(fpr, tpr, n_figure = 1):
    '''Calcule et affiche la courbe ROC
    :input: les taux de faux positifs et vrais positifs, le numéro de la figure
    :output: rien'''
    plt.figure(n_figure)
    plt.plot(fpr, tpr)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.show()


#Pour tester
from tweet_analyser.get_data import *
from tweet_analyser.treatment_algorithms.text_blob_treatement import *
def f():
    df = load_tweets_general()
    a, b, c, d = text_blob_treatement(df)
    Y = a.drop('Text', axis=1)
    compute_ROC_AUC(c, Y, 1)
