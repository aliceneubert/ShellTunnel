import socket
import sys
from SocketServer import TCPServer,BaseRequestHandler,StreamRequestHandler
from message import message
import threading
from time import sleep

def leave():
    print "\nGoodbye."
    listener.shutdown()
    sys.exit()

def writeFile(name, stream):
    with open("otherfile.txt", 'w') as outFile:
        outFile.write(stream)

prompt = "Say: "
class ServerListener(StreamRequestHandler):
    def handle(self):
        mes = message.readMessage(self.rfile)
        #print "\nReceived: \n%s" % mes.getMessage()
        if "getfile" in mes.command:
            filename = " ".join(mes.command.split(" ")[1:])
            writeFile(filename, mes.data[:-1])
        print ""
        print mes.data.strip()
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
        command = raw_input(prompt)
        mes = message(command, "")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(mes.getMessage())
        received = sock.recv(1024)
#        print received
    except socket.error as se:
        print se
    except EOFError as eof:
        leave()
    except KeyboardInterrupt as ki:
        leave()
    finally:
        sock.close()
