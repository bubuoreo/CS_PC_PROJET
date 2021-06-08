# BURLOT ALEXANDRE - ROTH LUCAS
# DATE : 08/06/2021
# -*- coding : 'utf-8' -*- 
# ASCII de 'A' à 'Z' sont de 65 à 90
# TODO :
# -  

import multiprocessing as mp
from multiprocessing.queues import Queue
from random import randint
import time


def Client(Q,i):
    while True:
        time.sleep(randint(1,10))
        print("Je suis le client",i//100,"et j'effectue la commande n°",i,"et je demande le Plat",chr(ord('A')+randint(0,25)))
        i += 1
        Q.put((i,chr(ord('A')+randint(0,25))))

def Serveur(Q,numero):
    while True:
        tuple_args = Q.get()
        commande = tuple_args[0]
        plat = tuple_args[1]
        print(f"je suis le serveur n°{numero}, je m'occupe de la commande n°{commande}, le plat {plat} est en train d'être préparé")
        time.sleep(5)

def Major_dHomme():
    print("je suis le major d'homme et je m'occupe des affichages")


#---------------------------------------------------------------------------

if __name__ == '__main__':
    
    nb_client = 5
    nb_serveurs = 6
    pile = mp.Queue()

    Lprocess = [mp.Process(target=Client,args=(pile,(i+1)*100,)) for i in range(nb_client)]
    Lprocess.extend([mp.Process(target=Serveur,args=(pile,i+1)) for i in range(nb_serveurs)])
    for p in Lprocess:
        p.start()
    for p in Lprocess:
        p.join()
