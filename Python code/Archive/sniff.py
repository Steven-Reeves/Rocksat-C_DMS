# Author:        Andy Horn
# Date:          4/10/2018
# Modified:      4/10/2018
# Filename:      sniff.py
# Overview:      Detects USB ports with active connections and returns a list
#                with each port name.

from subprocess import Popen, PIPE
def sniff():
    data = Popen(['ls', '/dev/'], stdout=PIPE).communicate()
    data = data[0].decode('ascii').split('\n')
    ports = []
    for line in data:
        if 'ttyACM' in line:
            ports.append(line)
        elif 'ttyUSB' in line:
            ports.append(line)
        elif 'ttySerial' in line:
            ports.append(line)
    return ports
