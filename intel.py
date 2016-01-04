from SocketServer import TCPServer,BaseRequestHandler
from time import sleep
import threading
import socket

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
        elif splitRequest[0] == "add" or splitRequest[0] == "a":
            command = " ".join(splitRequest[1:])
            ServerHandler.commandList.append(command)
            response = command
        elif len(splitRequest) > 0:
            command = self.data
            ServerHandler.commandList.append(command)
            response = command
        else:
            print "Empty line received."
            response = ""
        print "Response: %s" % response
        self.request.sendall(response)

class PiMaster(BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.SendResponse()
        if self.data != "get":
            print "{} (soldier) wrote: %s".format(self.client_address[0]) % self.data
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
while True:
    try:
        commandserver = TCPServer(("localhost", 737), ServerHandler)
        commandThread = threading.Thread(target=commandserver.serve_forever, args=())
        commandThread.start()
        pimasterserver = TCPServer(("localhost", 738), PiMaster)
        print "Serving forever..."
        pimasterserver.serve_forever()
    except socket.error as se:
        print se
        print "Error occurred, sleeping..."
        sleep(5)
        print "Restarting..."
    except KeyboardInterrupt as ki:
        pass
    finally:
        pimasterserver.shutdown()
        commandserver.shutdown()
