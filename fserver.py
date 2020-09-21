import time
import zmq
import os
import json
from datetime import datetime
import sys


class FServer():
    #en los argumentos recivir la carpeta donde va a se almacenado todo
    def __init__(self):
        self.context = zmq.Context() #nos permite crear el socket
        
    def run(self):
        validation = self.receiveParameters()
        if validation == True:
            self.port_server = sys.argv[1]
            self.ip_proxy = sys.argv[2]
            self.name_server = sys.argv[3]
            self.server_capacity = sys.argv[4]

            socket = self.initSocket()
            self.conectProxy()
            self.saveServer()
            #self.receive(socket)

    def receiveParameters(self):
        boolean = True
        try:
            sys.argv[1]
        except:
            print("Ingrese el puerto del server")
            boolean = False
        try:
            sys.argv[2]
        except:
            print("Ingrese la dirección:port del proxy")
            boolean = False
        try:
            sys.argv[3]
        except:
            print("Ingrese el nombre del server")
            boolean = False
        try:
            sys.argv[4]
        except:
            print("Ingrese la capacidad del server")
            boolean = False
        return boolean
        

    def initSocket(self):
        socket = self.context.socket(zmq.REP) #REP(REPLY) to answer to clients
        socket.bind("tcp://*:{}".format(self.port_server)) #se enlaza por medio del protocolo tcp y va a responder todo lo que venga del pueto 5555
        print("Socket created in port {}!!!".format(self.port_server))
        return socket

    def conectProxy(self):
        p = self.context.socket(zmq.REQ) #to connect with proxy
        p.connect("tcp://{}".format(self.ip_proxy))
        print("Connection with proxy in {}!!!".format(self.ip_proxy))

    def saveServer(self):
        #TODO at begining clear info_servers
        #valid that ip and port not exist
        f = open('info_servers.json','r')
        servers_dict = json.load(f)
        list_servers = list(servers_dict)

        server_bool = True
        for server in list_servers:
            if (servers_dict[server]['ip'] == "localhost") and (servers_dict[server]['port'] == self.port_server):
                print("ip and port equal")
                server_bool = False

        f.close()
        if server_bool == True:
            print("authorization created server")
            info_server = {
                    "ip": "localhost",
                    "port": self.port_server,
                    "capacity": self.server_capacity
            }
            f = open('info_servers.json','w')
            servers_dict[self.name_server] = info_server
            json.dump(servers_dict, f, indent=4)
            f.close()


        else:
            print("no authorizated")
            

    def receive(self,socket):
        pass
        """
        while True:
            message = socket.recv_multipart()

            if message[0] == b'upload':
                # client wants to upload a file
                filename = message[1].decode('utf-8')
                user = message[2].decode('utf-8')
                parthash = message[4].decode('utf-8')
                complethash = message[5].decode('utf-8')
                print("parthash: {}".format(parthash))
                print("complethash: {}".format(complethash))
                        
                diruser = "D:\Escritorio\Arquitectura cliente servidor\code/files/"+user+"/"
                print(user)

                with open('data.json') as file:
                    data = json.load(file)

                    if user in data:
                        print("el user already exist")
                        directorio = os.listdir(diruser)
                        
                        #si el archivo ya existe(complethash) entonces hacer el apend de los parthash
                        #sino entonces crear un nuevo complethash
                        print("//////////////////////////")
                        complethash_list = list(data[user])
                        print(complethash_list)

                        if complethash in complethash_list:
                            print("complethash already exist")
                            
                            print(data[user][complethash]["parthash"])
                            data[user][complethash]["parthash"].append(parthash)

                            with open('data.json', 'w') as file:
                                json.dump(data, file, indent=4)
                        else:
                            data[user] = {
                                complethash: {
                                    "filename": filename,
                                    "owner": user,
                                    "parthash": [parthash]
                                }
                            }

                            with open('data.json', 'w') as file:
                                json.dump(data, file, indent=4)

                        elementos = data.items()
                        for key, valor in elementos:
                            elementosanidados = key.items()
                            if complethash in elementosanidados:
                                print("apend parthash")
                        print(elementos)

                        
                        with open('data.json', 'w') as file:
                                json.dump(data, file, indent=4)

                        with open(diruser + filename, 'ab') as f:
                            f.write(message[3])
                            socket.send_string("Part upload!!")

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
                        #datenow = str(datetime.now())
                        data[user].append({
                            complethash: {
                                "filename": filename,
                                "owner": user,
                                "parthash": [parthash]
                            }})
                        
                        data[user] = {
                            complethash: {
                                "filename": filename,
                                "owner": user,
                                "parthash": [parthash]
                            }
                        }
                        with open('data.json', 'w') as file:
                            json.dump(data, file, indent=4)

                        with open(diruser + filename, 'wb') as f:
                            f.write(message[3])
                            socket.send_string("Ready!!")

            #TODO set try except when user don´t exist
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
                socket.send_string("Error") """

if __name__ == "__main__":
    #TODO iniciarlizar servers
    server = FServer()
    #proxy.servers()
    server.run()