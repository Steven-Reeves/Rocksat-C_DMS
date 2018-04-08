# Author: 	    Andy Horn
# Date:		    4/4/18
# Modified: 	4/8/18
# Filename:     serial_func.py
# Overview:     Defines functions to read serial data from a USB port, then print
#               the data to the screen and write it to a file.


from threading import Timer
import serial
import time

def timeout(port, name):
    print("[Timeout] Device [{}] is unresponsive, flushing port.".format(name))
    port.flush()
    print("[Timeout] Port flushed")

def read_serial(port, baudrate=9600, filename='none', file_type='.txt', wait_time=1, retries=0):
    num_failures = 0
    if filename == 'none':
        filename = 'serial_in'
    s = serial.Serial(port, baudrate, timeout=wait_time*2)
    time.sleep(.01)
    file = open(filename + file_type, 'wb')
    try:
        while True:
            if wait_time > 0:
                timer = Timer(wait_time, timeout, (s, port))
                timer.start()

            buffer = s.readline()

            if wait_time > 0:
                timer.cancel()
            if buffer != b'':
                file.write(buffer)
                print("[{}] {}".format(port, str(buffer)))
            else:
                print("[{}] No input".format(port))
                num_failures += 1
                if num_failures >= retries:
                    print("Device [{}] has failed, exiting thread.".format(port))
                    s.close()
                    file.close()
                    break
    except KeyboardInterrupt:
        s.close()
        file.close()
    finally:
        s.close()
        file.close()
