# Goal: Read serial data from multiple ports through multiple threads.
# Author:	Andy Horn
# Date:		4/4/2018
# Modified:	4/5/2018

from DataThread import DataThread
#from serial_func import read_serial
from thread_func import print_time, timer_test

dt = DataThread()
#dt.add_thread(read_serial, port="/dev/ttyAMA0", baudrate=9600, filename="Test-1")
dt.add_thread(print_time,'Thread-1', 5)
dt.add_thread(print_time,'Thread-2', 5, 2)
dt.add_thread(timer_test)
dt.start(True)