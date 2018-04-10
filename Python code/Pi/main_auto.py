# Goal: Read serial data from multiple ports through multiple threads.
# Author:	Andy Horn
# Date:		4/4/2018
# Modified:	4/10/2018

from DataThread import DataThread
from serial_func import read_serial
import sniff

try:
    portList = sniff.sniff()
    print("Found {} ports in use. Connecting.".format(len(portList)))
    dt = DataThread()
    for port in portList:
        dt.add_thread(read_serial, '/dev/'+port, 57600, port)
        print("Connected to {}.".format(port))
    dt.start(True)
except KeyboardInterrupt:
    print("Exit main")
