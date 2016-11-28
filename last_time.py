import time

#maintenance des voisins
date_new_unilateral_neighbours = time.time()
date_new_symetric_neighbours = time.time()
date_delete_old_neighbours = time.time()
date_enough_potential_neighbours = time.time()
#maintenance des données
date_delete_old_data = time.time()
date_pulish_date = time.time()
#incrementer sequeno
date_publi = time.time()



def time_publi ():
    now = time.time()
    if now - date_publi > 1800. :
        # publie (now)
        return 0

def publie(date):
    date_publi = date
    #incr_seqno()
    #innonde ()
