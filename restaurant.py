# BURLOT ALEXANDRE - ROTH LUCAS
# DATE : 08/06/2021
# -*- coding : 'utf-8' -*- 
# ASCII de 'A' à 'Z' sont de 65 à 90
# TODO :
# -  affichage à vérifier pourquoi il ne marche pas 

import multiprocessing as mp
from multiprocessing.queues import Queue
import random
import time
import sys


CLEARSCR="\x1B[2J\x1B[;H"        #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"
CRLF  = "\r\n"                  #  Retour à la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné

def effacer_ecran() : print(CLEARSCR,end='')
    # for n in range(0, 64, 1): print("\r\n",end='')

def erase_line_from_beg_to_curs() :
    print("\033[1K",end='')

def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')

def move_to(lig, col) : # No work print("\033[%i;%if"%(lig, col)) # print(GOTOYX%(x,y))
    print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def Client(i,nb_c,tableau,lock): # commande à intervalle irrégulier
    while True:
        time.sleep(random.randint(3,5)) # attente random
        for indice in range(0,len(tableau[:])-1,2): # parcours le tableau avec un pas de 2
            if tableau[indice] != -1: # si commande rentrée à cet emplacement, on passe au couple suivant
                pass
            else:
                lock.acquire() # assure qu'il est le seul à écrire dans le tampon
                tableau[indice] = i//100
                tableau[indice+1] = ord('A')+random.randint(0,25)
                lock.release() # laisse la place à un autre client qui souhaiterai commander
                break


def Serveur(Q,numero,tableau,lock):
    while True:
        lock.acquire() # assure qu'il est le seul à écrire dans le tampon
        # Le serveur prend connaissance de la commande en première position du tableau
        num_commande = tableau[0]
        plat = tableau[1]
        tableau[0] = -1
        tableau[1] = -1

        # le serveur réorganise le tableau correctement en commançant à l'indice 2
        indice = 2
        while indice < (len(tableau[:])):
            if tableau[indice] == -1:
                tableau[indice-2] = tableau[indice]
                tableau[indice-1] = tableau[indice+1]
                break
            elif indice > (len(tableau[:])-2):
                pass
            else:
                tableau[indice] = tableau[indice+2]
                tableau[indice+1] = tableau[indice+3]
            indice += 2
        lock.release() # laisse la place à un autre serveur libre

        if (num_commande,plat) == (-1,-1):
            Q.put((-1,-1,numero,-1))
        else:
            Q.put((num_commande,plat,numero,'preparation'))
            time.sleep(random.randint(5,10))
            Q.put((num_commande,plat,numero,'servie'))


def Major_dHomme(Q,tableau,nb_serveurs):
    while True:
        tuple_arguments = Q.get()
        ident,plat,num_serveur,etat = tuple_arguments
        if etat == 'preparation':
            move_to(num_serveur,10)
            print(f"Le serveur {num_serveur} prépare la commande ({ident,chr(plat)})        ")
        elif etat == 'servie':
            move_to(num_serveur+3,10)
            print(f"Le serveur {num_serveur} sert la commande ({ident,chr(plat)})           ")
        elif etat == -1:
            move_to(num_serveur,10)
            print("                                                                         ")
        
        # la liste d'attente fonctionne
        liste_attente = []
        for indice in range(0,len(tableau[:])-1,2):
            if tableau[indice] != -1:
                liste_attente.append((tableau[indice],tableau[indice+1]))
        move_to(nb_serveurs+1,10)
        print("Les commandes clients en attente :",liste_attente,"                                                     ")
        move_to(nb_serveurs+2,10)
        print("Nombres de commandes attente :",len(liste_attente),"              ")
        move_to(nb_serveurs+4,10)
        print(tableau[:])



#--------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    nb_client = 5
    nb_serveurs = 5
    taille_tableau = 50

    tableau_commandes = mp.Array('b',[-1 for _ in range(taille_tableau*2)])
    tableau_commandes[0] = 127
    tableau_commandes[1] = ord('A')
    accesseur = mp.Lock()
    effacer_ecran()
    curseur_invisible()
    pile = mp.Queue()

    Lprocess = [mp.Process(target=Client,args=((i+1)*100,nb_client,tableau_commandes,accesseur)) for i in range(nb_client)]
    Lprocess.extend([mp.Process(target=Serveur,args=(pile,i,tableau_commandes,accesseur)) for i in range(nb_serveurs)])
    Lprocess.append(mp.Process(target=Major_dHomme,args=(pile,tableau_commandes,nb_serveurs)))
    for p in Lprocess:
        p.start()
    for p in Lprocess:
        p.join()
    
    curseur_visible()
