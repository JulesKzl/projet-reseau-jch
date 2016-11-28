import time

#maintenance des voisins
date_send_pad1 = time.time()
date_send_ihu = time.time()
date_delete_old_neighbours = time.time()
date_enough_potential_neighbours = time.time()
#maintenance des données
date_delete_old_data = time.time()
date_pulish_date = time.time()
#incrementer sequeno
date_publi = time.time()

def send_pad1():
    """" Toutes les 30 secondes, on envoie des Pad1 à U et S
         Si |S| < 5, on envoie un paquet vide à i dans P au hasard """
    now = time.time()
    if now - date_publi > 30. :
        print("On envoie des Pad1 à U et S")
        #On envoie à tous les voisins unilateraux
        for n in unilateral_neighbourgs:
            send_pad1()
        #On envoie à tous les voisins symétriques
        for n in unilateral_neighbourgs:
            send_pad1()


def time_publi ():
    now = time.time()
    if now - date_publi > 1800. :
        # publie (now)
        return 0

def publie(date):
    date_publi = date
    #incr_seqno()
    #innonde ()
