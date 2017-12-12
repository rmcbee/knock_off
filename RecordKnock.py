#file used to store the knock information so that it can be used in an analysis

import spidev
import time
import os
from piezoHandler import *
from knockDetector import *
from predictKnock import *

current_milli_time = lambda: int(round(time.time() * 1000))


if __name__ == "__main__":

	spi = spidev.SpiDev()
	spi.open(0,0)


	#piezo definitions
	
	#piezo 1
	piezo1_channel = 1
	piezo1 = piezo(spi, piezo1_channel) #create the pizeo class


	#piezo 2
	piezo2_channel = 2
	piezo2 = piezo(spi, piezo2_channel) #create the pizeo class


	#set up the file that is going to writen to
	outFile = open('knock_spacings_basic.csv', 'a')

	delay = 0.00005

	prevTime = 0

	prevTime = current_milli_time()	

	clf = generateKnockTree()

	while(1):
		
		#wait until the first knock is heard
		while not piezo1.knock_available:
			piezo1.sample()
			time.sleep(delay)

		knock_times = []

		knock_counter = 0

		print("Next reading.")

		prevTime = current_milli_time()

		while(1):	
			#value1 = piezo1.ReadChannel()
			value = piezo1.sample()
			if(piezo1.knock_available):
				print(value)
				curtime = current_milli_time()
				knock_times.append(curtime - prevTime)
				knock_counter = knock_counter + 1
				prevTime = current_milli_time()


			time.sleep(delay)

			#break out if the data is of size 10
			if knock_counter >= 10:
				break

			#if the time between knocks is greater than 2 seconds, break out
			if (current_milli_time() - prevTime) > 2000:
				break

		#pad the knock_times variable with 0s until there are 10 values
		for i in range(10 - len(knock_times)):
			knock_times.append(0)

		if (clf.predict([knock_times])[0]) == 0:
			print ("shave")
		else:
			print ("basic")


		#outFile.write(', '.join([str(i) for i in knock_times]))
		#outFile.write("\n")

