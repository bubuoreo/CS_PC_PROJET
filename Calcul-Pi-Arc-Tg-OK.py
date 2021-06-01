# Calcul de PI par la loi Normale
import multiprocessing as mp
from multiprocessing.context import Process
import random, time
# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
start_time = time.time()
from math import *
 
def arc_tangente(d,f,k,sem):
    py = 0
    print(d,f)
    for i in range(d,f):
        py += 4/(1+ ((i+0.5)/f)**2)
    sem.acquire()
    k.value += (1/f)*py
    sem.release()
    

if __name__ == "__main__" :
    k=mp.Value('d',0)
    sem=mp.Semaphore(1)
    N= 10**6
    Nb_process = 4
    mes_process = [0 for i in range(Nb_process)]
    for i in range(Nb_process):  # Lancer     Nb_process  processus
            mes_process[i] = Process(target=arc_tangente, args= (int((i*N/4)),floor(((i+1)*N-1)/4),k,sem))
            mes_process[i].start()
    
    for i in range(Nb_process): mes_process[i].join()
    
    print("Valeur estimée Pi par la méthode Tangente : ", k.value)
    print("Temps d'execution : ", time.time() - start_time)




    



