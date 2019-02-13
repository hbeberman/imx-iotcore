import serial
import sys
ser = serial.Serial('COM3', 115200)
while 1:
        line = ser.readline().decode('UTF-8')[0:-2]
        print(line)
        if line == "MFG:reqmac":
                ser.write(b'0xBADBAD00\n')