# Author: 	Andy Horn
# Date:		4/4/18
# Modified: 	4/4/18
#
# Purpose: Functions to read serial data and write to a file.



import serial
import RPi.GPIO as GPIO # Only runs ON the Pi, will not run on Windows.

GPIO.setwarnings(False) # Turn warnings off
GPIO.setmode(GPIO.BOARD) # Use the GPIO pin numbers printed on the Pi
chan_in = [] # put all necessary input channels (pins) in this list
chan_out = [] # put all necessary output channels (pins) in this list
GPIO.setup(chan_in, GPIO.IN)
GPIO.setup(chan_out, GPIO.OUT)

# Original code by Steven:
s1 = serial.Serial("/dev/ttyAMA0",9600)  #change ACM number as found from ls /dev/tty/ACM*
# s2 = serial.Serial(port, baudrate)

def read_serial(port, baudrate, filename, type_flag=1, num_bytes=1):
	s = serial.Serial(port, baudrate)
	if type_flag == 1:
		file = open(filename + '.txt')
	else:
		file = open(filename + '.csv')
	while True:
		buffer = s.read(num_bytes) # reads 1 byte of data
		# decode if necessary
		file.write(buffer)


while True:
    print("Reading serial line...")
    read_ser = ser.readline()
    # read_byte = ser.read() # read() reads a number of bytes (default = 1)
    # read_byte = read_byte.decode("UTF-8") # decode incoming bytes if necessary
    print (read_ser)
