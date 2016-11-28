import socket
import types
import aux_fonctions as af

HOST_JCH = '2001:660:3301:9200::51c2:1b9b'
HOST_SELF= '::'
PORT_BOOT = 1212
PORT_SELF = 1312
BOOTSRAP_JCH = bytes.fromhex('6722a421aadb51bd') 
ENTETE = bytes([57,0,0,2,22,4,19,94,29,12,19,94]) 
SUITE = bytes([3,0])

# envoie une neighour request à qqn et récupère la liste de triplés
def main ():
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    s.bind((HOST_SELF,PORT_SELF))
    while True :
        s.sendto(ENTETE + SUITE + BOOTSRAP_JCH , (HOST_JCH,PORT_BOOT))
        mess = s.recvfrom(4096)
        tlv_list = af.extract_tlv_from_paquet(mess[0])
        if len(tlv_list) == 0 :
            print("c'est plutôt raté")
        else :
            print(af.find_tlv_type(tlv_list[0]))
            neigh = af.extract_neigh_from_tlv (tlv_list[0])
            if len(neigh) == 0 :
                print("on n'a pas de voisins ??")
            else :
                return (neigh)


if __name__ == "__main__":
    main ()
