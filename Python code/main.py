# Goal: Read serial data from multiple ports through multiple threads.
# Author:	Andy Horn
# Date:		4/4/2018
# Modified:	4/4/2018

from DataThread import DataThread
# from serial_func import read_serial
from thread_func import print_time

dt = DataThread()
# dt.add_thread(read_serial, "/dev/ttyAMA0", 9600, "test-1")
dt.add_thread(print_time,'Thread-1', 15)
dt.add_thread(print_time,'Thread-2', 15, 2)
dt.start(True)


