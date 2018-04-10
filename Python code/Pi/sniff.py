from subprocess import Popen, PIPE
def sniff():
    data = Popen(['ls', '/dev/'], stdout=PIPE).communicate()
#print(data[0])
    data = data[0].decode('ascii').split('\n')
#ports = ports.decode('ascii')
#ports = ports.split('\n')
#print(ports)
    ports = []
    for line in data:
        if 'ttyACM' in line:
        #print(line)
            ports.append(line)
        elif 'ttyUSB' in line:
        #print(line)
            ports.append(line)
        elif 'ttySerial' in line:
        #print(line)
            ports.append(line)
#    print(ports)
    return ports
