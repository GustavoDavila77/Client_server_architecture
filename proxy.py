import zmq
import os
import json

context = zmq.Context() #de momento, nos permite crear el socket
socket = context.socket(zmq.REP) #REP(REPLY) define el papel que va a tomar el socket, en este caso responder
socket.bind("tcp://*:5555") #se enlaza por medio del protocolo tcp y va a responder todo lo que venga del pueto 5555

print("Socket Proxy created!!!")

class Proxy():

    #recibir como parametro el array de hash
    def servers(self):
        #entrar a info_servers y verificar que capacidad > 0 solo para probar
        #implement round robins algorithm - investigar como es la teoria
        #poner un hash en cada server e ir disminuyendo el atributo capacity
        #surge una duda, como seria la implementación cuando se quiera enviar cada uno de
        # esos hash y bytes a los servers ??
        ports_servers = [] 
        f = open('info_servers.json','r')
        servers_dict = json.load(f)

        print(servers_dict)
        
        list_servers = list(servers_dict)
        #print(list_servers)
        
        #hacer un while donde se recorra el lenght del array de hash 
        #y obtener el server 

        for server in list_servers:

            if int(servers_dict[server]['capacity']) > 0:
                print("mayor a 0")
                f.close()
                f = open('info_servers.json','w')
                servers_dict[server]['capacity'] = str(int(servers_dict[server]['capacity'])-1)
                json.dump(servers_dict, f, indent=4)
                f.close()
                #ports_servers.append(servers_dict[server]['port'])
            else:
                print("menor a 0")

                

    def run(self):
        while True:
            message = socket.recv_json()
            #len_hash_part = len(message['parts'])
            #self.servers(len_hash_part)
            #print(message)
            socket.send_string("return proxy")

if __name__ == "__main__":
    #TODO iniciarlizar servers
    proxy = Proxy()
    proxy.servers()
    #proxy.run()

