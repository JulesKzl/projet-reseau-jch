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
    add_potential_neighbours(l)

def add_potential_neighbours(l):
    """ Prends en entrée une liste de triplet (Id,IP,Port)
        et ajoute les nouveaux voisins potentiels à la variable globale
        potential_neighbourgs """
    while l != list():
        #On considère le nouvel element
        (Id,IP,port) = l[0]
        #et on le supprime de la liste initiale
        l = l[1::]
        new_neighbourg = Neighbourg(Id,IP,port)
        potential_neighbourgs = potential_neighbourgs.append(new_neighbourg)



def neighbourg_maintenance():
    """" Gère les listes de voisins """
    #Toutes les 30 secondes, on envoie des Pad0 à U et S
    return 0
    #Si |S| < 5, on envoie un paquet vide à i dans P au hasard
