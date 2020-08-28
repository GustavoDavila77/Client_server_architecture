import zmq
import sys

context = zmq.Context()

#  Socket to talk to server
try:
    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ) #REQ este socket va a ser utilizado para hacer solicitudes
    socket.connect("tcp://localhost:5555") #Se conect de modo local, por el pueto 5555
except:
    print("No se pudo conectar al server")

cmd = sys.argv[1]

if cmd == 'upload':
    #subir el archivo
    filename = sys.argv[2]
    print("subiendo {}".format(filename))

    #'rb' read binary
    with open(filename,'rb') as f:
        bytes = f.read()
        socket.send_multipart([b"upload", filename.encode('utf-8'), bytes])
        resp = socket.recv_string()
        print(resp)
elif cmd == 'list':
    #list files
    socket.send_multipart([bytes("list", encoding='utf-8')])
    #recibir como multipart?
    resp = socket.recv_multipart()
    for ans in resp:
        print(ans.decode('utf-8'))
elif cmd == 'download':
    filetodownload = sys.argv[2]
    socket.send_multipart([bytes("download", encoding='utf-8'), bytes(filetodownload, encoding='utf-8')])
    resp = socket.recv_multipart()
    filename = resp[1].decode('utf-8')
    print(filename)
    with open('downloads/'+filename, 'wb') as f:
            f.write(resp[2])
    print("archivo descargado")
else:
    print('Error, comando no valido')