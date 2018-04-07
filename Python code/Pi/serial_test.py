import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
s = [0]
try:
	while True:
		#read_serial = ser.readline()
		#s[0] = str(int(ser.readline(),16))
		#print s[0]
		print ser.readline()

except KeyboardInterrupt:
	ser.close()
