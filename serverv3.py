import time
import zmq

context = zmq.Context() #de momento, nos permite crear el socket
socket = context.socket(zmq.REP) #REP(REPLY) define el papel que va a tomar el socket, en este caso responder
socket.bind("tcp://*:5555") #se enlaza por medio del protocolo tcp y va a responder todo lo que venga del pueto 5555

print("Socket created!!!")

while True:
    
    message = socket.recv()

    with open("imagen.jpg","wb") as f:
        f.write(message)
    socket.send_string("okas")