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
            socket.connect("tcp://localhost:5555") #Se conect de modo local, por el pueto 5555
            
            cmd = sys.argv[1]
    
            if cmd == 'upload':
                filename = sys.argv[2]
                self.upload(socket,filename)
                
            elif cmd == 'list':
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

        

    def upload(self,socket,filename):
        print(filename)
        #size_filename = os.path.getsize("D:\Escritorio\Arquitectura cliente servidor\code/"+filename)
        #hashobj = Hash("md5")
        #print(hashobj.getHash(filename))
        
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
            print("complethash: {}".format(hash))
            return hash

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
    
