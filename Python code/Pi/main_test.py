# Author:	Andy Horn
# Date:		4/4/2018
# Modified:	4/10/2018
# Filename:     main_auto.py
# Overview:     Uses the sniff function to automatically detect USB devices
#               and begin independent threads for each device at baud=57600.
#               This was more for my own experimentation and potential future use
#               than for use in this year's (2018) Rocksat-C program.

from DataThread import DataThread
from serial_func import read_serial
import sniff

try:
    portList = sniff.sniff()
    print("Found {} ports in use.".format(len(portList)))
    if len(portList) > 0:
        dt = DataThread()
        for port in portList:
            dt.add_thread('/dev/'+port, 57600, port)
            print("Connected to {}.".format(port))
        dt.start()
except KeyboardInterrupt:
    print("Exit main")