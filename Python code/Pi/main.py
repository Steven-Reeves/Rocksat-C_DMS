# Author:	Andy Horn
# Date:		4/4/2018
# Modified:	4/18/2018
# Purpose:  Start threads for serial reading from multiple devices to multiple files

from DataThread import DataThread

dt = DataThread()
# add_thread(port, baudrate=9600, filename='none', file_type='.txt')

# Tests for USB hub local to Andy's pi:
# dt.add_thread("/dev/ttyACM0", 57600, "Test-1")
# dt.add_thread("/dev/ttyACM1", 57600, "Test-2")

# Tests for USB hub connected to Windows PC:
# dt.add_thread("COM4", 57600, "Delay500")
dt.add_thread("COM7", 57600, "GeigerTest")

# Tests for USB hub local to Steven's pi:
# dt.add_thread("/dev/ttyACM0", 57600, "Test-1")
# dt.add_thread("/dev/ttyUSB0", 9600, "Test-2")
# dt.add_thread("/dev/ttyUSB1", 9600, "Test-3")
# dt.add_thread("/dev/ttyUSB2", 9600, "Test-4")

dt.start()
