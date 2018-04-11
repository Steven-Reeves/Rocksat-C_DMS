# Author:       Andy Horn
# Date:	        4/4/18
# Modified: 	4/10/18
# Filename:     serial_func.py
# Overview:     Defines functions to read serial data from a USB port, then print
#               the data to the screen and write it to a file.


from threading import Timer
import serial
import time

def mainTimerComplete(run):
    del run[0]
    print("[times_up] Countdown complete.")

def serialReadTimeout(port, name):
    print("[Timeout] Device [{}] is unresponsive, flushing port.".format(name))
    port.flush()
    print("[Timeout] Port flushed")

def read_serial(port, baudrate=9600, filename='none', file_type='.txt', wait_time=2, retries=1):
    num_failures = 0
    run = ['true']
    countdown = Timer(60, mainTimerComplete, (run,))
    countdown.start()
    if filename == 'none':
        filename = 'serial_in'
    try:
        with serial.Serial(port, baudrate, timeout=wait_time*2, dsrdtr=True) as s:
            with open(filename + file_type, 'a') as file:
                while run:
                    if wait_time > 0:
                        timer = Timer(wait_time, serialReadTimeout, (s, port))
                        timer.start()
                        buffer = s.readline().decode('ascii')
                    if wait_time > 0:
                        timer.cancel()
                    if buffer.split():
                        file.write(buffer)
                        print("[{}] {}".format(port, str(buffer)))
                    else:
                        print("[{}] No input".format(port))
                        num_failures += 1
                        if num_failures > retries:
                            print("Device [{}] has failed, exiting thread.".format(port))
                            break
    except KeyboardInterrupt:
        print("[read_serial] KeyboardInterrupt")
    except:
        print("[read_serial] Unhandled Exception")
    finally:
        print("[read_serial] Exit Code 0")
