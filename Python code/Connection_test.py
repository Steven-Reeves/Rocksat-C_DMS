# Author: Steven Reeves
# Co-author: Andy Horn
# Last Modified: 4/4/18
#
# Testing connection between Arduino and Raspberry Pi using GPIO pins and Serial data transmission



import serial
import RPi.GPIO as GPIO # Only installable ON the Pi, will not run on Windows.
from DataThread import DataThread
import time

# Added by Andy:
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Use the GPIO pin numbers printed on the Pi
chan_in = [] # put all necessary input channels (pins) in this list
chan_out = [] # put all necessary output channels (pins) in this list
GPIO.setup(chan_in, GPIO.IN)
GPIO.setup(chan_out, GPIO.OUT)

# Original code by Steven:
ser = serial.Serial("/dev/ttyAMA0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600


while True:
    print("Reading serial line...")
    read_ser = ser.readline()
    # read_byte = ser.read() # read() reads a number of bytes (default = 1)
    # read_byte = read_byte.decode("UTF-8") # decode incoming bytes if necessary
    print (read_ser)
