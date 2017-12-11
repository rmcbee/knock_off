



#For USB camera
from time import gmtime, strftime, sleep
from os import system


#For TCP communication
import socket


def takePicture():
	
	fileName = strftime("y%Y-m%m-d%d___h%H-m%M-s%S", gmtime())
	system("fswebcam -S 20 -r 1280x720 --no-banner ./temp/" + fileName + ".jpg")

	with open("./photos/" + fileName + ".html", "w") as f:
		f.write("<img src=\"./../temp/" + fileName + ".jpg\" style=\"max-width: 100%; height: auto;\"></img>")

def setup():
	system("./photos/server&")
	pass
	

if __name__ == "__main__":
	#Do the intial setup of things
	setup()	

	#Must be the IP address of this computer
	#Use ifconfig to find this out
	TCP_IP = '192.168.1.103'

	TCP_PORT = 5005

	BUFFER_SIZE = 100  # Normally 1024, but we want fast response

	print(TCP_PORT)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)

	conn, addr = s.accept()
	print('Connection address:' + str(addr))
	
	#Variables used inside of the loop
	message = "Hello World" #Message to be send over TCP
	knockSensed = False #True when a knock is detected

	try:
		takePicture()
		while 1:
			
			#Insert code here to trigger changing the message being sent
			message = message[-1] + message[:-1]

			#Uncomment if you want to reciever data from the client
			#data = conn.recv(BUFFER_SIZE)
			#if data:
				#pass				
				#print("received data: " + str(data.decode("utf-8") ))
			
			if knockSensed:
				b = bytearray()
				b.extend(map(ord, message))
				conn.sendall(b)  # echo
				takePicture()
				knockSensed = False

	finally:
		conn.close()
