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

import network

HOST = ''
PORT = network.PORT
clients, replay, nicknames = [], [], {}
games, tokens = [[]], [0]

def send(client, msg):
    msg = network.prep_msg(msg)
    client.transport.write(msg)

class GameServerProtocol(asyncio.Protocol):
    """ Each instance of class represents a client and the socket
    connection to it. """

    def connection_made(self, transport):
        """ Called on instantiation, when new client connects """
        self.transport = transport
        self.addr = transport.get_extra_info('peername')
        self._rest = b''
        clients.append(self)

        # Add to games
        self.gid = len(games) - 1 # game id
        self.pid = len(games[-1]) # player id
        print("game {gid} - player {pid} | connected".format(gid=self.gid,pid=self.pid))
        send(self, "setattr(self, 'player', {})".format(self.pid))
        games[-1].append(self)
        if len(games[-1]) == 2:
            games.append([])
            tokens.append(0)

    def data_received(self, data):
        """ Handle data as it's received. """
        data = self._rest + data
        (msgs, rest) = network.parse_recvd_data(data)
        self._rest = rest
        for msg in msgs:
            msg = msg.decode('utf-8')
            print('game {gid} - player {pid} | received : {m}'.format(
                gid= self.gid, pid= self.pid, m= msg ))
            _ = msg.split()
            if _[0] == 'click' and tokens[self.gid] == self.pid:
                print("len :", len(games[self.gid]))
                if len(games[self.gid]) == 2:
                    self.send2game('self.play({},{})'.format(*_[1:]))
                    tokens[self.gid] = 0 if tokens[self.gid] else 1
                    self.send2game("setattr(self, 'token', {tok})".format(tok=tokens[self.gid]))
            elif _[0] == 'replay':
                if self.gid in replay:
                    self.send2game('self.reset()')
                    replay.remove(self.gid)
                    tokens[self.gid] = 0
                else:
                    replay.append(self.gid)

    def send2game(self, msg):
        for player in games[self.gid]:
            print('game {gid} - player {pid} | sent : {m}'.format(
                gid=player.gid, pid=player.pid, m=msg))
            send(player, msg)

    def connection_lost(self, ex):
        """ Called on client disconnect. Clean up client state """
        print('Client {} disconnected'.format(self.addr))
        clients.remove(self)
        for game in games:
            if self in game:
                game.remove(self)

if __name__ == '__main__':
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