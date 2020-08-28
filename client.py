import zmq
import sys

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ) #REQ este socket va a ser utilizado para hacer solicitudes
socket.connect("tcp://localhost:5555") #Se conect de modo local, por el pueto 5555

op = sys.argv[1]

socket.send_string(op)
resp = socket.recv()
print("Response from server {}".format(resp))

"""
print("Sending request")
socket.send(b"Hello")

message = socket.recv()
print("Received reply [ %s ]" % (message))
#  Do 10 requests, waiting each time for a response """

