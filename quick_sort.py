# BURLOT ALEXANDRE - ROTH LUCAS
# DATE : 01/06/2021 
# TODO :
# - FAIRE LE PROGRAMME DE TRI

import multiprocessing as mp
import sys
import time
from array import array


def Qsort():
    while True:
        print("oui")
        # attente à a queue des 8 processus
        # traitement et séparation en deux liste de droite, et liste de gauche
        # mettre le pivot à la place 

# liste de type array. Soit de la bibliothèque array, soit de mp ( variable partagée )
liste = "liste générée avec un randint"
# création de d'une queue dans laquelle on entrera des listes de la sorte 
# [morceau_de_liste, Liste_initiale_en_train_d'etre_changée,idx_pour_repérer_si_gauche_ou_droite]
# création de 8 processus
# explication : 
#    - prend les parametres depuis la queue
#    - fait l'opération de séparation
#    - les remet dans la queue
#    - si la liste de la queue mesure 1 refaire le pivot une dernière fois
#    - si liste vide --> abandonner la fonction
#    - dans la liste_initiale, on la récupère changée