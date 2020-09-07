import zmq
import sys
import json

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
    filename = sys.argv[2]
    user = sys.argv[3]
    #subir el archivo
    print("subiendo {}".format(filename))

    #'rb' read binary
    with open(filename,'rb') as f:
        contentbytes = f.read()
        socket.send_multipart([b"upload", filename.encode('utf-8'), user.encode('utf-8'), contentbytes])
        resp = socket.recv_string()
        print(resp)
elif cmd == 'list':
    #list files
    user = sys.argv[2]
    socket.send_multipart([bytes("list", encoding='utf-8'),bytes(user, encoding='utf-8')])
    resp = socket.recv_multipart()
    for ans in resp:
        print(ans.decode('utf-8'))
elif cmd == 'download':
    filetodownload = sys.argv[2]
    user = sys.argv[3]
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
else:
    print('Error, comando no valido')