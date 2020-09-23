import zmq
import os
import json
import sys

context = zmq.Context() #de momento, nos permite crear el socket
socket = context.socket(zmq.REP) #REP(REPLY) define el papel que va a tomar el socket, en este caso responder
socket.bind("tcp://*:{}".format(sys.argv[1])) #se enlaza por medio del protocolo tcp y va a responder todo lo que venga del pueto 5555

print("Socket Proxy created in port {}!!!".format(sys.argv[1]))

class Proxy():

    def run(self):
        #TODO poner validaciones en los métodos
        while True:
            message = socket.recv_multipart()
            #message = socket.recv_json()
            if message[0] == b'upload':
                info_message = message[1].decode('utf-8')
                #print(info_message)
                self.returnInfoServers(info_message)

            if message[0] == b'list':
                user = message[1].decode('utf-8')
                list_file = self.listFilesUser(user)
                socket.send_multipart(list_file)

            if message[0] == b'download':
                filename = message[1].decode('utf-8')
                user = message[2].decode('utf-8')
                info_download = self.infoDownload(filename,user)
                socket.send_json(info_download)

    def returnInfoServers(self, new_message):
        message = json.loads(new_message)
        parts = message['parts']
        len_hash_part = len(parts)
        port_servers = self.servers(len_hash_part)
        user = message['user']
        filename = message['filename']
        complethash = message['complethash']         
        
        info_response = {
            "user": user,
            "filename": filename,
            "parts": parts,
            "servers": port_servers,
            "complethash": complethash
        }
        self.saveInfo(info_response)
        #print(message)
        socket.send_json(info_response)

    def servers(self,len_hash_part):

        ip_ports_servers = [] 
        f = open('info_servers.json','r')
        servers_dict = json.load(f)
        f.close()        
        print(servers_dict)
        
        list_servers = list(servers_dict)
        
        print("/////////////////")
        print("len_hash_part: " + str(len_hash_part))

        while (len_hash_part > 0):

            for server in list_servers:
                if len_hash_part == 0:
                    break
                if int(servers_dict[server]['capacity']) > 0:
                    
                    f = open('info_servers.json','w')
                    servers_dict[server]['capacity'] = str(int(servers_dict[server]['capacity'])-1)
                    json.dump(servers_dict, f, indent=4)
                    f.close()
                    len_hash_part -= 1
                    ip_ports_servers.append(servers_dict[server]['ip'] + ":" + servers_dict[server]['port'])
                else:
                    print("el server {} no tiene espacio".format(server))
                print(len_hash_part)

        return ip_ports_servers

    def saveInfo(self,info_response):
        f = open('info_proxy.json','r')
        info_dict = json.load(f)
        f.close()

        f = open('info_proxy.json','w')
        id_complethash = info_response['complethash']
        new_info = {
            "user": info_response['user'],
            "filename": info_response['filename'],
            "parts": info_response['parts'],
            "servers": info_response['servers']
        }
        info_dict[id_complethash] = new_info
        json.dump(info_dict, f, indent=4) 
        f.close()

    def listFilesUser(self,user):
        list_file = []
        f = open('info_proxy.json','r')
        info_dict = json.load(f)
        f.close()
        list_hash = list(info_dict) #get key_list
        print(list_hash)
        for key_hash in list_hash:
            if info_dict[key_hash]['user'] == user:
                list_file.append(info_dict[key_hash]['filename'].encode('utf-8'))

        return list_file
    
    def infoDownload(self,filename, user):
        f = open('info_proxy.json','r')
        info_dict = json.load(f)
        f.close()

        list_hash = list(info_dict)
        for key_hash in list_hash:
            if (info_dict[key_hash]['user'] == user) and (info_dict[key_hash]['filename'] == filename):
                return info_dict[key_hash]
        return {}

if __name__ == "__main__":
    #TODO iniciarlizar servers
    proxy = Proxy()
    #proxy.servers()
    proxy.run()

