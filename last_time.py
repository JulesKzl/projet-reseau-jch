import time
from random import randint
import neighbours as nb
import send

#maintenance des voisins
date_send_neighbours_pad1 = time.time()
date_send_neighbours_ihu = time.time()
date_delete_old_neighbours = time.time()
date_enough_potential_neighbours = time.time()
#maintenance des données
date_delete_old_data = time.time()
date_pulish_date = time.time()
#incrementer sequeno
date_publi = time.time()

def send_neighbours_pad1(sock,neigh):
    """" Toutes les 30 secondes, on envoie des Pad1 à U et S
         Si |S| < 5, on envoie un paquet vide à i dans P au hasard """
    now = time.time()
    global date_send_neighbours_pad1
    if now - date_send_neighbours_pad1 > 30. :
        print("On envoie des Pad1 à U et S")
        #On envoie à tous les voisins unilateraux
        for n in nb.unilateral_neighbours:
            send.send_pad1(sock,neigh)
        #On envoie à tous les voisins symétriques
        for n in nb.symetric_neighbours:
            send.send_pad1(sock,neigh)
        #On regarde si |S| < 5
        if len(nb.symetric_neighbours) < 5:
            print("We have less than 5 symetrics neighbours")
            #On envoie un paquet vide à un P au hasard (pour qu'il nous ajoute
            #dans son unilateral stp)
            if nb.potential_neighbours != list():
                x = randint(0,len(nb.potential_neighbours)-1)
                n = nb.potential_neighbours[x]
                send.send_empty(sock,neigh)
        #On termine par réinitialiser la date de dernière mise à jour
        date_send_neighbours_pad1 = time.time()

def time_publi ():
    now = time.time()
    if now - date_publi > 1800. :
        # publie (now)
        return 0

def publie(date):
    date_publi = date
    #incr_seqno()
    #innonde ()
