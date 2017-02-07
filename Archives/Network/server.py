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
import socket, select, pickle
import re

class Server(object):
    def __init__(self):
        self.player = 0

host = "0.0.0.0"
port = 80

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

print("="*25 + " Server Started " + "="*25)

ids = {}
clients = []
while True:
    Connections, wlist, xlist = select.select([server],[], [], 0.05)

    for Connection in Connections:
        client, Informations = Connection.accept()
        clients.append(client)

    clientsList = []
    try:
        clientsList, wlist, xlist = select.select(clients, [], [], 0.05)
    except select.error:
        pass
    else:
        for clientInList in clientsList:
            if clientInList not in ids.keys():
                ids[clientInList] = max(ids.values()) + 1 if ids.values() else 0
            data = clientInList.recv(1024)
            data = pickle.loads(data)
            print("received from client {} : << {} >>".format(ids[clientInList], data))
            data = "Client number {}, successfully received {}.".format(ids[clientInList], data)
            print("sent to client {}       : {}".format(ids[clientInList], data))
            data = pickle.dumps(data)
            clientInList.send(data)

clientInList.close()
server.close()
