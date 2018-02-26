import serial
import RPi.GPIO as GPIO
import time

ser = serial.Serial("/dev/ttyAMA0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600


while True:
    print("Reading serial line...")
    read_ser = ser.readline()
    print (read_ser)
