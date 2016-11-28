import socket
import types

# Prend un TLV de type 4  et renvoie une liste de triplés (id,ip,port)
def extract_neigh_from_tlv (tlv):
    if tlv[0] != 4 :
        print("il ne s'agit pas d'un 'Neighbours'")
        return(-1)
    else :
        neigh = list()
        length = tlv[1]
        for k in range(length//26) :
            l = 26*k
            neigh.append((tlv[2+l:10+l],tlv[10+l:26+l],tlv[26+l:28+l]))
        return(neigh)

# Prend un paquet et renvoie la liste des TLV encapsulés dedans
def extract_tlv_from_paquet (paquet):
    tlv_list = list()
    length_p = paquet[2] * 256 + paquet[3]
    curseur = 12
    while curseur-12 < length_p :
        length_tlv = paquet[curseur+1]
        tlv_list = tlv_list + [paquet[curseur:curseur+length_tlv+2]]
        curseur = curseur + length_tlv + 2
    return(tlv_list)

# Renvoie le type d'un tlv (int)
def find_tlv_type (tlv):
    return (tlv[0])

# Renvoie l'id de l'emetteur du paquet (bytes)
def get_id_from_paquet (paquet):
    return(paquet[4:12])

# Renvoie la longueur du paquet (int)
def get_length_of_paquet (paquet):
    return(paquet[2]*256 + paquet[3])

def bidon() :
    return (0)



