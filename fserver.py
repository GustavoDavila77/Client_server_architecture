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
        self.dirservers = "D:\Escritorio\Arquitectura cliente servidor\code/files/"

    def run(self):
        validation = self.receiveParameters()
        if validation == True:
            self.port_server = sys.argv[1]
            self.ip_proxy = sys.argv[2]
            self.name_server = sys.argv[3]
            self.server_capacity = sys.argv[4]
            
            if self.saveServer() == True:
                socket = self.initSocket()
                self.conectProxy()

                self.receive(socket)

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
        #valid that ip and port not exist
        create_bool = True
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
            list_folders = os.listdir(self.dirservers)
            if self.name_server in list_folders:
                print("Folder name already exist")
                create_bool = False
            else:
                os.makedirs("D:\Escritorio\Arquitectura cliente servidor\code/files/"+ self.name_server) #new folder created
                print("new server working")
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
            print("server is already working")
        
        return create_bool
            

    def receive(self,socket):

        while True:
            message = socket.recv_multipart()

            if message[0] == b'upload':
    
                name_parthash = message[1].decode('utf-8')
                print("name_parthash: {}".format(name_parthash))
                        
                dirserver = "D:\Escritorio\Arquitectura cliente servidor\code/files/"+self.name_server+"/"
                print(self.name_server)
                
                with open(dirserver + name_parthash, 'wb') as f:
                    f.write(message[2])
                    socket.send_string("File created!!")

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
                part_hash = message[1].decode('utf-8')
                print(part_hash)
                print(self.name_server)
                dir_server = "D:\Escritorio\Arquitectura cliente servidor\code/files/"+self.name_server+"/"
            
                try:
                    with open(dir_server+ part_hash,'rb') as f:
                        bytes = f.read()
                        socket.send_multipart([b"downloading", bytes])
                except:
                    socket.send_multipart([b"Notfound"])

            else:
                print('Error!!')
                socket.send_string("Error")

if __name__ == "__main__":
    #TODO iniciarlizar servers
    server = FServer()
    #proxy.servers()
    server.run()