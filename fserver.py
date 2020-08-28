import time
import zmq
import os

context = zmq.Context() #de momento, nos permite crear el socket
socket = context.socket(zmq.REP) #REP(REPLY) define el papel que va a tomar el socket, en este caso responder
socket.bind("tcp://*:5555") #se enlaza por medio del protocolo tcp y va a responder todo lo que venga del pueto 5555

print("Socket created!!!")

files = []
archivos = []
# 1. upload a file
# 2. list files
# 3. download a file

while True:
    message = socket.recv_multipart()
    print(message)
    if message[0] == b'upload':
        # client wants to upload a file
        filename = message[1].decode('utf-8')
        print(filename)
        files.append('filename')
        with open('files/'+filename, 'wb') as f:
            f.write(message[2])
        socket.send_string("Listo!!")
    elif message[0] == b'list':
        directorio = os.listdir('D:\Escritorio\Arquitectura cliente servidor\code/files')
        print(directorio)
        #socket.send_multipart([b"listfiles", directorio.encode('utf-8'), bytes])
        for f in directorio:
            archivos.append(f.encode('utf-8'))

        socket.send_multipart(archivos)
    elif message[0] == b'download':
        filename = message[1].decode('utf-8')
        print(filename)
        with open('files/'+ filename,'rb') as f:
            bytes = f.read()
            socket.send_multipart([b"downloadfile", filename.encode('utf-8'), bytes])      
    else:
        print('Error!!')
        socket.send_string("Error")