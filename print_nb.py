import send
import neighbours as nb
import time
import codecs

def print_neighbours(l):
    """ Prends en entrée une liste de voisins et l'imprime """
    i = 0
    if len(l) == 0:
        print("Empty list here!")
    while i < len(l):
        n = l[i]
        print("** neighbour",i+1,"/",len(l),"**")
        print("Id :",codecs.encode(n.Id,'hex'))
        print("IP :",send.convert_bytes_to_ipv4(n.IP))
        print("Port :",send.convert_bytes_to_port(n.port))
        if (l == nb.symetric_neighbours or l == nb.unilateral_neighbours):
            print("Date :",n.date)
            print("date updated ?",time.time() - n.date)
        if l == nb.symetric_neighbours:
            print("Date_IHU :",n.date_ihu)
            print("date_ihu updated ? ",time.time() - n.date_ihu)
        i += 1

def debug_neighbours():
    print("potential_neighbours")
    print_neighbours(nb.potential_neighbours)
    print("unilateral_neighbours")
    print_neighbours(nb.unilateral_neighbours)
    print("symetric_neighbours")
    print_neighbours(nb.symetric_neighbours)
