import zmq
import sys
import json
import os
import hashlib

partsize = 1024*1024 #N° MBytes

class Hash():
    def __init__(self,tipohash):
        self.tipohash = tipohash

    def getHash(self, file):
        if self.tipohash == "md5":
            hasher = hashlib.md5()
            hasher.update(file)
            return (hasher.hexdigest())
        elif self.tipohash == "sha1":
            hasher = hashlib.sha1(file).hexdigest()
            return hasher
        elif self.tipohash == "sha256":
            hasher = hashlib.sha256(file).hexdigest()
            return hasher
        else:
            print("Don´t found hash type, insert md5,sha1 or sha256")
            return("NoHash")

class Client():
    def __init__(self):
        self.context = zmq.Context()
        self.hashobj = Hash("sha256")

    def run(self):
        #  Socket to talk to server
        try:
            #TODO hacer una función para la conección y el envio de data con multipart
            #función que reciva 2 o 3 parametros
            print("Connecting to hello world server…")
            socket = self.context.socket(zmq.REQ) #REQ este socket va a ser utilizado para hacer solicitudes
            
            
            cmd = sys.argv[1]
            if cmd == 'upload':
                socket.connect("tcp://{}".format(sys.argv[4])) #Se conect de modo local, por el pueto indicado en la linea de comandos
                filename = sys.argv[2]
                info_send = self.sendInfoProxy(socket,filename)
                self.sendDataServers(info_send)
                #self.upload(socket,filename)
                
            elif cmd == 'list':
                socket.connect("tcp://{}".format(sys.argv[3])) #Se conect de modo local, por el pueto indicado en la linea de comandos
                user = sys.argv[2]
                self.list(socket,user)
                
            elif cmd == 'download':
                filetodownload = sys.argv[2]
                user = sys.argv[3]
                self.download(socket,filetodownload,user)
                
            else:
                print('Error, comando no valido')
        except ValueError:
            print("No se pudo conectar al server")

    def sendInfoProxy(self,socket,filename):
        print("enviando info al proxy de {}".format(filename))
        hash_whole_file = self.complethash(filename)
        part_hash = self.partHash(filename)
        #print("hash_whole_file: {}".format(hash_whole_file))
        #print("parthash: {}".format(part_hash))
        user = sys.argv[3]
        fileinfo = {
            "user": user,
            "filename": filename,
            "parts": part_hash,
            "complethash": hash_whole_file
        }
        #socket.send_json(fileinfo)
        str_json = json.dumps(fileinfo)
        socket.send_multipart([b'upload', str_json.encode('utf-8')])
        resp = socket.recv_json()
        print(resp)
        return resp

    #TODO optimizar conexiones y envio de datos a los servers (agruparlos)
    def sendDataServers(self, info_send):
        dir_servers = info_send['servers']
        index = 0
        for dir in dir_servers:
            socket = self.context.socket(zmq.REQ)
            socket.connect("tcp://" + dir)

            with open(info_send['filename'],'rb') as f:
                partbytes = f.read(partsize)
                if not partbytes:
                    break
                socket.send_multipart([b'upload', info_send['parts'][index].encode('utf-8'),  partbytes])
                resp = socket.recv_string()
                print(resp)
            index += 1
            socket.close()

    def upload(self,socket,filename):
        #size_filename = os.path.getsize("D:\Escritorio\Arquitectura cliente servidor\code/"+filename)

        user = sys.argv[3]
        print("subiendo {}".format(filename))
        
        hash_whole_file = self.complethash(filename)
        self.sendRequest(socket, b"upload", filename, user, hash_whole_file)

        

    def list(self,socket,user):
        socket.send_multipart([bytes("list", encoding='utf-8'),bytes(user, encoding='utf-8')])
        resp = socket.recv_multipart()
        for ans in resp:
            print(ans.decode('utf-8'))

    def download(self,socket,filetodownload,user):
        socket.send_multipart([bytes("download", encoding='utf-8'), bytes(filetodownload, encoding='utf-8'),bytes(user, encoding='utf-8')])
        resp = socket.recv_multipart()
        if len(resp) == 3:
            filename = resp[1].decode('utf-8')
            print(filename)
            with open('downloads/'+filename, 'wb') as f:
                    f.write(resp[2])
            print("archivo descargado")
        else:
            print(resp)
        
    def complethash(self,filename):
        #'rb' read binary
        with open(filename, 'rb') as f:
            completbytes = f.read()
            #print("completbytes: {}".format(completbytes))
            hash= self.hashobj.getHash(completbytes)
            #print("complethash: {}".format(hash))
            return hash

    def partHash(self,filename):
        hashes = []
        with open(filename,'rb') as f:
            while True:
                partbytes = f.read(partsize)
                if not partbytes:
                    break
                parthash= self.hashobj.getHash(partbytes)
                hashes.append(parthash)
                #print("parthash: {}".format(parthash))
            return hashes


    def sendRequest(self,socket,option,filename,user,complethash):
        with open(filename,'rb') as f:
            while True:
                partbytes = f.read(partsize)
                parthash= self.hashobj.getHash(partbytes)
                print("parthash: {}".format(parthash))
                if not partbytes:
                    break
                socket.send_multipart([option, filename.encode('utf-8'), user.encode('utf-8'), partbytes, parthash.encode('utf-8'), complethash.encode('utf-8')])
                resp = socket.recv_string()
                print(resp)
            print("File created")
        

if __name__ == "__main__":
    client = Client()
    client.run()
    
