import time
import zmq
import os

context = zmq.Context() #de momento, nos permite crear el socket
socket = context.socket(zmq.REP) #REP(REPLY) define el papel que va a tomar el socket, en este caso responder
socket.bind("tcp://*:5555") #se enlaza por medio del protocolo tcp y va a responder todo lo que venga del pueto 5555

print("Socket created!!!")

#files = []
archivos = []
# 1. upload a file
# 2. list files
# 3. download a file

while True:
    message = socket.recv_multipart()
    directorio = os.listdir('D:\Escritorio\Arquitectura cliente servidor\code/files')
    if message[0] == b'upload':
        # client wants to upload a file
        filename = message[1].decode('utf-8')
        if filename in directorio:
            print("exist")
            socket.send_string("File already exist, change name")
        else:
            print("don´t exist")
            with open('files/'+filename, 'wb') as f:
                f.write(message[2])
                socket.send_string("Ready!!")

        
    elif message[0] == b'list':
        for f in directorio:
            archivos.append(f.encode('utf-8'))

        socket.send_multipart(archivos)
    elif message[0] == b'download':
        filename = message[1].decode('utf-8')
        print(filename)
        try:
            with open('files/'+ filename,'rb') as f:
                bytes = f.read()
                socket.send_multipart([b"downloadfile", filename.encode('utf-8'), bytes])
        except:
            socket.send_multipart([b"Notfound"])

    else:
        print('Error!!')
        socket.send_string("Error")