import serial

ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
ser.close()
ser.open()
testInput = "testing"
ser.write(testInput.encode())

try:
	while True:
		print("Reading...")
		d = ser.read(1000)
		print(str(d))
except KeyboardInterrupt:
	ser.close()
