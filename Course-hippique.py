# BURLOT ALEXANDRE - ROTH LUCAS
# DATE : 01/06/2021 
# TODO :
# - GESTION DES EX AEQUOS
# - CHANGEMENT DU CHEVAL par ça :
#        __
#   ____//\\
# /[__A_]
#  ||  || 

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


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

#-------------------------------------------------------

from multiprocessing import Process, Semaphore, Value, Lock, Array
import os, time,math, random, sys
from array import array  # Attention : différent des 'Array' des Process

keep_running=Value('b',True) # Fin de la course ?
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY, CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, \
             CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
    # for n in range(0, 64, 1): print("\r\n",end='')

def erase_line_from_beg_to_curs() :
    print("\033[1K",end='')

def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')

def move_to(lig, col) : # No work print("\033[%i;%if"%(lig, col)) # print(GOTOYX%(x,y))
    print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='')


def un_cheval(ma_ligne : int,LONGEUR_COURSE,mutex,Lpos,keep_running) : # ma_ligne commence à 0
    # move_to(20, 1); print("Le chaval ", chr(ord('A')+ma_ligne), " démarre ...")
    col=1

    while col <= LONGEUR_COURSE and keep_running.value :
        if col == LONGEUR_COURSE:
            mutex.acquire()
            keep_running.value = False
            move_to(30,30)
            en_couleur(lyst_colors[0])
            print(chr(ord('A')+ma_ligne),"fini 1 er")
            mutex.release()
        mutex.acquire();
        move_to(ma_ligne+1,col)
        erase_line_from_beg_to_curs() # pour effacer toute ma ligne
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('('+chr(ord('A')+ma_ligne)+'>')
        Lpos[ma_ligne] = col
        mutex.release()
        col+=1
        time.sleep(0.1 * random.randint(1,5))


def arbitrage(Lpos,mutex,keep_running,bet):
    time.sleep(1)
    while keep_running.value:
        mutex.acquire()
        maxL = max(Lpos[:])
        indexPremier = Lpos[:].index(maxL)
        minL = min(Lpos[:])
        indexDernier = Lpos[:].index(minL)
        move_to(25,30)
        en_couleur(lyst_colors[0])
        print("Le premier cheval est le cheval ",chr(ord('A')+indexPremier)," en position ", maxL," et le cheval ",chr(ord('A')+indexDernier)," est dernier en position ",minL)
        mutex.release()
    mutex.acquire()
    maxL = max(Lpos[:])
    indexPremier = Lpos[:].index(maxL)
    minL = min(Lpos[:])
    indexDernier = Lpos[:].index(minL)
    move_to(25,30)
    en_couleur(lyst_colors[0])
    print("Le premier cheval est le cheval ",chr(ord('A')+indexPremier)," en position ", maxL," et le cheval ",chr(ord('A')+indexDernier)," est dernier en position ",minL)
    mutex.release()
    if bet == chr(ord('A')+indexPremier):
        mutex.acquire()
        move_to(31,30)
        en_couleur(lyst_colors[0])
        print("Vous avez gagné votre pari")
        mutex.release()
    else:
        mutex.acquire()
        move_to(31,30)
        en_couleur(lyst_colors[0])
        print("Vous avez perdu votre pari")
        mutex.release()

#------------------------------------------------

if __name__ == "__main__" :

    Nb_process = 20 # renseigne ne nombre de chevaux sur la ligne de départ
    mes_process = [0 for i in range(Nb_process)] # liste des processus
    mutex = Semaphore(1) # semaphore pour l'exclusion mutuelle
    Lpos = Array('b',20)

    LONGEUR_COURSE = 100 # longueur de la course
    ListeChevaux = list(chr(ord('A')+i) for i in range(Nb_process))
    print("les chevaux sur la ligne de départ sont :", ListeChevaux)
    while True:
        pari = input("Quel cheval va gagner selon vous ?")
        try:
            if pari in ListeChevaux:
                break
            raise Exception
        except:
            print("Ce cheval n'est pas sur la grille de départ")
    effacer_ecran()
    curseur_invisible()

    
    for i in range(Nb_process):  # Lancement des Nb_process processus
        mes_process[i] = Process(target=un_cheval, args= (i,LONGEUR_COURSE,mutex,Lpos,keep_running))
        mes_process[i].start()

    move_to(Nb_process+10, 1)
    print("tous lancés")
    arbitre = Process(target=arbitrage, args=(Lpos,mutex,keep_running,pari))
    arbitre.start()

    for i in range(Nb_process): mes_process[i].join()

    move_to(31, 1)
    curseur_visible()
    en_couleur(lyst_colors[0])
    print("Fini")
    