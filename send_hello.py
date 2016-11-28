import socket
import types

HOST_JCH = '2001:660:3301:9200::51c2:1b9b'
HOST_SELF= '::'
PORT_BOOT = 1212
PORT_SELF = 1312
BOOTSRAP_JCH = bytes.fromhex('6722a421aadb51bd')
ENTETE = bytes([57,0,0,73,22,4,19,94,29,12,19,94])
SUITE = bytes([5,71,0,0,0,2,22,4,19,94,29,12,19,94,32,57])

def main ():
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    s.bind((HOST_SELF,PORT_SELF))
    while True :
        s.sendto(ENTETE + SUITE + b'Castro est mort mais vous finirez quand meme au goulag !!',(HOST_JCH,PORT_BOOT))
        mess = s.recvfrom(4096)
        print(mess)

if __name__ == "__main__":
    main ()
