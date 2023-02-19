import serial
import time

ser = serial.Serial('COM2',9600)

ser.timeout = 1

ser.write('hello world'.encode())
time.sleep(0.5)

ser.close()
