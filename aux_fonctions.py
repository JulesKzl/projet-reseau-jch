import socket
import types

# Prend un TLV de type 4  et renvoie une liste de triplés (id,ip,port)
def extract_neigh_from_tlv (tlv):
    if tlv[0] != 4 :
        print("il ne s'agit pas d'un 'Neighbours'")
    else :
        neigh = list()
        length = tlv[1]
        for k in range(length/26) :
            l = 26*k
            neigh = neigh + (tlv[2+l:10+l],tlv[10+l:26+l],tlv[26+l:28+l])
        return(neigh)

def extract_tlv_from_paquet (paquet):
    tlv_list = list()
    length_p = paquet[2] * 256 + paquet[3]
    curseur = 12
    while curseur-12 < 0 :
        length_tlv = curseur+1
        tlv_list = tlv_list + [l[curseur:curseur+length_tlv+2]]
        curseur = curseur + length_tlv + 2
    return(tlv_list)









