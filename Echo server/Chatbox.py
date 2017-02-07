# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '04/02/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
import sys, socket, threading, tkinter as tk

HOST = sys.argv[-1] if len(sys.argv) > 1 else '92.134.224.55'
PORT = 4242

def create_listen_socket(host, port):
    """ Setup the sockets our server will receive connection requests on """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)
    return sock

def recv_msg(sock):
    """ Wait for data to arrive on the socket, then parse into messages using b'\0' as message delimiter """
    data = bytearray()
    msg = ''
    # Repeatedly read 4096 bytes off the socket, storing the bytes
    # in data until we see a delimiter
    while not msg:
        recvd = sock.recv(4096)
        if not recvd:
            # Socket has been closed prematurely
            raise ConnectionError()
        data = data + recvd
        if b'\0' in recvd:
            # we know from our protocol rules that we only send
            # one message per connection, so b'\0' will always be
            # the last character
            msg = data.rstrip(b'\0')
    msg = msg.decode('utf-8')
    return msg

def prep_msg(msg):
    """ Prepare a string to be sent as a message """
    msg += '\0'
    return msg.encode('utf-8')

def send_msg(sock, msg):
    """ Send a string over a socket, preparing it first """
    data = prep_msg(msg)
    print("Sending data %s" % data)
    sock.sendall(data)

def parse_recvd_data(data):
    """ Break up raw received data into messages, delimited by null byte """
    parts = data.split(b'\0')
    msgs = parts[:-1]
    rest = parts[-1]
    return (msgs, rest)

def recv_msgs(sock, data=bytes()):
    """ Receive data and break into complete messages on null byte
    delimiter. Block until at least one message received, then return received messages """
    msgs = []
    while not msgs:
        recvd = sock.recv(4096)
        if not recvd:
            raise ConnectionError()
        data = data + recvd
        (msgs, rest) = parse_recvd_data(data)
        msgs = [msg.decode('utf-8') for msg in msgs]
        return (msgs, rest)

class ChatBox(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Custom chat client')

        self.UI = {0 : self}
        self.UI[1] = tk.Frame(self.UI[0])
        self.UI[1].pack(fill=tk.X, expand=True, side=tk.TOP)
        self.UI[1, 1] = Consol(self.UI[1], 1)
        self.UI[1, 1].pack(fill=tk.X, expand=True, side=tk.TOP)
        self.UI[1, 2] = Consol(self.UI[1], 30)
        self.UI[1, 2].pack(fill=tk.X, expand=True, side=tk.TOP)
        self.UI[1, 3] = tk.Entry(self.UI[1])
        self.UI[1, 3].pack(fill='x', padx=4, side=tk.TOP)
        self.UI[1, 3].bind("<Return>", self.on_return)

        self.UI[1,1].display('=' * 31 + ' - chat server - ' + '=' * 31)
        self.main()
    
    def main(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        # Create thread for handling user input and message sending
        # Loop indefinitely to receive messages from server
        thread = threading.Thread(target=self.receive, args=[], daemon=True)
        thread.start()

    def receive(self):
        rest = bytes()
        while True:
            try:
                # blocks
                (msgs, rest) = recv_msgs(self.sock, rest)
                for msg in msgs:
                    self.UI[1,2].display(msg)
            except ConnectionError:
                self.UI[1,1].display('Connection to server closed')
                self.sock.close()
                break

    def on_return(self, unused_ev):
        msg = self.UI[1, 3].get()
        print(msg)
        send_msg(self.sock, msg)
        self.UI[1, 3].delete(0, tk.END)

class Consol(tk.Text):
    """ Custom Text widget that can only display """

    def __init__(self, master=None, height=20, **kwargs):
        tk.Text.__init__(self, master, bd=2, bg="white", height=height, highlightthickness=0, state='disabled', relief='ridge')

    def empty(self):
        self.delete(1.0, tk.END)

    def display(self, text, end='\n', empty=False):
        self.configure(state='normal')
        if empty: self.empty()
        self.insert(tk.END, '{0}\n'.format(text))
        self.configure(state='disable')

if __name__ == '__main__':
    test = ChatBox()
    test.mainloop()