import socket
import sys
from SocketServer import TCPServer,BaseRequestHandler
import threading
from time import sleep

def leave():
    print "\nGoodbye."
    listener.shutdown()
    sys.exit()
    
prompt = "Say: "
class ServerListener(BaseRequestHandler):
    def handle(self):
        print "\n"+self.request.recv(1024).strip()
        print prompt

HOST,PORT = "localhost", 737
#HOST,PORT = "batterystapler.com", 737

##START LISTENER##
listenAddress = ("localhost", 739)
listener = TCPServer(listenAddress, ServerListener)
listenThread = threading.Thread(target=listener.serve_forever, args=())
listenThread.start()

##Run Client##
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        data = raw_input(prompt)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(data + "\n")
        received = sock.recv(1024)
        print received
    except socket.error as se:
        print se
    except EOFError as eof:
        leave()
    except KeyboardInterrupt as ki:
        leave()
    finally:
        sock.close()
