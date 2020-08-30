import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def show_score(y_real, y_guessed):
    '''Affiche la qualité du modèle considéré
    :input: le dataframe des classes réelles, le dataframe des classes devinées
    :output: rien (affiche le graphe correspondante)'''
    sns.set(style="white", context="talk")
    results = (y_real == y_guessed).Polarity.value_counts()
    nb_true = results[True]
    nb_false = results[False]
    nb_tot = len(y_real)
    X = ['Vrai', 'Faux']
    Y = [nb_true/nb_tot, nb_false/nb_tot]
    sns.barplot(x=X, y=Y, palette="rocket")
    plt.ylabel("Pourcentage des tweets devinés")
    plt.title('Qualité du modèle')
    axes = plt.gca()
    axes.set_ylim([0,1])
    plt.show()
