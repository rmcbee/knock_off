import time
from enum import Enum

class knock_state(Enum):
	IDLE = 0
	RECORD_KNOCK = 1
	WAIT_FOR_KNOCK_TO_FINISH = 2
	EXIT_KNOCK = 3



class piezo:
	def __init__(self, spi, port_pin):
		#variables required to read the adc
		self.spi = spi	#reference to the mcp3008 class
		self.port_pin = port_pin #the pin on the mcp3008 that the piezo is on

		#the value of the piezo exponentially averaged
		#this value is initially set to the first value it reads
		self.average = self.ReadChannel()

		#file where to save the data if we want to record
		#the piezo data
		self.file_to_save_to = None

		#status of whether the data should record its data to 
		#an external file
		self.record_data_status = False

		#used to indicate if a knock has occured
		self._knock_available = False

		#state machine state
		self.knock_upper_threshold = 95
		self.knock_lower_threshold = 2
		self.state = knock_state.IDLE


	# Function to read SPI data from MCP3008 chip
	# Channel must be an integer 0-7
	def ReadChannel(self):
		adc = self.spi.xfer2([1,(8+self.port_pin)<<4,0])
		data = ((adc[1]&3) << 8) + adc[2]
		return data

	def sample(self):
		self.average = (((self.average * 15) + (self.ReadChannel())) >> 4)

		#if(value > 10):
		#	print("val" + str(value) + " avg: " + str(self.average))

		self.calculate_next_knock_state()

		return self.average

	def set_write_file(self, file_name):
		self.file_to_save_to = file_name

	def data_to_file(self):
		self.file_to_save_to.write(self.average)
		self.file_to_save_to.write("\n")

	def has_knock_occured(self):
		returnVal = self._knock_available
		self._knock_available = False

		return returnVal

	@property
	def knock_available(self):
		if(self._knock_available):
			self._knock_available = False
			return True
		else:
			return False

	def calculate_next_knock_state(self):
		#the states are not going to change unless explicietly done


		#state for when no signal has appeared
		if(self.state == knock_state.IDLE):
			if(self.average > self.knock_upper_threshold):
				self.state = knock_state.RECORD_KNOCK
		#record that a knock has been complete
		elif(self.state == knock_state.RECORD_KNOCK):
			#set tje knock available to be true
			self._knock_available = True
			#go to the the wait for knock to finish state
			self.state = knock_state.WAIT_FOR_KNOCK_TO_FINISH
		#waiting for the vibrations form the knock settle down
		elif(self.state == knock_state.WAIT_FOR_KNOCK_TO_FINISH):
			if(self.average < self.knock_lower_threshold):
				self.state = knock_state.EXIT_KNOCK
		elif(self.state == knock_state.EXIT_KNOCK):
			#go to the the wait for knock to finish state
			self.state = knock_state.IDLE
		#default state. This should never be reached
		else:
			#incase things go wrong, go to the IDLE state
			self.state = knock_state.IDLE