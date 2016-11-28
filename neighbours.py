""" On gère les opérations relatives aux voisins """
import time
import const as c
import send

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
        v considérée et ajoute les nouveaux voisins l à la variable globale v"""
    while l != list():
        #On considère le nouvel element
        (Id,IP,port) = l[0]
        #et on le supprime de la liste initiale
        l = l[1::]
        #Assurons nous de ne pas être dans la liste de voisins...
        if Id != c.Id:
            new_neighnour = Neighnour(Id,IP,port)
            #Si on est dans S ou U, alors on associe une date
            if (v == symetric_neighbours or v == unilateral_neighbours):
                new_neighnour.date = time.time()
            #Si on est dans S, on associe une date de dernier IHU reçu
            if v == symetric_neighbours:
                new_neighnour.date_ihu = time.time()
            v.append(new_neighnour)
        else:
            print("I was in the possibly neighbours")

def add_potential_neighbours(l):
    """ Prends en entrée une liste l de triplet (Id,IP,Port)et ajoute les
        nouveaux voisins l à potential_neighbours sans doublon avec les autres
        listes de voisins """
    #liste sans doublon qu'on ajoutera à potential_neighbours
    l2 = list()
    #On parcourt notre liste d'entrée pour unilateral_neighbours
    l1 = list()
    print("len l =",len(l))
    if unilateral_neighbours != list():
        while l != list():
            for n in unilateral_neighbours:
                if n.Id != (l[0])[0]:
                    l1.append(l[0])
            del l[0]
    else:
        l1 = l
    print("len l1 = ",len(l1))
    if symetric_neighbours != list():
        while l1 != list():
            for n in symetric_neighbours:
                if n.Id != (l1[0])[0]:
                    l2.append(l1[0])
            del l1[0]
    else:
        l2 = l1
    print("In reality,",len(l2),"new neighbours")
    #On ajoute les nouveaux noeuds dans potential_neighbours
    add_neighbours(l2,potential_neighbours)



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

# def answer_nr(sock,id_sender,ip_sender,port_sender)
#     neigh = Neighbour(id_sender,ip_send,port_sender)
#
#     send.send_neighbours(sock,neigh,neigh_list):

# neigh.IP b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xa4\x84j\x07'
# neigh.port b'\x04\xa8'

def new_unilateral_neighbour(new_Id,new_IP,new_port):
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


def new_symetric_neighbour(new_Id,new_IP,new_port):
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
