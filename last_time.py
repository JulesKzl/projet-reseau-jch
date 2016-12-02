""" Dans ce package se situent les fonctions appelées périodiquement """

import time
from random import randint
import neighbours as nb
import send

#maintenance des voisins
date_send_neighbours_pad1 = time.time()
date_send_neighbours_ihu = time.time()
date_clean_neighbours = time.time()
date_last_nr = time.time()
#maintenance des données
date_delete_old_data = time.time()
date_pulish_date = time.time()
#incrementer sequeno
date_publi = time.time()

def send_neighbours_pad1(sock):
    """" Toutes les 30 secondes, on envoie des Pad1 à U et S
         Si |S| < 5, on envoie un paquet vide à i dans P au hasard """
    now = time.time()
    global date_send_neighbours_pad1
    if now - date_send_neighbours_pad1 > 30. :
        print("Pad1 will be send to U and S")
        #On envoie à tous les voisins unilateraux
        print("number of unilateral neighbours=",len(nb.unilateral_neighbours))
        for neigh in nb.unilateral_neighbours:
            send.send_pad1(sock,neigh)
        #On envoie à tous les voisins symétriques
        for neigh in nb.symetric_neighbours:
            send.send_pad1(sock,neigh)
        #On regarde si |S| < 5
        if len(nb.symetric_neighbours) < 5:
            print("We have",len(nb.symetric_neighbours),"< 5 symetrics neighbours ")
            #On envoie un paquet vide à un P au hasard (pour qu'il nous ajoute
            #dans son unilateral stp)
            if nb.potential_neighbours != list():
                print("Potential list not empty, Empty msg will be send")
                x = randint(0,len(nb.potential_neighbours)-1)
                neigh = nb.potential_neighbours[x]
                send.send_empty(sock,neigh)
            else:
                print("but the potential_neighbours is empty")
        #On termine par réinitialiser la date de dernière mise à jour
        date_send_neighbours_pad1 = time.time()

def send_neighbours_ihu(sock):
    """" Toutes les 90 secondes, on envoie des IHU à U et S """
    now = time.time()
    global date_send_neighbours_ihu
    if now - date_send_neighbours_ihu > 90. :
        print("IHU will be send to U et S")
        #On envoie à tous les voisins unilateraux
        for neigh in nb.unilateral_neighbours:
            send.send_ihu(sock,neigh)
        #On envoie à tous les voisins symétriques
        for neigh in nb.symetric_neighbours:
            send.send_ihu(sock,neigh)
        #On termine par réinitialiser la date de dernière mise à jour
        date_send_neighbours_ihu = time.time()

def send_neighbours_nr(sock):
    """" Toutes les 5 minutes, on envoie un NR à un S au hasard """
    now = time.time()
    global date_last_nr
    if now - date_last_nr > 300./10. :
        print("************************************************")
        print("************************************************")
        print("We will send Neighbour Request to a member of S")
        print("************************************************")
        print("************************************************")
        if len(nb.potential_neighbours) < 5:
            print("We have less than 5 potentials neighbours")
            #On envoie un NR à un S au hasard
            if nb.symetric_neighbours != list():
                print("Symetric list not empty, NR will be send")
                x = randint(0,len(nb.symetric_neighbours)-1)
                neigh = nb.symetric_neighbours[x]
                send.send_nr(sock,neigh)
            else:
                print("but the symetric_neighbours list is empty, nothing sent")
        #On termine par réinitialiser la date de dernière mise à jour
        date_last_nr = time.time()


def maintenance_neighbours(sock):
    send_neighbours_pad1(sock)
    send_neighbours_ihu(sock)
    send_neighbours_nr(sock)
    #TODO clean old neigbourg

def time_publi ():
    now = time.time()
    if now - date_publi > 1800. :
        # publie (now)
        return 0

def publie(date):
    date_publi = date
    #incr_seqno()
    #innonde ()
