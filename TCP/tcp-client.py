# !/usr/bin/env python

import socket
from time import sleep


TCP_IP = '192.168.1.117'

TCP_PORT = 5005

BUFFER_SIZE = 1024

MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TCP_IP, TCP_PORT))

counter = 0

while 1:
    MESSAGE = "Hello World! " + str(counter)
    s.send(MESSAGE)
    counter = counter + 1
    sleep(1)
    data = s.recv(BUFFER_SIZE)
    print(data)

s.close()

print("received data:" + str(data))
