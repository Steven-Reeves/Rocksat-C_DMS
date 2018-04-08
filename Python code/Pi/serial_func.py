# Author: 	Andy Horn
# Date:		4/4/18
# Modified: 	4/5/18
#
# Purpose: Functions to read serial data and write to a file.


from threading import Timer
import serial
#import RPi.GPIO as GPIO # Only runs ON the Pi, will not run on Windows.

#GPIO.setwarnings(False) # Turn warnings off
#GPIO.setmode(GPIO.BOARD) # Use the GPIO pin numbers printed on the Pi
# chan_in = [] # put all necessary input channels (pins) in this list
# chan_out = [] # put all necessary output channels (pins) in this list
# GPIO.setup(chan_in, GPIO.IN)
# GPIO.setup(chan_out, GPIO.OUT)

# Original code by Steven:
# s1 = serial.Serial("/dev/ttyAMA0",9600)  #change ACM number as found from ls /dev/tty/ACM*
# s2 = serial.Serial(port, baudrate)

def timeout(run, port):
	print("Timeout, thread ceased.")
	port.write('R')
	run[0] += 1

def read_serial(port, baudrate=9600, filename='none', file_type='.txt', wait_time=1):
        run = [0]
        if filename == 'none':
            filename = 'serial_in'
        s = serial.Serial(port, baudrate)
        # Commented out line below for Python 3.5
        #file = open(filename + file_type, 'w')
        # Line below is for Python 3.5:
        file = open(filename + file_type, 'wb')
        try:
            while run[0] < 5:
                timer = Timer(wait_time, timeout, (run,s))
                timer.start()
                buffer = s.readline() # reads bytes of data, default = 1
                timer.cancel()
                # decode if necessary
                file.write(buffer)
                print(str(buffer))
            if run[0] == 5:
                    s.close()
                    file.close()
                    print("Arduino failed 5 times, Exit thread")
        except KeyboardInterrupt:
            s.close()
            file.close()

            #wooooo!