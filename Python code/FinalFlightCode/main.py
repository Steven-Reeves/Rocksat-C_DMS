# Author:	Andy Horn
# Date:		4/4/2018
# Modified:	4/18/2018
# Purpose:  Start threads for serial reading from multiple devices to multiple files

from DataThread import DataThread

dt = DataThread()
# add_thread(port, baudrate=9600, filename='none', file_type='.txt')

# Ports relative to USB hub on board:
dt.add_thread("/dev/ttyACM0", 9600, "Module-1")
dt.add_thread("/dev/ttyUSB0", 9600, "Module-2")
dt.add_thread("/dev/ttyUSB1", 9600, "Module-3")
dt.add_thread("/dev/ttyUSB2", 9600, "Module-4")

dt.start()
