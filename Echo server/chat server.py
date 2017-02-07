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
import chat
HOST = chat.HOST
PORT = chat.PORT
clients = []
nicknames = {}
rooms = dict([("Room {}".format(i),[]) for i in range(10)])

class ChatServerProtocol(asyncio.Protocol):
    """ Each instance of class represents a client and the socket
    connection to it. """

    def connection_made(self, transport):
        """ Called on instantiation, when new client connects """
        self.transport = transport
        self.addr = transport.get_extra_info('peername')
        self._rest = b''
        clients.append(self)
        nicknames[self] = self.addr
        print('Connection from {}'.format(self.addr))
        msg = " Welcome to this private chat server ! ".center(80, '=')
        msg += '\n You will be defaulted to room 0. To join another room, or create one, please type :\n'\
               '/join <room name>\n\nTo change your nickname, please type :\n/nickname <new name>'
        msg += '\n\nTo see Rooms available and clients, type :\n/show rooms\n'
        msg += '=' * 80
        msg = chat.prep_msg(msg)
        self.transport.write(msg)
        rooms["Room 0"].append(self)
        self.room = "Room 0"

    def data_received(self, data):
        """ Handle data as it's received. Broadcast complete
        messages to all other clients """
        data = self._rest + data
        (msgs, rest) = chat.parse_recvd_data(data)
        self._rest = rest
        for msg in msgs:
            msg = msg.decode('utf-8')
            print('{} - {} : {}'.format(self.addr, nicknames[self], msg))
            if msg[0] == '/':
                if msg.split(' ', 1)[0] == '/nickname':
                    nicknames[self] = msg.split(' ',1)[1]
                elif msg.split(' ', 1)[0] == '/join':
                    room = msg.split(' ',1)[1]
                    if room not in rooms.keys():
                        rooms[room] = []
                    msg = "{} this room <{}> for the room <{}>".format(
                        nicknames[self], self.room, room
                    )
                    msg = chat.prep_msg(msg)
                    for client in rooms[self.room]:
                        client.transport.write(msg)
                    rooms[self.room].remove(self)
                    rooms[room].append(self)
                    self.room = room
                    msg = "{} joined this room <{}>".format(
                        nicknames[self], room
                    )
                    msg = chat.prep_msg(msg)
                    for client in rooms[room]:
                        client.transport.write(msg)

                elif msg == '/show rooms':
                    msg = ''
                    for room in rooms.keys():
                        header = ' ' + room + ' '
                        msg += header.center(80, '=')
                        if rooms[room]:
                            for client in rooms[room]:
                                msg += '\n- ' + str(nicknames[client])
                        else:
                            msg += '\n- <empty>'
                        msg += '\n'
                    msg += '=' * 80
                    msg = chat.prep_msg(msg)
                    self.transport.write(msg)
            else :
                msg = '{}: {}'.format(nicknames[self], msg)
                msg = chat.prep_msg(msg)
                for client in rooms[self.room]:
                    client.transport.write(msg) # <-- non-blocking

    def connection_lost(self, ex):
        """ Called on client disconnect. Clean up client state """
        print('Client {} disconnected'.format(self.addr))
        clients.remove(self)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Create server and initialize on the event loop
    coroutine = loop.create_server(ChatServerProtocol, host=HOST, port=PORT)
    server = loop.run_until_complete(coroutine)
    # print listening socket info
    for socket in server.sockets:
        addr = socket.getsockname()
        print('Listening on {}'.format(addr))
    # Run the loop to process client connections
    loop.run_forever()