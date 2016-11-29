import time
import neighbours as n
import send


# 0 -> data
# 1 -> date de dernière reception
# 2 -> seqno
# 3 -> en cours d'innondation
# 4 -> liste des voisins n'ayant pas encore répondu à l'innondation
# 5 -> date de début de l'innondation
# 6 -> date du dernier envoi pendant l'innondation
datas = {'1604135e1d0c135e':['L.O.',time.time(),0,True,n.symetric_neighbours,time.time(),time.time()]}


def rm_data ():
    for key in datas :
        if time.time() - datas.get(key)[2] > 2100.:
            del datas[key]

# Prend un tlv correspondant à une data et effectue la mise à jour correspondant
def update_data (tlv):
    seqno = tlv[2:6]
    Id = tlv[6:14]
    now = time.time()
    data = tlv[14:]
    some = datas.get(Id)
    if some :
        if some[2] < seqno :
            some[0] = data
            some[1] = now
            some[2] = seqno
            some[3] = True
            some[4] = n.symetric_neighbours
            some[5] = now
            some[6] = now
    else :
        datas[Id] = [data,now,seqno,True,[],n.symetric_neighbours,now,now]

def innondation ():
    for key in datas :
        tupl = datas.get(key)
        targets = tupl[4]
        for neigh in targets :
            send.send_data(sock,neigh,key)





