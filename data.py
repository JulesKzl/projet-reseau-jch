import time

datas = {'1604135e1d0c135e':('L.O.',time.time(),0)}

def add_data (Id,new_data,seqno):
    maybe = datas.get(Id)
    if maybe != None :
        if maybe[2] < seqno :
            maybe[0] = new_data
            maybe[1] = time.time()
            maybe[2] = seqno
            #innonde()
    else :
        datas[Id] = (new_data,time.time(),seqno)
        #innonde()
    #send_I_have ()


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
            #innondation()
    else :
        datas[Id] = (data,now,seqno)
        #innondation()


