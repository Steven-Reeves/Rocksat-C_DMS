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

def read_serial(port, baudrate=9600, filename='none', file_type='.txt', wait_time=2, retries=1):
    num_failures = 0
    if filename == 'none':
        filename = 'serial_in'
    with serial.Serial(port, baudrate, timeout=wait_time*2, dsrdtr=True) as s:
#    s.open()
#    time.sleep(.01)
       # s.flush()
       # time.sleep(.02)
#    with open(filename + file_type, 'wb') as file: #can use "with" to automatically close file,
    # or open and close the file each time the while statement executes. Not closing the file
    # properly can lead to blank output, especially in Python3.
        try:
            while True:
#            s.flush()
                if wait_time > 0:
                    timer = Timer(wait_time, timeout, (s, port))
                    timer.start()
#            if s.in_waiting() > 0:
                    buffer = s.readline().decode('ascii')
#            time.sleep(.01)
                if wait_time > 0:
                    timer.cancel()
                if buffer.split():
                    with open(filename + file_type, 'a') as file:
                        file.write(buffer)
#                    file.close()
#                    print("[{}] {}".format(port, str(buffer.decode('ascii'))))
                        print("[{}] {}".format(port, str(buffer)))
                else:
                    print("[{}] No input".format(port))
                    num_failures += 1
                    if num_failures > retries:
                        print("Device [{}] has failed, exiting thread.".format(port))
                        break
                    #s.close()
                    #file.close()
                    #break
        except KeyboardInterrupt:
        #    s.close()
        #file.close()
            print("[read_serial] KeyboardInterrupt")
        except:
        #s.close()
        #file.close()
            print("[read_serial] Unhandled Exception")
        finally:
        #s.close()
        #file.close()
            print("[read_serial] Exit Code 0")
