from SocketServer import TCPServer,BaseRequestHandler,StreamRequestHandler
from message import message
from time import sleep
import threading
import socket

ack = "Acknowledged."

class ServerHandler(BaseRequestHandler):    
    commandList = []

    def handle(self): 
        self.data = self.request.recv(1024).strip()
        print "{} (commander) wrote: %s".format(self.client_address[0]) % self.data
        self.SendResponse()
        self.request.close()

    def SendResponse(self):
        splitRequest = self.data.split(" ")
        if splitRequest[0] == "clear":
            ServerHandler.commandList = []
            response = "Cleared List."
        elif splitRequest[0].isdigit():
            num = int(splitRequest[0])
            if num < len(ServerHandler.commandList):
                response = ServerHandler.commandList(int(splitRequest[0]))
            else:
                response = "Number is too large."
        elif splitRequest[0] == "size":
            response = str(len(ServerHandler.commandList))
        elif splitRequest[0] == "list" or splitRequest[0] == "queue":
            response = "Command Queue:\n\t" + ("\n\t".join(ServerHandler.commandList))
#        elif splitRequest[0] == "getfile":
#            command = "cat " + " ".join(splitRequest[1:])
#            ServerHandler.commandList.append(command)
#            response = command
        elif splitRequest[0] == "add" or splitRequest[0] == "a":
            command = " ".join(splitRequest[1:])
            ServerHandler.commandList.append(command)
            response = self.data
        elif len(splitRequest) > 0:
            command = self.data
            ServerHandler.commandList.append(command)
            response = self.data
        else:
            print "Empty line received."
            response = ""
        print "Response: %s" % response
        self.request.sendall(response)

class PiMaster(StreamRequestHandler):
    def handle(self):
        mes = message.readMessage(self.rfile)
        self.data = mes.getMessage()
        self.SendResponse()
        if mes.command != "get":
            print "{} (soldier) wrote: %s".format(self.client_address[0]) % mes.getMessage()
            self.tellClient()
        self.request.close()
        
    def SendResponse(self):
        if len(ServerHandler.commandList) > 0:
            response = ServerHandler.commandList[0]
            ServerHandler.commandList.remove(response)
        else:
            response = "\0"
        self.request.sendall(response)

    def tellClient(self):
        try:
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientSocket.connect(("localhost", 739))
            self.clientSocket.sendall(self.data)
        finally:
            self.clientSocket.close()

interrupt = False
while True:
    try:
        pimasterserver = TCPServer(("localhost", 738), PiMaster)
        commandserver = TCPServer(("localhost", 737), ServerHandler)
        commandThread = threading.Thread(target=commandserver.serve_forever, args=())
        commandThread.start()
        print "Serving forever..."
        pimasterserver.serve_forever()
    except socket.error as se:
        print se
        print se.message
        print "Error occurred, sleeping..."
        sleep(1)
        print "Restarting..."
    except KeyboardInterrupt as ki:
        interrupt = True
    finally:
        try:
            pimasterserver.shutdown()
            commandserver.shutdown()
        except:
            pass
        if interrupt:
            break
