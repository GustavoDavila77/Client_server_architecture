import time
import zmq
import os
import json
from datetime import datetime

context = zmq.Context() #de momento, nos permite crear el socket
socket = context.socket(zmq.REP) #REP(REPLY) define el papel que va a tomar el socket, en este caso responder
socket.bind("tcp://*:5555") #se enlaza por medio del protocolo tcp y va a responder todo lo que venga del pueto 5555

print("Socket created!!!")


while True:
    message = socket.recv_multipart()

    if message[0] == b'upload':
        # client wants to upload a file
        filename = message[1].decode('utf-8')
        user = message[2].decode('utf-8')
        diruser = "D:\Escritorio\Arquitectura cliente servidor\code/files/"+user+"/"
        print(user)

        with open('data.json') as file:
            data = json.load(file)

            if user in data:
                print("el user already exist")
                directorio = os.listdir(diruser)
                if filename in directorio:
                    print("file already exist")
                    socket.send_string("File already exist, change name")
                else:
                    datenow = str(datetime.now())
                    data[user].append({
                    filename: datenow})

                    with open('data.json', 'w') as file:
                        json.dump(data, file, indent=4)

                    with open(diruser + filename, 'wb') as f:
                        f.write(message[3])
                        socket.send_string("File created!!")
            else:
                print("el user don´t exist")
                os.makedirs("D:\Escritorio\Arquitectura cliente servidor\code/files/"+user) #new folder created
                data[user] = []
                #TODO poner el filename: fecha
                datenow = str(datetime.now())
                data[user].append({
                filename: datenow})
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)

                with open(diruser + filename, 'wb') as f:
                    f.write(message[3])
                    socket.send_string("Ready!!")

    elif message[0] == b'list':
        user = message[1].decode('utf-8')
        diruser = "D:\Escritorio\Arquitectura cliente servidor\code/files/"+user+"/"
        directorio = os.listdir(diruser)
        print(directorio)
        archivos = []

        for f in directorio:
            archivos.append(f.encode('utf-8'))

        socket.send_multipart(archivos)

    elif message[0] == b'download':
        filename = message[1].decode('utf-8')
        user = message[2].decode('utf-8')
        diruser = "D:\Escritorio\Arquitectura cliente servidor\code/files/"+user+"/"
        print(filename)
        try:
            with open(diruser+ filename,'rb') as f:
                bytes = f.read()
                socket.send_multipart([b"downloadfile", filename.encode('utf-8'), bytes])
        except:
            socket.send_multipart([b"Notfound"])

    else:
        print('Error!!')
        socket.send_string("Error")