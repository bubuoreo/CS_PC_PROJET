# BURLOT ALEXANDRE - ROTH LUCAS
# DATE : 08/06/2021
# -*- coding : 'utf-8' -*- 
# ASCII de 'A' à 'Z' sont de 65 à 90
# TODO :
# -  timer pour mettre fin au service

import multiprocessing as mp
from multiprocessing.queues import Queue
import signal, sys, time, random


CLEARSCR="\x1B[2J\x1B[;H"        #  Clear SCReen

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

def effacer_ecran() : print(CLEARSCR,end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')

def move_to(lig, col) :
    print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def Client(i,tableau,lock): # commande à intervalle irrégulier
    while True:
        time.sleep(random.randint(3,10)) # attente random
        lock.acquire() # assure qu'il est le seul à écrire dans le tampon
        for indice in range(0,len(tableau[:])-1,2): # parcours le tableau avec un pas de 2
            if tableau[indice] != -1: # si commande rentrée à cet emplacement, on passe au couple suivant
                pass
            else:
                tableau[indice] = i//100
                tableau[indice+1] = ord('A')+random.randint(0,25)
                # print("commande à l'indice",indice,"du client",tableau[indice],"pour le plat",tableau[indice+1])
                break
        lock.release() # laisse la place à un autre client qui souhaiterai commander


def Serveur(Q,numero,tableau,lock):
    deja_dit_rien_faire = False
    while True:
        lock.acquire() # assure qu'il est le seul à écrire dans le tampon
        if (tableau[0] == -1) and (deja_dit_rien_faire == False):
            Q.put((-1,-1,numero,-1))
            lock.release() # laisse la place à un autre serveur libre
            deja_dit_rien_faire = True
        elif tableau[0] != -1:
            deja_dit_rien_faire = False
            # Le serveur prend connaissance de la commande en première position du tableau
            num_commande = tableau[0]
            plat = tableau[1]
            # print("serveur numero (",numero,") à vu les infos (",num_commande,plat,")")
            tableau[0] = -1
            tableau[1] = -1
            # le serveur réorganise le tableau correctement en commançant à l'indice 2
            indice = 0
            while indice <= (len(tableau[:])-2):
                if tableau[indice+2] == -1:
                    tableau[indice] = -1
                    tableau[indice+1] = -1
                    break
                else:
                    tableau[indice] = tableau[indice+2]
                    tableau[indice+1] = tableau[indice+3]
                indice += 2
            lock.release() # laisse la place à un autre serveur libre

            Q.put((num_commande,plat,numero,'preparation'))
            time.sleep(random.randint(3,5))
            Q.put((num_commande,plat,numero,'servie'))
        else:
            lock.release()


def Major_dHomme(Q,tableau,nb_serveurs):
    while True:
        tuple_arguments = Q.get()
        # print(tuple_arguments)
        ident,plat,num_serveur,etat = tuple_arguments
        # if etat == 'preparation':
        #     print(f"Le serveur {num_serveur} prépare la commande ({ident,plat})        ")
        # elif etat == 'servie':
        #     print(f"Le serveur {num_serveur} sert la commande ({ident,plat})           ")
        # elif etat == -1:
        #     print(f"Le serveur {num_serveur} ne fait rien")
        if etat == 'preparation':
            move_to(num_serveur,10)
            print(f"Le serveur {num_serveur} prépare la commande ({ident,chr(plat)})        ")
        elif etat == 'servie':
            move_to(nb_serveurs+3,10)
            print(f"Le serveur {num_serveur} sert la commande ({ident,chr(plat)})           ")
        elif etat == -1:
            move_to(num_serveur,10)
            print("le serveur n'a rien à faire                                                                         ")
        
        # la liste d'attente fonctionne
        liste_attente = []
        for indice in range(0,len(tableau[:])-1,2):
            if tableau[indice] != -1:
                liste_attente.append((tableau[indice],chr(tableau[indice+1])))
        move_to(nb_serveurs+1,10)
        print("Les commandes clients en attente :",liste_attente,"                                                     ")
        move_to(nb_serveurs+2,10)
        print("Nombres de commandes attente :",len(liste_attente),"              ")

def FinService(signal,frame):
    move_to(14,10)
    print("Fin du service. Au revoir")
    curseur_visible()
    sys.exit(0)

#--------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    nb_client = 5
    nb_serveurs = 3
    taille_tableau = 50

    # le tableau est défini pour une taille de deux fois la taille demandée car chaque commande prendra deux places dans le tableau
    # une première place pour le numero du client qui à commandé et le deuxième sera l'ascii du plat commandé
    tableau_commandes = mp.Array('b',[-1 for _ in range(taille_tableau*2)])
    accesseur = mp.Lock() # Lock pour le tableau
    effacer_ecran() # effaçage de l'écran pour affichage
    curseur_invisible() # rend invisible le curseur
    pile = mp.Queue() # queue de discussion entre les serveurs et le major d'homme
    signal.signal(signal.SIGINT, FinService) # pour arreter le service

    # création de la liste des process et du lancement de ceux ci
    Lprocess = [mp.Process(target=Client,args=((i+1)*100,tableau_commandes,accesseur)) for i in range(nb_client)]
    Lprocess.extend([mp.Process(target=Serveur,args=(pile,i+1,tableau_commandes,accesseur)) for i in range(nb_serveurs)])
    Lprocess.append(mp.Process(target=Major_dHomme,args=(pile,tableau_commandes,nb_serveurs)))
    for p in Lprocess:
        p.start()
    for p in Lprocess:
        p.join()
