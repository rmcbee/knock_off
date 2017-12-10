
from enum import Enum

class knock_state(Enum):
	IDLE = 0
	RECORD_KNOCK = 1
	WAIT_FOR_KNOCK_TO_FINISH = 2
	EXIT_KNOCK = 3



class piezo:
	def __init__(spi, port_pin):
		#variables required to read the adc
		self.spi = spi	#reference to the mcp3008 class
		self.port_pin = port_pin #the pin on the mcp3008 that the piezo is on

		#the value of the piezo exponentially averaged
		#this value is initially set to the first value it reads
		self.average = self.ReadChannel(self.port_pin)

		#file where to save the data if we want to record
		#the piezo data
		self.file_to_save_to = None

		#status of whether the data should record its data to 
		#an external file
		self.record_data_status = False

		#used to indicate if a knock has occured
		self.knock_available = False

		#state machine state
		self.knock_upper_threshold = 350
		self.knock_lower_threshold = 70
		self.state = IDLE


	# Function to read SPI data from MCP3008 chip
	# Channel must be an integer 0-7
	def ReadChannel(channel):
		adc = self.spi.xfer2([1,(8+channel)<<4,0])
		data = ((adc[1]&3) << 8) + adc[2]
		return data

	def sample():
		self.average = (self.average >> 4) * 15 + (self.ReadChannel >> 4)

		return self.average

	def set_write_file(file_name):
		self.file_to_save_to = file_name

	def data_to_file():
		self.file_to_save_to.write(self.average)
		self.file_to_save_to.write("\n")

	def has_knock_occured():
		returnVal = self.knock_available
		self.knock_available = False

		returnVal returnVal

	@property
	def knock_available(self):
		if(self.knock_available):
			self.knock_available = False
			return True
		else:
			return False

	def calculate_next_knock_state():
		#the states are not going to change unless explicietly done


		#state for when no signal has appeared
		if(self.state == IDLE):
			if(self.average > self.knock_upper_threshold):
				self.state = RECORD_KNOCK
		#record that a knock has been complete
		elif(self.state == RECORD_KNOCK):
			#set tje knock available to be true
			self.knock_available = True
			#go to the the wait for knock to finish state
			self.state = WAIT_FOR_KNOCK_TO_FINISH
		#waiting for the vibrations form the knock settle down
		elif(self.state == WAIT_FOR_KNOCK_TO_FINISH):
			if(self.average < self.knock_lower_threshold):
				self.state = EXIT_KNOCK
		elif(self.state == EXIT_KNOCK):
			#go to the the wait for knock to finish state
			self.state = IDLE
		#default state. This should never be reached
		else
			#incase things go wrong, go to the IDLE state
			self.state = IDLE