# Calcul de PI par la loi Normale
import multiprocessing as mp
import random, time
# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
start_time = time.time()
from math import *
 
def arc_tangente(n):
    pi = 0
    for i in range(n):
        pi += 4/(1+ ((i+0.5)/n)**2)
    return (1/n)*pi
    

if __name__ == "__main__" :
    # Nombre d’essai pour l’estimation
    nb_total_iteration = 1000000
    #nb_hits=frequence_de_hits_pour_n_essais(nb_total_iteration)
    result = arc_tangente(nb_total_iteration)
    print("Valeur estimée Pi par la méthode Tangente : ", result)
    print("Temps d'execution : ", time.time() - start_time)



