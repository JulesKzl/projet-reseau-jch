import time

datas = {'1604135e1d0c135e':('L.O.',time.time(),seqno)}

if __init__ == "__main__" :
    print("toto")

def add_data (Id,new_data,seqno):
    maybe = datas.get('Id')
    if maybe != None :
        if maybe[2] < seqno :
            maybe[0] = new_data
            maybe[1] = time.time()
            maybe[2] = seqno
            #innonde()
    else :
        datas['Id'] = (new_data,time.time(),seqno)
        #innonde()
    #send_I_have ()


def rm_data ():
    for key in datas :
        if time.time() - datas.get(key)[2] > 2100.:
            del datas[key]

