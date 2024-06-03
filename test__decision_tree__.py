import socket
import queue
import threading
queue_ret=queue.Queue()
queue_ip_freq=queue.Queue()
dizionario={}
import tensorflow as tf
tree=tf.keras.models.load_model("tree/")
def string_to_dict(ip_frequency):
    ip_frequency=ip_frequency.replace("'","")
    ip_frequency=ip_frequency.replace(" ","")
    ip_frequency=ip_frequency.replace("}","")
    ip_frequency=ip_frequency.replace("{","")
    ip_frequency_temp=ip_frequency.split(",")
    ip_frequency_final={}
    
    for i in ip_frequency_temp:
        i=i.split(":")
        ip_frequency_final[i[0]]=int(i[1])
    return ip_frequency_final

def somma_dizionari(d1):
    global dizionario
    for chiave in d1.keys():
        if chiave in dizionario:
            dizionario[chiave] = (d1[chiave]) + dizionario[chiave]
        else:
            dizionario[chiave] = (d1[chiave])
    print(dizionario)
    return

def sottrai_dizionario(d1):
    global dizionario
    for chiave, valore in d1.items():
        dizionario[chiave] -= valore
        if dizionario[chiave] == 0:
            del dizionario[chiave]
    return dizionario

def server_30104():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("0.0.0.0",30104))
        server_socket.listen()
        connection,address=server_socket.accept()
        with connection:
            while True:
                data=connection.recv(4096)
                data=data.decode()
                data=data.replace("'","")
                data=data.replace("None","-1")
                i=string_to_dict(data)
                
                somma_dizionari(i)
                queue_ip_freq.put(i)
                
def server_10469():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("0.0.0.0",10469))
        server_socket.listen()
        connection,address=server_socket.accept()
        with connection:
            while True:
                data2=connection.recv(4096)
                if queue_ret.qsize()>5:
                    queue_ret.get()
                queue_ret.put(float(data2.decode().replace("'","").replace("]","").replace("[","")))
                
print("pronto a connettere")       
thread1=threading.Thread(target=server_30104).start()
thread2=threading.Thread(target=server_10469).start()
while True:
    if queue_ip_freq.qsize()>5 and queue_ret.qsize()>5:
        
        queue_list1 = list(queue_ret.queue)
        last_five = queue_list1[-5:]
        errase1=queue_ip_freq.get()
        errase2=queue_ret.get()
        dizionario=sottrai_dizionario(errase1)
        Y=tree.predict([last_five]) 
        print(Y)
        if(Y[0]>0.5):
            print("attacco dos in corso")
            
        else:
            print("false")
    
        
        

                