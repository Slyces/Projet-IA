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
import sys, socket, threading
import chat
HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = chat.PORT
def handle_input(sock):
    """ Prompt user for message and send it to server """
    print("Type messages, enter to send. 'q' to quit")
    while True:
        msg = input() # Blocks
        if msg == 'q':
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            break
        try:
            chat.send_msg(sock, msg) # Blocks until sent
        except (BrokenPipeError, ConnectionError):
            break

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print('Connected to {}:{}'.format(HOST, PORT))
    # Create thread for handling user input and message sending
    thread = threading.Thread(target=handle_input, args=[sock], daemon=True)
    thread.start()
    rest = bytes()
    addr = sock.getsockname()
    # Loop indefinitely to receive messages from server
    while True:
        try:
            # blocks
            (msgs, rest) = chat.recv_msgs(sock, rest)
            for msg in msgs:
                print(msg)
        except ConnectionError:
            print('Connection to server closed')
            sock.close()
            break