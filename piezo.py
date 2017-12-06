

class pizeo:
	def init(spi, port_pin):
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


	# Function to read SPI data from MCP3008 chip
	# Channel must be an integer 0-7
	def ReadChannel(channel):
		adc = self.spi.xfer2([1,(8+channel)<<4,0])
		data = ((adc[1]&3) << 8) + adc[2]
		return data

	def sample():
		self.average = (self.average >> 4) * 15 + (self.ReadChannel >> 4)

		return self.average
