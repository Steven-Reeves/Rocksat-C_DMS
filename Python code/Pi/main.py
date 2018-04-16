# Goal: Read serial data from multiple ports through multiple threads.
# Author:	Andy Horn and Steven Reeves
# Date:		4/4/2018
# Modified:	4/15/2018

from DataThread import DataThread


try:
    dt = DataThread()
    # Tests for USB hub local to Andy's pi
    #dt.add_thread("/dev/ttyACM0", 57600, "Test-1")
    #dt.add_thread("/dev/ttyACM1", 57600, "Test-2")
	# Tests for USB hub local to Steven's pi
    #dt.add_thread("/dev/ttyACM0", 57600, "Test-1")
	#dt.add_thread("/dev/ttyUSB0", 9600, "Test-2")
	#dt.add_thread("/dev/ttyUSB1", 9600, "Test-3")
	#dt.add_thread("/dev/ttyUSB2", 9600, "Test-4")
    # Tests for USB hub local to Steven's PC
    dt.add_thread("COM4", 57600, "Test-1")
    dt.start()
except KeyboardInterrupt:
    print("Exit main")
