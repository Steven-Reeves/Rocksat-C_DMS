# Author: 	    Andy Horn
# Date:		    4/4/18
# Modified: 	4/5/18
#
# Purpose: Functions to read serial data and write to a file.


from threading import Timer
import serial

def timeout(port, name):
    print("[Timeout] Device on port {} timeout, flushing port.".format(name))
    port.flush()
    print("[Timeout] Port flushed")
	#port.write('R')
	#run[0] += 1

def read_serial(port, baudrate=9600, filename='none', file_type='.txt', wait_time=1):
    num_failures = 0
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
                buffer = s.readline(timeout=wait_time) # reads bytes of data, default = 1
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
