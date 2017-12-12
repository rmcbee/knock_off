



#For USB camera
from time import gmtime, strftime, sleep
import time
from os import system

#for piezo handling
import spidev
from piezoHandler import *
from knockDetector import *
from predictKnock import *

current_milli_time = lambda: int(round(time.time() * 1000))


#For TCP communication
import socket

from random import randint

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
	TCP_IP = '192.168.1.120'

	TCP_PORT = 5005

	BUFFER_SIZE = 100  # Normally 1024, but we want fast response

	#print(TCP_PORT)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)

	conn, addr = s.accept()
	#print('Connection address:' + str(addr))
	
	#Variables used inside of the loop
	message = "Hello World" #Message to be send over TCP
	knockSensed = False #True when a knock is detected
	responses = ["Hello World", "shave", "something else"]

	#Set up code for the piezo
	spi = spidev.SpiDev()
	spi.open(0,0)

	#piezo 1
	piezo1_channel = 1
	piezo1 = piezo(spi, piezo1_channel) #create the pizeo class

	delay = 0.00005

	clf = generateKnockTree()

	try:
		while 1:
			
			#wait until the first knock is heard
			while not piezo1.knock_available:
				piezo1.sample()
				sleep(delay)

			knock_times = []

			knock_counter = 0

			#print("Next reading.")

			prevTime = current_milli_time()

			while(1):	
				value = piezo1.sample()
				if(piezo1.knock_available):
					#print(value)
					curtime = current_milli_time()
					knock_times.append(curtime - prevTime)
					knock_counter = knock_counter + 1
					prevTime = current_milli_time()


				sleep(delay)

				#break out if the data is of size 10
				if knock_counter >= 10:
					break

				#if the time between knocks is greater than 2 seconds, break out
				if (current_milli_time() - prevTime) > 2000:
					break

			#A knock has been sensed

			#pad the knock_times variable with 0s until there are 10 values
			for i in range(10 - len(knock_times)):
				knock_times.append(0)

			if (clf.predict([knock_times])[0]) == 0:
				message = "shave" 
			else:
				message = "basic"

			b = bytearray()
			b.extend(map(ord, message))
			conn.sendall(b)  # echo
			#takePicture()
			knockSensed = False
			sleep(5)

	finally:
		conn.close()
