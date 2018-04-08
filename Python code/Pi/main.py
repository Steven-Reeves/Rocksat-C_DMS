# Goal: Read serial data from multiple ports through multiple threads.
# Author:	Andy Horn
# Date:		4/4/2018
# Modified:	4/8/2018

from DataThread import DataThread
from serial_func import read_serial

try:
    dt = DataThread()
    dt.add_thread(read_serial, "/dev/ttyACM0", 9600, "Test-1")
    dt.add_thread(read_serial, "/dev/ttyACM1", 9600, "Test-2")
	# Tests for USB hub local to Steven's pi
	#dt.add_thread(read_serial, "/dev/ttyUSB0", 9600, "Test-2")
	#dt.add_thread(read_serial, "/dev/ttyUSB1", 9600, "Test-3")
	#dt.add_thread(read_serial, "/dev/ttyUSB2", 9600, "Test-4")
    dt.start(True)
except KeyboardInterrupt:
    print("Exit main")
