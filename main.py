import socket
import types

import aux_fonctions as af
import last_time as lt
import neighbours as nb
import const as c
import send
import data


def main():
    #On crée la socket pour se connecter à Juliusz
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((c.HOST_SELF,c.PORT_SELF))
    #On initialise nos voisins grâce à nos bootstrap
    nb.initialize_neighnour([(c.Id_JCH,c.HOST_JCH,c.PORT_JCH)])
    #On envoie un IHU à nos bootstrap (ici Juliusz)
    for neigh in nb.potential_neighbours:
        send.send_ihu (s,neigh)

    #Boucle principale
    while True :
        #On recoit un paquet UDP de taille maximale 4096
        message,(ip_sender,port_sender) = s.recvfrom(4096)
        print("Type=",type(ip_sender))
        id_sender = af.get_id_from_paquet(message)
        print("New UDP paquet received, from ",ip_sender,":",port_sender\
        ,"with Id :",id_sender.hex())
        print("Message :",message)
        print("Body length of message :",af.get_length_of_paquet(message))

        #On mets à jour les voisins car on a reçu un nouveau paquet
        nb.new_unilateral_neighbour(id_sender,ip_sender,port_sender)

        # On extrait les TLV dans une liste tlv_list
        print("Extraction of TLV from UDP paquet ...")
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
                #Le TLV Pad1 est ignoré à la récéption
                print("TLV Pad1 received")
            if tlv_type == 1:
                #Le TLV PadN est ignoré à la récéption
                print("TLV PadN received")
            if tlv_type == 2:
                #On a reçu un IHU
                print("TLV IHU received")
                #On mets à jour les voisins (unilatéral deviennent symétrique)
                nb.new_symetric_neighbour(id_sender,ip_sender,port_sender)
            if tlv_type == 3:
                #On a reçu un Neighbour Request
                print("TLV Neighbour Request received")
                #TODO On envoie un TLV Neighbours à l'emetteur contenant
                #au moins 5 voisins symétriques
                #nb.answer_nr(s,id_sender,ip_sender,port_sender)
            if tlv_type == 4:
                #TODEBUG
                #On a reçu un Neighbours
                print("TLV Neighbours received")
                #On extrait les voisins sous forme d'une liste de triplés
                new_neighbours = af.extract_neigh_from_tlv(tlv)
                print(len(new_neighbours),"possibly new neighbours")
                #on repeuple nos voisins potentiels (sans double dans U et S !)
                nb.add_potential_neighbours(new_neighbours)
                nb.debug_neighbours()
            if tlv_type == 5:
                #On a reçu des données !
                print("TLV Data received !")
                data.update_data(tlv)
                send.send_Ihave (s,ip_sender,port_sender,tlv)
            if tlv_type == 6:
                #On a reçu un IHave
                print("TLV IHave received !")
                #cf inondation je sais pas encore trop

            #On a traité le TLV, on le supprime de la liste courante
            print("TLV",i,"/",n,"has been explored")
            i += 1
            tlv_list = tlv_list[1:]
        #TODO On regarde si on doit inonder ou non (cf plus tard)

        #Choses à executer pérodiquement
        lt.maintenance_neighbours(s)


if __name__ == "__main__":
    main ()
