import zmq
import sys

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ) #REQ este socket va a ser utilizado para hacer solicitudes
socket.connect("tcp://localhost:5555") #Se conect de modo local, por el pueto 5555

with open("pc.jpg",'rb') as f:
    bytes = f.read()
    print(bytes)
    socket.send(bytes)
    resp = socket.recv_string()
    print(resp)