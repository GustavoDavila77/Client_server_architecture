import time
import zmq

context = zmq.Context() #de momento, nos permite crear el socket
socket = context.socket(zmq.REP) #REP(REPLY) define el papel que va a tomar el socket, en este caso responder
socket.bind("tcp://*:5555") #se enlaza por medio del protocolo tcp y va a responder todo lo que venga del pueto 5555

print("Socket created!!!")

while True:
    #  Wait for next request from client
    print("waiting for message on socket")
    #message = socket.recv() #se recive los mensajes
    message = socket.recv_string() #se recive los mensajes
    
    print("Received request: %s" % message)

    v1 = message[0]
    op = message[1]
    v2 = message[2]
    
    result = 0
    if op == '+':
        result = int(v1) + int(v2)
    else:
        print("Error")

    #time.sleep(1) #delay

    #  Send reply back to client
    socket.send_string(str(result)) #envio para el cliente    
    #socket.send(b"World") #envio para el cliente