# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '31/01/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
import socket, pickle

host = "192.168.173.1"
port = 80

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((host, port))

data = "I'm connecting to you"
while True:
    print("Moi - {}".format(data))
    # print("sent to server       : << {} >>".format(data))
    data = pickle.dumps(data)
    server.send(data)
    data = server.recv(1024)
    data = pickle.loads(data)
    # print("received from server : << {} >>".format(data))
    print("Server - {}".format(data))

    data = {"Hello":(0,0)}

server.close()
