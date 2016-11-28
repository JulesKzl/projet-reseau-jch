import socket
import types

#en IPv4
HOST_JCH = '81.194.27.155'
HOST_SELF= '255.255.255.255'
PORT_BOOT = 1212
PORT_SELF = 1412
BOOTSRAP_JCH = bytes.fromhex('6722a421aadb51bd')
#entete Jules
ENTETE = bytes([57,0,0,10,22,4,19,95,29,12,19,95])
#entete Gab
#ENTETE = bytes([57,0,0,10,22,4,19,94,29,12,19,94])

SUITE = bytes([2,8])

def main ():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.bind((HOST_SELF,PORT_SELF))
    while True :
        s.sendto(ENTETE + SUITE + BOOTSRAP_JCH , (HOST_JCH,PORT_BOOT))
        print(ENTETE + SUITE + BOOTSRAP_JCH)
        mess = s.recvfrom(4095)
        print(mess)


if __name__ == "__main__":
    main ()
