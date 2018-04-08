# Goal: Read serial data from multiple ports through multiple threads.
# Author:	Andy Horn
# Date:		4/4/2018
# Modified:	4/5/2018

from DataThread import DataThread
#from serial_func import read_serial
from thread_func import print_time, timer_test
from serial_func import read_serial

try:
	dt = DataThread()
	dt.add_thread(read_serial, "/dev/ttyACM0", 9600, "Test-1")
	# Tests for USB hub local to Steven's pi
	dt.add_thread(read_serial, "/dev/ttyUSB0", 9600, "Test-2")
	dt.add_thread(read_serial, "/dev/ttyUSB1", 9600, "Test-3")
	dt.add_thread(read_serial, "/dev/ttyUSB2", 9600, "Test-4")
	# dt.add_thread(print_time,'Thread-1', 5)
	#dt.add_thread(print_time,'Thread-2', 5, 2)
	#dt.add_thread(timer_test, 3)
	dt.start(True)
except KeyboardInterrupt:
	dt.purge()
	print("Exit main")
