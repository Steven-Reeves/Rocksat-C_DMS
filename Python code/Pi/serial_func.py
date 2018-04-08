# Author: 	    Andy Horn
# Date:		    4/4/18
# Modified: 	4/5/18
#
# Purpose: Functions to read serial data and write to a file.


from threading import Timer
import serial
import time

def timeout(port, name):
    print("[Timeout] Device on port {} timeout, flushing port.".format(name))
    port.flush()
    print("[Timeout] Port flushed")

def read_serial(port, baudrate=9600, filename='none', file_type='.txt', wait_time=1):
    num_failures = 0
    if filename == 'none':
        filename = 'serial_in'
    s = serial.Serial(port, baudrate, timeout=wait_time*2)
    time.sleep(.01)
        # Commented out line below for Python 3.5
        #file = open(filename + file_type, 'w')
        # Line below is for Python 3.5:
    file = open(filename + file_type, 'wb')
    try:
        while True:
            if wait_time > 0:
                timer = Timer(wait_time, timeout, (s, port))
                timer.start()
            buffer = s.readline() # reads bytes of data, default = 1
            if wait_time > 0:
                timer.cancel()
            # decode if necessary
            if buffer != '':
                file.write(str(buffer))
                print("[Buffer] {}".format(str(buffer)))
            else:
                print("[read_serial] No input")
                num_failures += 1
                if num_failures >= retries:
                    print("Device {} failed, exiting thread.".format(port))
                    s.close()
                    file.close()
                    break
    except KeyboardInterrupt:
        s.close()
        file.close()
    finally:
        s.close()
        file.close()
