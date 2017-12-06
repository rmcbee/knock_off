import spidev
from time import sleep
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data
  
# Define sensor channels
pot_channel = 0

piezo_channel = 1

# Define delay between readings
delay = 0.0001
curr_time = 0

averagedPiezoLevel = ReadChannel(piezo_channel);

piezo_file = open('piezoData.csv', 'w')

triggered = False

pot_level = 70

while True:

	# Read the light sensor data
	piezo_level = ReadChannel(piezo_channel)


	#exponential average of the piezo data
	averagedPiezoLevel = (averagedPiezoLevel >> 4) * 15 + (piezo_level >> 4)

	'''if(averagedPiezoLevel > pot_level and triggered == False):
		print("piezo: {}, pot: {}".format(str(averagedPiezoLevel), str(pot_level)))
		triggered = True
		#piezo_file.write(str(curr_time) + " , " + str(averagedPiezoLevel) + '\n')
	elif (triggered == True):
		print("out")
		triggered = False'''

	if(averagedPiezoLevel > 5):
		print(averagedPiezoLevel)

	# Wait before repeating loop
	sleep(delay)

	curr_time = curr_time + delay
 
