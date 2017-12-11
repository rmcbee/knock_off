# !/usr/bin/env python

import socket

#Must be the IP address of this computer
#Use ifconfig to find this out
TCP_IP = '192.168.1.103'

TCP_PORT = 5005

BUFFER_SIZE = 20  # Normally 1024, but we want fast response

print(TCP_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:' + str(addr))

while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("received data:" + str(data))
    try:
    	conn.send(data)  # echo
    except:
        conn.close
        break
conn.close()
