#en IPv4 qui marche sur eduroam
#IP de Juliusz
#HOST_JCH = '81.194.27.155'
HOST_JCH = '138.231.146.117'
#toutes les IP
HOST_SELF= '0.0.0.0'
#Port de Juliusz
#PORT_JCH = 1212
PORT_JCH = 1312
#Notre port
PORT_SELF = 1312
#Id de Juliusz
#Id_JCH = bytes.fromhex('68fa34ac85cf9349')
Id_JCH = bytes.fromhex('1604135e1d0c135e')

#Magic et Version
ENTETE_UDP = bytes([57,0])

#Id_Jules
Id = bytes([22,4,19,95,29,12,19,95])
#Id_Gab
#Id = bytes([22,4,19,94,29,12,19,94])
