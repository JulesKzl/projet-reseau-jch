""" On gère les opérations relatives aux voisins """
import time

class Neighnour:
    """Classe définissant un neighnour :
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
potential_neighbours = list()
#La liste contenant les voisins unilateraux
unilateral_neighbours = list()
#La liste contenant les voisins bilateraux
symetric_neighbours = list()


def initialize_neighnour(l):
    """ On part avec les noeuds de bootstrap"""
    add_neighbours(l,potential_neighbours)

def add_neighbours(l,v):
    """ Prends en entrée une liste l de triplet (Id,IP,Port) et la liste voisins
        v considérée et ajoute les nouveaux voisins potentiels à la variable globale
        v"""
    while l != list():
        #On considère le nouvel element
        (Id,IP,port) = l[0]
        #et on le supprime de la liste initiale
        l = l[1::]
        new_neighnour = Neighnour(Id,IP,port)
        #Si on est dans S ou U, alors on associe une date
        if (v == symetric_neighbours or v == unilateral_neighbours):
            new_neighnour.date = time.time()
        #Si on est dans S, on associe une date de dernier IHU reçu
        if v == symetric_neighbours:
            new_neighnour.date_ihu = time.time()
        v = v.append(new_neighnour)


def print_neighbours(l):
    """ Prends en entrée une liste de voisins et l'imprime """
    i = 0
    if len(l) == 0:
        print("Empty list here!")
    while i < len(l):
        n = l[i]
        print("** Neighnour",i+1,"/",len(l),"**")
        print("Id :",n.Id.hex())
        print("IP :",n.IP)
        print("Port :",n.port)
        if (l == symetric_neighbours or l == unilateral_neighbours):
            print("Date :",n.date)
            print("date updated ?",time.time() - n.date)
        if l == symetric_neighbours:
            print("Date_IHU :",n.date_ihu)
            print("date_ihu updated ? ",time.time() - n.date_ihu)
        i += 1


def new_unilateral_neighnour(new_Id,new_IP,new_port):
    """ Quand on recoit un nouveau message, on met à jour nos listes de
    voisins """
    #On parcourt la liste des S : si S contient Id, on modifie sa date
    l = symetric_neighbours
    n = len(l)
    i = 0
    while i < n:
        neighnour = l[i]
        if neighnour.Id == new_Id:
            #On met à jour la date
            neighnour.date = time.time()
            #On sort de la boucle
            i = n
            print("new Id is already in symetric_neighbours, date updated")
            return 0
        else:
            i += 1
    print("new Id is not in symetric_neighbours, let's visiting unilateral")
    #On parcourt la liste des U : si U contient Id, on modifie sa date,
    #sinon on l'y ajoute
    l = unilateral_neighbours
    n = len(l)
    i = 0
    while i < n:
        neighnour = l[i]
        if neighnour.Id == new_Id:
            #On met à jour la date
            neighnour.date = time.time()
            #On sort de la boucle
            i = n
            print("new Id is already in unilateral_neighbours, date updated")
            return 0
        else:
            i += 1
    print("new Id is not in unilateral_neighbours, let's add it in")
    add_neighbours([(new_Id,new_IP,new_port)],unilateral_neighbours)
    #On le supprime des potential_neighbours s'il y est
    l = potential_neighbours
    n = len(l)
    i = 0
    while i < n:
        neighnour = l[i]
        if neighnour.Id == new_Id:
            del(l[i])
            print("new Id was in potential_neighbours, yet no more")
            return 0
        else:
            i += 1
    print("new Id was not in potential_neighbours anyway")


def new_symetric_neighnour(new_Id,new_IP,new_port):
    """ Quand on recoit un nouveau IHU, on met à jour nos listes de
    voisins """
    #On parcourt la liste des S : si S contient Id, on modifie ses dates
    l = symetric_neighbours
    n = len(l)
    i = 0
    while i < n:
        neighnour = l[i]
        if neighnour.Id == new_Id:
            #On met à jour la date
            neighnour.date = time.time()
            neighnour.date_ihu = time.time()
            #On sort de la boucle
            i = n
            print("new Id is already in symetric_neighbours, date updated")
            return 0
        else:
            i += 1
    print("new Id is not in symetric_neighbours, let's add it in")
    add_neighbours([(new_Id,new_IP,new_port)],symetric_neighbours)
    #On parcourt la liste des U : si U contient Id, on modifie sa date,
    #on l'ajoute dans S et on le supprime de U
    l = unilateral_neighbours
    n = len(l)
    i = 0
    while i < n:
        neighnour = l[i]
        if neighnour.Id == new_Id:
            del(l[i])
            #On sort de la boucle
            i = n
            print("new Id was in unilateral_neighbours, yet no more")
            return 0
        else:
            i += 1
    print("new Id was not in unilateral_neighbours anyway")
    #On le supprime aussi des potential_neighbours s'il y est
    l = potential_neighbours
    n = len(l)
    i = 0
    while i < n:
        neighnour = l[i]
        if neighnour.Id == new_Id:
            del(l[i])
            print("new Id was in potential_neighbours, yet no more")
            return 0
        else:
            i += 1
    print("new Id was not in potential_neighbours anyway")

def debug_neighbours():
    print("potential_neighbours")
    print_neighbours(potential_neighbours)
    print("unilateral_neighbours")
    print_neighbours(unilateral_neighbours)
    print("symetric_neighbours")
    print_neighbours(symetric_neighbours)
