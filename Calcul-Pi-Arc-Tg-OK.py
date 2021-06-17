# Calcul de PI par la loi Normale
import multiprocessing as mp
from multiprocessing.context import Process
import random, time
# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
start_time = time.time()
from math import *
 
def arc_tangente(d,f,k,sem,N):
    py = 0  # variable permettant de stocker la somme partielle de pi caculculé par les différents processus
    for i in range(d,f):
        py += 4/(1+ ((i+0.5)/N)**2)
    sem.acquire()
    k.value += py/N   # ajout dans la variable partagé de la somme partielle calculée
    sem.release()
    

if __name__ == "__main__" :
    k=mp.Value("d",0.0)
    sem=mp.Semaphore(1) # semaphore permettant de verouiller l'accès à la variable partagée
    N= 10**6
    Nb_process = 4  # choix du nombre du processus pour calculer la valeur de pi 
    mes_process = [0 for i in range(Nb_process)]
    for i in range(Nb_process):  
        mes_process[i] = Process(target=arc_tangente, args= (int(i*N/Nb_process),floor(((i+1)*N -1)/ Nb_process),k,sem,N))
        mes_process[i].start()
        mes_process[i].join()
    
    print("Valeur estimée Pi par la méthode Tangente : ", k.value)
    print("Temps d'execution : ", time.time() - start_time)




    



