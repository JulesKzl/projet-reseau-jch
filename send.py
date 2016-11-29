import socket
import types
import time
import neighbours
import const as c
import data

US = c.Id

def convert_ipv4_to_bytes(ipv4):
    ip_as_bytes = bytes(map(int, ipv4.split('.')))
    en_tete = bytes.fromhex('00000000000000000000ffff')
    return(en_tete + ip_as_bytes)

def convert_port_to_bytes(p):
    return bytes([p//256,p%256])

def convert_bytes_to_ipv4(b):
    return (str(b[12]) + '.' + str(b[13]) + '.' + str(b[14]) + '.'+str(b[15]))

def convert_bytes_to_port(b):
    return (str(256*b[0]+b[1]))

def make_entete (length):
    return(bytes([57,0,(length // 256),(length % 256)])+US)

def send_pad1 (sock,neigh):
    IP = convert_bytes_to_ipv4(neigh.IP)
    port = int(convert_bytes_to_port(neigh.port))
    sock.sendto(make_entete(1) + bytes([0]) , (IP,port))
    print("PAD1 sent to",IP,":",port)

def send_empty (sock,neigh):
    IP = convert_bytes_to_ipv4(neigh.IP)
    port = int(convert_bytes_to_port(neigh.port))
    sock.sendto(make_entete(0) , (IP,port))
    print("NOTHING sent to",IP,":",port)


def make_ihu (Id):
    return(bytes([2,8]) + Id)
def send_ihu (sock,neigh):
    IP = convert_bytes_to_ipv4(neigh.IP)
    port = int(convert_bytes_to_port(neigh.port))
    sock.sendto(make_entete (10) + make_ihu(neigh.Id) , (IP,port))
    print("IHU sent to",IP,":",port)


def make_nr ():
    return(bytes([3,0]))
def send_nr (sock,neigh):
    IP = convert_bytes_to_ipv4(neigh.IP)
    port = int(convert_bytes_to_port(neigh.port))
    sock.sendto(make_entete(2) + make_nr() , (IP,port))
    print("NR sent to",IP,":",port)


def make_neighbours (neigh_list):
    l = len(neigh_list)
    length = 26 * l
    tlv = bytes([4,length])
    for k in range (l):
        neigh = neigh_list[k]
        tlv = tlv + neigh.Id + neigh.IP + neigh.port
    return(tlv)
def send_neighbours (sock,neigh,neigh_list):
    IP = convert_bytes_to_ipv4(neigh.IP)
    port = int(convert_bytes_to_port(neigh.port))
    sock.sendto(make_entete(2+26*len(neigh_list)) + make_neighbours(neigh_list) , (IP,port))
    print("NEIGHBOURS sent to",IP,":",port)

def answer_nr(sock,id_sender,ip_sender,port_sender):
    print("We will respond to NR")
    neigh = Neighbour(id_sender,ip_send,port_sender)
    send_neighbours(sock,neigh,nb.symetric_neighbours)

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
    return(bytes([6,12])+seqno+Id)
def send_Ihave (sock,IP,port,tlv):
    seqno = tlv[2:6]
    Id = tlv[6:14]
    sock.sendto(make_entete(14) + make_Ihave(seqno,Id) , (IP,port))
    print("I HAVE sent to",IP,":",port)
