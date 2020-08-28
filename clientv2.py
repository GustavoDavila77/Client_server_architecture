import zmq
import sys

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ) #REQ este socket va a ser utilizado para hacer solicitudes
socket.connect("tcp://localhost:5555") #Se conect de modo local, por el pueto 5555

op = sys.argv[0]
num1 = sys.argv[1]
num2 = sys.argv[2]

print(type(op))
print(type(num1))
print(type(num2))

#num1 = 7
socket.send_multipart([bytes(op, encoding='utf-8'), bytes(num1, encoding='utf8'), bytes(num2, encoding='utf8')])
resp = socket.recv()
print("Response from server {}".format(resp))

"""
print("Sending request")
socket.send(b"Hello")

message = socket.recv()
print("Received reply [ %s ]" % (message))
#  Do 10 requests, waiting each time for a response """

