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
    


