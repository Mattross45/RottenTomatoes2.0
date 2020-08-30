import seaborn as sns
import numpy as np
import pandas as pd

def get_type(y_real, y_guessed, version):
    '''Pour trouver dans quelle catégorie se situe chaque couple entrée/sortie
    :input: la sortie réelle, la sortie trouvée, la version des tweets (classés entre 1 et -1, ou 1, 0 et -1)
    :output: la catégorie (selon la sortie réelle et la sortie trouvée)'''
    if version == 1:
        if y_real == 1:
            if y_guessed == 1:
                return [1, 1]
            else:
                return [1, 2]
        else:
            if y_guessed == 1:
                return [2, 1]
            else:
                return [2, 2]
    else:
        if y_real == 1:
            if y_guessed == 1:
                return [1, 1]
            elif y_guessed == 0:
                return [1, 2]
            else:
                return [1, 3]
        elif y_real == 0:
            if y_guessed == 1:
                return [2, 1]
            elif y_guessed == 0:
                return [2, 2]
            else:
                return [2, 3]
        else:
            if y_guessed == 1:
                return [3, 1]
            elif y_guessed == 0:
                return [3, 2]
            else:
                return [3, 3]


def graph_matrice(Y_real, Y_guessed, version=1):
    '''Affiche la matrice présentant le nombre de sorties trouvées dans chaque catégorie (négatif, neutre si il y a, positif) en fonction de la vraie catégorie (idem)
    :input: le dataframe des classes réelles, le dataframe des classes devinées, la version (0 si (-1, 0, 1), 1 si (-1, 1))
    :output: rien (affiche la matrice correspondante)'''
    if version == 1:
        matrix_confusion = np.zeros((2, 2))
        # matrix_confusion = [vrai_positif(1,1), faux_negatif(1,-1)]
        #                  [faux_positif(-1,1), vrai_negatif(-1,-1)]
        for i in range(len(Y_real)):
            result = get_type(Y_real["Polarity"][i], Y_guessed["Polarity"][i], version)
            matrix_confusion[result[0] - 1][result[1] - 1] += 1
        matrix_confusion = pd.DataFrame(matrix_confusion, columns=['Deviné : positif', 'Deviné : négatif'], index=['Réel : positif', 'Réel : négatif'])
        sns.heatmap(matrix_confusion, annot=True)
    else:
        matrix_confusion = np.zeros((3, 3))
        # matrix_confusion = [(1,1), (1,0), (1,-1)]
        #                   [(0,1), (0,0), (0,-1)]
        #                  [(-1,1), (-1,0), (-1,-1)]
        for i in range(len(Y_real)):
            result = get_type(Y_real["Polarity"][i], Y_guessed["Polarity"][i], version)
            matrix_confusion[result[0] - 1][result[1] - 1] += 1
        matrix_confusion = pd.DataFrame(matrix_confusion, columns=['Deviné : positif', 'Deviné : neutre', 'Deviné : négatif'], index=['Réel : positif', 'Réel : neutre', 'Réel : négatif'])
        sns.heatmap(matrix_confusion, annot=True, cmap="YlGnBu")
