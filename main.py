import socket
import types
import aux_fonctions as af

import last_time
import neighbourgs as nb

#en IPv4
#IP de Juliusz
HOST_JCH = '81.194.27.155'
#toutes les IP
HOST_SELF= '0.0.0.0'
#Port de Juliusz
PORT_JCH = 1212
#Notre port
PORT_SELF = 1512
#Id de Juliusz
Id_JCH = bytes.fromhex('6722a421aadb51bd')

#Magic et Version
ENTETE_UDP = bytes([57,0])

#TODO rendre l'Id aléatoire (à la fin, d'abord les tests)
#Id_Jules
Id = bytes([22,4,19,95,29,12,19,95])
#Id_Gab
#Id = bytes(22,4,19,94,29,12,19,94])



def make_IHU(Id1,Id2):
    """ Créer un IHeardYou d'une Id1 vers une Id2 """
    IHU = bytes([2,8])
    length_IHU = bytes([0,10])
    return ENTETE_UDP + length_IHU + Id1 + IHU + Id2



def main():
    #On crée la socket pour se connecter à Juliusz
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST_SELF,PORT_SELF))
    #On initialise nos voisins grâce à nos bootstrap
    nb.initialize_neighbourg([(Id_JCH,HOST_JCH,1212)])
    #On envoie un IHU à nos bootstrap (ici Juliusz)
    s.sendto(make_IHU(Id,Id_JCH), (HOST_JCH,PORT_JCH))
    print('IHU send to',HOST_JCH,":",PORT_JCH)

    #Boucle principale
    while True :
        #On recoit un paquet UDP de taille maximale 4096
        message,(ip_sender,port_sender) = s.recvfrom(4096)
        id_sender = af.get_id_from_paquet(message)
        print("New UDP paquet received, from ",ip_sender,":",port_sender\
        ,"with Id :",id_sender.hex())
        print("Message :",message)
        print("Body length of message :",af.get_length_of_paquet(message))

        #On mets à jour les voisins car on a reçu un nouveau paquet
        nb.new_unilateral_neighbourg(id_sender,ip_sender,port_sender)
        print("Extraction of TLV from UDP paquet ...")

        # On extrait les TLV dans une liste tlv_list
        tlv_list = af.extract_tlv_from_paquet(message)
        n = len(tlv_list) #n est le la taille de tlv_list, soit le nbr de TLV
        print(n," TLV found !")

        #On traite le TLV selon son type
        i = 1 #On incrémentera i à chaque nouveau TLV exploré
        while tlv_list != list():
            tlv = tlv_list[0]
            tlv_type = af.find_tlv_type(tlv)
            print("TLV",i,"/",n,"of type",tlv_type,"is going to be explore")
            if tlv_type == 0:
                #Le TLV Pad0 est ignoré à la récéption
                print("TLV Pad0 received")
            if tlv_type == 1:
                #Le TLV PadN est ignoré à la récéption
                print("TLV PadN received")
            if tlv_type == 2:
                #On a reçu un IHU
                print("TLV IHU received")
                #On mets à jour les voisins (unilatéral deviennent symétrique)
                nb.new_symetric_neighbourg(id_sender,ip_sender,port_sender)
            if tlv_type == 3:
                #On a reçu un Neighbour Request
                print("TLV Neighbour Request received")
                #TODO On envoie un TLV Neighbours à l'emetteur contenant
                #au moins 5 voisins symétriques
            if tlv_type == 4:
                #On a reçu un Neighbours
                print("TLV Neighbours received")
                new_neighbours = af.extract_neigh_from_tlv(tlv)
                #On extrait les voisins sous forme d'une liste de triplés
                #TODO on repeuple nos voisins potentiels
            if tlv_type == 5:
                #On a reçu des données !
                print("TLV Data received !")
                #TODO on appelle update_data pour modifier nos données
                #TODO on envoie un IHave pour la donnée
            if tlv_type == 6:
                #On a reçu un IHave
                print("TLV IHave received !")
                #cf inondation je sais pas encore trop

            #On a traité le TLV, on le supprime de la liste courante
            print("TLV",i,"/",n,"has been explored")
            i += 1
            tlv_list = tlv_list[1:]
        #TODO On regarde si on doit inonder ou non (cf plus tard)
        #TODO choses à executer pérodiquement


if __name__ == "__main__":
    main ()
