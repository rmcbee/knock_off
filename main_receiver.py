# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

#Neopixel stuff
import time
from time import sleep

from neopixel import *

import argparse
import signal
import sys

#TCP communication stuff
import socket

def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)

def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true', help='clear the display on exit')
        args = parser.parse_args()
        if args.c:
                signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)
		
# Main program logic follows:
if __name__ == '__main__':
	# Process arguments
	opt_parse()

	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	
	#TCP communication stuff
	#TCP_IP = '192.168.1.117'
	TCP_IP = '169.254.186.163'
	TCP_PORT = 5005

	BUFFER_SIZE = 100

	message = "Hello, World!"

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect((TCP_IP, TCP_PORT))

	print ('Press Ctrl-C to quit.')
	try:
		while True:
			
			data = s.recv(BUFFER_SIZE)
			if data:
				print(str(data))
				if(str(data) == "basic"):
					colorWipe(strip, Color(255, 0, 0))  # Red wipe
					
				elif(str(data) == "shave"):
					colorWipe(strip, Color(0, 255, 0))  # Blue wipe
					
				else:
					colorWipe(strip, Color(0, 0, 255))  # Green wipe
			sleep(10)
			colorWipe(strip, Color(0, 0,0))
	finally:
		s.close()
