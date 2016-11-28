import socket
import types
import time
import neighbours
import const as c

US = c.Id

def make_entete (length):
    return(bytes([57,0,(length // 256),(length % 256)])+US)

def send_pad1 (sock,neigh):
    sock.sendto(make_entete(1) + bytes([0]) , (neigh.port,neigh.IP))

def send_empty (sock,neigh):
    sock.sendto(make_entete(0) , (neigh.port,neigh.IP))


def make_ihu (Id):
    return(bytes([2,8]) + Id)
def send_ihu (sock,neigh):
    sock.sendto(make_entete (10) + make_ihu(neigh.Id) , (neigh.port,neigh.IP))


def make_nr ():
    return(bytes([3,0]))
def send_nr (sock,neigh):
    sock.sendto(make_entete(2) + make_nr() , (neigh.port,neigh.IP))
    

def make_neighbours (neigh_list):
    l = len(neigh_list)
    length = 26 * l
    tlv = bytes([4,length])
    for k in range (l):
        neigh = neigh_list[k]
        tlv := tlv + neigh.Id + neigh.IP + neigh.port
    return(tlv)
def send_neighbours (sock,neigh,neigh_list):
    sock.sendto(make_entete(2+26*len(neigh_list)) + make_neighbours(neigh_list) , (neigh.port,neighIP))








