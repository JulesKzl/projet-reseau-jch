#en IPv4 qui marche sur eduroam
#IP de Juliusz
HOST_JCH = '81.194.27.155'
#toutes les IP
HOST_SELF= '0.0.0.0'
#Port de Juliusz
PORT_JCH = 1212
#Notre port
PORT_SELF = 1312
#Id de Juliusz
Id_JCH = bytes.fromhex('68fa34ac85cf9349')

#Magic et Version
ENTETE_UDP = bytes([57,0])

#TODO rendre l'Id aléatoire (à la fin, d'abord les tests)
#Id_Jules
Id = bytes([22,4,19,95,29,12,19,95])
#Id_Gab
#Id = bytes([22,4,19,94,29,12,19,94])



def make_IHU(Id1,Id2):
    """ Créer un IHeardYou d'une Id1 vers une Id2 """
    IHU = bytes([2,8])
    length_IHU = bytes([0,10])
    return ENTETE_UDP + length_IHU + Id1 + IHU + Id2
