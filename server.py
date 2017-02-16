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
import asyncio
from Network import network

HOST = ''
PORT = network.PORT

clients = []
nicknames = {}

class GameServerProtocol(asyncio.Protocol):
    """ Each instance of class represents a client and the socket
    connection to it. """

    def send(self, client, msg):
        msg = network.prep_msg(msg)
        client.transport.write(msg)

    def userloop(self, client, msg, checker):
        result = self.ask(client, msg)
        while not checker(result):
            result = self.ask(client, msg)
        return result

    def ask(self, client, msg):
        self.send(client, "self.send(input('{}'))".format(msg))

    def connection_made(self, transport):
        """ Called on instantiation, when new client connects """
        self.transport = transport
        self.addr = transport.get_extra_info('peername')
        self._rest = b''
        self.clients.append(self)

        # Ask nickname
        self.userloop()
        # Handle already taken nickname


    def data_received(self, data):
        """ Handle data as it's received. """
        data = self._rest + data
        (msgs, rest) = network.parse_recvd_data(data)
        self._rest = rest
        for msg in msgs:
            msg = msg.decode('utf-8')
            # Handle the data as str input
            self.handle_msg(msg)

    def handle_msg(self, msg):
        # Handle every type of msg
        pass

    def send2game(self, msg):
        # Send a message to every
        for player in self.games[self.gid]:
            print('game {gid} - player {pid} | sent : {m}'.format(
                gid=player.gid, pid=player.pid, m=msg))
            self.send(player, msg)

    def connection_lost(self, ex):
        """ Called on client disconnect. Clean up client state """
        print('Client {} disconnected'.format(self.addr))
        clients.remove(self)
        for game in games:
            if self in game:
                game.remove(self)

class Server(object):
    def __init__(self):
        loop = asyncio.get_event_loop()
        # Create server and initialize on the event loop
        coroutine = loop.create_server(GameServerProtocol, host=HOST, port=PORT)
        server = loop.run_until_complete(coroutine)
        # print listening socket info
        for socket in server.sockets:
            addr = socket.getsockname()
            print('Listening on {}'.format(addr))
        # Run the loop to process client connections
        loop.run_forever()

if __name__ == '__main__':
    Server()