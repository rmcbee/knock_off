import spidev
import time
import os
from piezoHandler import *
from knockDetector import *


threshold = 50

def print_pound(num):
	for _ in range(int(num/3)):
		print("#", end="")
	print("")

if __name__ == "__main__":

	spi = spidev.SpiDev()
	spi.open(0,0)


	#piezo definitions
	
	#piezo 1
	piezo1_channel = 1
	piezo1_file = open('piezo1Data.csv', 'w')
	piezo1 = piezo(spi, piezo1_channel) #create the pizeo class
	piezo1.set_write_file(piezo1_file) #set the file to write to



	#piezo 2
	piezo2_channel = 2
	piezo2_file = open('piezo2Data.csv', 'w')
	piezo2 = piezo(spi, piezo2_channel) #create the pizeo class
	piezo2.set_write_file(piezo2_file) #set the file to write to


	delay = 0.0000001

	while(1):
		value1 = piezo1.ReadChannel()
		value2 = piezo2.ReadChannel()

		if(piezo1.knock_available):
			print("knock")
			#print_pound(value1)
			#print("O :{} ".format(value1))
			#piezo1.write_data_to_file()

		#if(value2 > threshold):
		#	print("\t T:{} ".format(value2), end="")

		#if(value1 > threshold or value2 > threshold):
		#	print("") # print a blank line

		time.sleep(delay)
