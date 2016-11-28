import socket
import types
import time
import neighbours
import const as c
import data

US = c.Id

def make_entete (length):
    return(bytes([57,0,(length // 256),(length % 256)])+US)

def send_pad1 (sock,neigh):
    sock.sendto(make_entete(1) + bytes([0]) , (neigh.IP,neigh.port))
    print("PAD1 sent to",neigh.IP,":",neigh.port)

def send_empty (sock,neigh):
    sock.sendto(make_entete(0) , (neigh.IP,neigh.port))
    print("NOTHING sent to",neigh.IP,":",neigh.port)


def make_ihu (Id):
    return(bytes([2,8]) + Id)
def send_ihu (sock,neigh):
    sock.sendto(make_entete (10) + make_ihu(neigh.Id) , (neigh.IP,neigh.port))
    print("IHU sent to",neigh.IP,":",neigh.port)


def make_nr ():
    return(bytes([3,0]))
def send_nr (sock,neigh):
    sock.sendto(make_entete(2) + make_nr() , (neigh.IP,neigh.port))
    print("NR sent to",neigh.IP,":",neigh.port)


def make_neighbours (neigh_list):
    l = len(neigh_list)
    length = 26 * l
    tlv = bytes([4,length])
    for k in range (l):
        neigh = neigh_list[k]
        tlv = tlv + neigh.Id + neigh.IP + neigh.port
    return(tlv)
def send_neighbours (sock,neigh,neigh_list):
    sock.sendto(make_entete(2+26*len(neigh_list)) + make_neighbours(neigh_list) , (neigh.IP,neigh.port))
    print("NEIGHBOURS sent to",neigh.IP,":",neigh.port)



def make_data (Id):
    tupl = data.datas.get(Id)
    data = tupl[0]
    seqno = tupl[2]
    length = len(data) + 12
    if length + 14 > 4096:
        print("cette donnée est trop grosse, je refuse de l'envoyer !")
    else :
        return(bytes([5,length,seqno])+Id+data)
def send_data (sock,neigh,Id):
    length = len(data.datas.get(Id)[0]) + 14
    corps = make_data(Id)
    if corps :
        sock.sendto(make_entete(length) + make_data(Id) , (neigh.IP,neigh.port))
        print("DATA sent to",neigh.IP,":",neigh.port)



def make_Ihave (seqno,Id):
    return(bytes([6,12,seqno//256,seqno%256])+Id)
def send_Ihave (sock,ip,port,tlv):
    seqno = tlv[2:6]
    Id = tlv[6:14]
    sock.sendto(make_entete(14) + make_Ihave(seqno,Id) , (neigh.IP,neigh.port))
    print("I HAVE sent to",neigh.IP,":",neigh.port)















