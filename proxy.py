import zmq
import os
import json
import sys

context = zmq.Context() #de momento, nos permite crear el socket
socket = context.socket(zmq.REP) #REP(REPLY) define el papel que va a tomar el socket, en este caso responder
socket.bind("tcp://*:{}".format(sys.argv[1])) #se enlaza por medio del protocolo tcp y va a responder todo lo que venga del pueto 5555

print("Socket Proxy created in port {}!!!".format(sys.argv[1]))

class Proxy():

    #recibir como parametro el array de hash
    def servers(self,len_hash_part):
        #entrar a info_servers y verificar que capacidad > 0 solo para probar
        #implement round robins algorithm - investigar como es la teoria
        #poner un hash en cada server e ir disminuyendo el atributo capacity
        #surge una duda, como seria la implementación cuando se quiera enviar cada uno de
        # esos hash y bytes a los servers ??
        ip_ports_servers = [] 
        f = open('info_servers.json','r')
        servers_dict = json.load(f)
        f.close()        
        print(servers_dict)
        
        list_servers = list(servers_dict)
        #print(list_servers)
        
        #hacer un while donde se recorra el lenght del array de hash 
        #y obtener el server 
        print("/////////////////")
        print("len_hash_part: " + str(len_hash_part))

        #f = open('info_servers.json','w')
        while (len_hash_part > 0):

            for server in list_servers:
                if len_hash_part == 0:
                    break
                if int(servers_dict[server]['capacity']) > 0:
                    #f.close()
                    f = open('info_servers.json','w')
                    servers_dict[server]['capacity'] = str(int(servers_dict[server]['capacity'])-1)
                    json.dump(servers_dict, f, indent=4)
                    f.close()
                    len_hash_part -= 1
                    ip_ports_servers.append(servers_dict[server]['ip'] + ":" + servers_dict[server]['port'])
                else:
                    print("el server {} no tiene espacio".format(server))
                print(len_hash_part)
        #f.close()
        return ip_ports_servers

                

    def run(self):
        #TODO almacenar la info de cada archivo
        #TODO poner validaciones en los métodos
        while True:
            message = socket.recv_json()
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
            #print(message)
            socket.send_json(info_response)

if __name__ == "__main__":
    #TODO iniciarlizar servers
    proxy = Proxy()
    #proxy.servers()
    proxy.run()

