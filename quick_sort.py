# BURLOT ALEXANDRE - ROTH LUCAS
# DATE : 01/06/2021
# -*- coding : utf-8 -*- 
# TODO :
# - timer sur les utilisations longues

import multiprocessing as mp
import time
from queue import Empty
from random import randint


def Qsort(Q,Tableau,lock,keep_running):
    while keep_running.value:
        
        # condition de sortie : si la liste 'Tableau' est bien triée
        verif = True
        for i in range(len(Tableau)-1):
            if Tableau[i] > Tableau[i+1]:
                verif = False
        keep_running.value = not verif
        # print('KP = ', keep_running.value)

        # vérification de présence de valeurs dans la queue
        try:
            liste_args = Q.get(timeout=1)
        except (Empty): 
            # print("exception empty")
            pass

        # print(liste_args)
        
        liste = liste_args[0]
        position = liste_args[1]

        # ne met rien dans la pile si la liste fournie est vide
        if liste == []:
            pass

        else:
            pivot = liste[0] # le pivot est le premier élément de la liste
            
            # initialisation des liste Gauche et Droite
            LG = []
            LD = []

            # tri dans les deux listes les valeurs plus grandes et plus petites que le pivot
            for chiffre in liste[1:]:
                if chiffre <= pivot:
                    LG.append(chiffre)
                else:
                    LD.append(chiffre)

            # print('pivot : ',pivot)
            # print('LG : ', LG)
            # print('LD : ',LD)

            # Utilisation d'un Lock pour le tableau partagé par les tous les Process 
            lock.acquire()
            # print('ecriture du pivot',pivot,"à l'indice",position+len(LG))
            Tableau[position+len(LG)] = pivot
            lock.release()

            # transmission dans la Queue des nouvelles listes à trier avec le bon indice de référence
            Q.put((LG,position))
            Q.put((LD,len(LG)+position+1))


if __name__ == '__main__':

    # création du tableau à valeurs aléatoire
    tableau = mp.Array('i', [randint(1,99) for i in range(100)])
    print("tableau d'origine",tableau[:])

    # Variables partagées
    keep_running = mp.Value('b',True)
    queue = mp.Queue()
    lock = mp.Lock()

    # Mise en queue du tableau de départ
    queue.put((tableau[:],0))

    # création et lancement des Process
    debut = time.time()
    Lprocess = [mp.Process(target=Qsort, args=(queue,tableau,lock,keep_running)) for i in range(8)]
    for p in Lprocess:
        p.start()
    for p in Lprocess:
        p.join()
    delay = time.time() - debut
    print("Tableau trié croissant : ",tableau[:])
    print(f"Temps d'execution : {delay} secondes")