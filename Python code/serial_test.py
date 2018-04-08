import serial
import pigpio

# Initial pins for testing pigpio library
RX=23
TX=24

ser = serial.Serial('/dev/serial0',9600, timeout=1)

#n = 'checkme out'
#ser.write (str(n).encode())
ser.close()
ser.open()
testInput = "testing"
ser.write(testInput.encode())

#s = [0]
try:
    while 1:
        print("Reading....")
        read_serial=ser.readline()
        #s[0] = str(int (ser.readline(),16))
        #print (s[0])
        print (read_serial)
except KeyboardInterrupt:
    ser.close()
        
