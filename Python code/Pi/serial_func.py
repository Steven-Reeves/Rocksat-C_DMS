# Author: 	Andy Horn
# Date:		4/4/18
# Modified: 	4/5/18
#
# Purpose: Functions to read serial data and write to a file.


import serial
import RPi.GPIO as GPIO # Only runs ON the Pi, will not run on Windows.

GPIO.setwarnings(False) # Turn warnings off
GPIO.setmode(GPIO.BOARD) # Use the GPIO pin numbers printed on the Pi
# chan_in = [] # put all necessary input channels (pins) in this list
# chan_out = [] # put all necessary output channels (pins) in this list
# GPIO.setup(chan_in, GPIO.IN)
# GPIO.setup(chan_out, GPIO.OUT)

# Original code by Steven:
# s1 = serial.Serial("/dev/ttyAMA0",9600)  #change ACM number as found from ls /dev/tty/ACM*
# s2 = serial.Serial(port, baudrate)

def read_serial(port, baudrate=9600, filename, file_type='.txt', num_bytes=1):
        run = True
	#s = serial.Serial(port, baudrate)
		file = open(filename + file_type, 'w')
	while run:
            buffer = s.read(num_bytes) # reads bytes of data, default = 1
            # decode if necessary
            file.write(buffer)
            print(str(buffer))
            
'''
See the thread_func method 'timer_test' and 'alarm' for examples on how to 
implement a timer. We should include a use_timer flag and a time_interval
argument in the read_serial method, this will allow us to use the same method
for every experiment, but alter whether or not a timer is used, and if so, how
long it should wait for Arduino communications before breaking out and 
attempting to reset and reconnect.
'''
                
