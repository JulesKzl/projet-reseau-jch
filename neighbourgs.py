""" On gère les opérations relatives aux voisins """
import time

class Neighbourg:
    """Classe définissant un neighbourg :
    - son Id
    - son IP
    - son port
    - son age (dernier paquet reçu)
    - son age_IHU (dernier TLV IHU reçu)"""

    def __init__(self, Id, IP, port):
        """Constructeur de la classe"""
        self.Id = Id
        self.IP = IP
        self.port = port
        self.date = time.time()

#La liste contenant les voisins potentiels
potential_neighbourgs = list()
#La liste contenant les voisins unilateraux
unilateral_neighbourgs = list()
#La liste contenant les voisins bilateraux
symetric_neighbourgs = list()


def initialize_neighbourg(l):
    """ On part avec les noeuds de bootstrap"""
    add_neighbours(l,potential_neighbourgs)

def add_neighbours(l,v):
    """ Prends en entrée une liste l de triplet (Id,IP,Port) et la liste voisins
        v considérée et ajoute les nouveaux voisins potentiels à la variable globale
        potential_neighbourgs """
    while l != list():
        #On considère le nouvel element
        (Id,IP,port) = l[0]
        #et on le supprime de la liste initiale
        l = l[1::]
        new_neighbourg = Neighbourg(Id,IP,port)
        new_neighbourg.date = time.time()
        if v == symetric_neighbourgs:
            new_neighbourg.date_ihu = time.time()
        v = v.append(new_neighbourg)


def print_neighbourgs(l):
    """ Prends en entrée une liste de voisins et l'imprime """
    i = 0
    if len(l) == 0:
        print("Empty list here!")
    while i < len(l):
        n = l[i]
        print("** Neighbourg",i+1,"/",len(l),"**")
        print("Id :",n.Id.hex())
        print("IP :",n.IP)
        print("Port :",n.port)
        print("Date :",n.date)
        print("date updated ? "time.time() - n.date())
        i += 1


def new_unilateral_neighbourg(new_Id,new_IP,new_port):
    """ Quand on recoit un nouveau message, on met à jour nos listes de
    voisins """
    #On parcourt la liste des S : si S contient Id, on modifie sa date
    l = symetric_neighbourgs
    n = len(l)
    i = 0
    while i < n:
        neighbourg = l[i]
        if neighbourg.Id == new_Id:
            #On met à jour la date
            neighbourg.date = time.time()
            #On sort de la boucle
            i = n
            print("new Id is already in symetric_neighbourgs, date updated")
            return 0
        else:
            i += 1
    print("new Id is not in symetric_neighbourgs, let's visiting unilateral")
    #On parcourt la liste des U : si U contient Id, on modifie sa date,
    #sinon on l'y ajoute
    l = unilateral_neighbourgs
    n = len(l)
    i = 0
    while i < n:
        neighbourg = l[i]
        if neighbourg.Id == new_Id:
            #On met à jour la date
            neighbourg.date = time.time()
            #On sort de la boucle
            i = n
            print("new Id is already in unilateral_neighbourgs, date updated")
            return 0
        else:
            i += 1
    print("new Id is not in unilateral_neighbourgs, let's add it in")
    add_neighbours([(new_Id,new_IP,new_port)],unilateral_neighbourgs)
    #On le supprime des potential_neighbourgs s'il y est
    l = potential_neighbourgs
    n = len(l)
    i = 0
    while i < n:
        neighbourg = l[i]
        if neighbourg.Id == new_Id:
            del(l[i])
            print("new Id was in potential_neighbourgs, yet no more")
            return 0
        else:
            i += 1
    print("new Id was not in potential_neighbourgs anyway")


def new_symetric_neighbourg(new_Id,new_IP,new_port):
    """ Quand on recoit un nouveau IHU, on met à jour nos listes de
    voisins """
    #On parcourt la liste des S : si S contient Id, on modifie ses dates
    l = symetric_neighbourgs
    n = len(l)
    i = 0
    while i < n:
        neighbourg = l[i]
        if neighbourg.Id == new_Id:
            #On met à jour la date
            neighbourg.date = time.time()
            neighbourg.date_ihu = time.time()
            #On sort de la boucle
            i = n
            print("new Id is already in symetric_neighbourgs, date updated")
            return 0
        else:
            i += 1
    print("new Id is not in symetric_neighbourgs, let's add it in")
    add_neighbours([(new_Id,new_IP,new_port)],symetric_neighbourgs)
    #On parcourt la liste des U : si U contient Id, on modifie sa date,
    #on l'ajoute dans S et on le supprime de U
    l = unilateral_neighbourgs
    n = len(l)
    i = 0
    while i < n:
        neighbourg = l[i]
        if neighbourg.Id == new_Id:
            del(l[i])
            #On sort de la boucle
            i = n
            print("new Id was in unilateral_neighbourgs, yet no more")
            return 0
        else:
            i += 1
    print("new Id was not in unilateral_neighbourgs anyway")
    #On le supprime aussi des potential_neighbourgs s'il y est
    l = potential_neighbourgs
    n = len(l)
    i = 0
    while i < n:
        neighbourg = l[i]
        if neighbourg.Id == new_Id:
            del(l[i])
            print("new Id was in potential_neighbourgs, yet no more")
            return 0
        else:
            i += 1
    print("new Id was not in potential_neighbourgs anyway")

def debug_neighbourgs():
    print("potential_neighbourgs")
    print_neighbourgs(potential_neighbourgs)
    print("unilateral_neighbourgs")
    print_neighbourgs(unilateral_neighbourgs)
    print("symetric_neighbourgs")
    print_neighbourgs(symetric_neighbourgs)


def neighbourg_maintenance():
    """" Gère les listes de voisins """
    #Toutes les 30 secondes, on envoie des Pad0 à U et S
    return 0
    #Si |S| < 5, on envoie un paquet vide à i dans P au hasard
