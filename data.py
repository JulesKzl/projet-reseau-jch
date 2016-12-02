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

# Prend un tlv correspondant à une data et effectue la mise à jour correspondant dans la liste des data que l'on maintient
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

# Parcours la liste des datas et si elles sont en cours d'innondation :
# vérifie que c'est toujours d'actualité :
# - si non alors on enlève le flag inondation et retire les restants de la liste de symetric_neighbours
# - si oui, vérifie qu'on est à plus de 3 secondes de la dernière inondation, si oui alors on envoie à tout le monde et actualise la date
def innondation (sock):
    for key in datas :
        tupl = datas.get(key)
        if tupl[3] :
            now = time.time()
            if now - tupl[5] > 11 :
                tupl[3] = False
                for neigh in tupl[4] :
                    remove_symetric_neighbour(neigh)
            else :
                if now - tupl[6] > 3 :
                    targets = tupl[4]
                    some[6] = now
                    for neigh in targets :
                        send.send_data(sock,neigh,key)

# Appelée lorsqu'on reçoit un tlv IHave contenant l'ID d'une donnée :
# si la donnée est au moins aussi récente, alors on retire l'emetteur de la liste des gens qui n'ont pas acquité, et vérifie que la liste est toujours non vide.
def update_innond (neigh,seqno):
    tupl = datas.get(Id)
    if tupl :
        if tupl[3] :
            if seqno > tupl[2] :
                if neigh in tupl[4] :
                    list[4].remove(neigh)
                    if not l :
                        tupl[3] = False
