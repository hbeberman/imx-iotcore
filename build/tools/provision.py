#pip install pySerial
import serial
import sys
import codecs
import os
import struct

ser = serial.Serial('COM4', 115200)
ekcertmode = False
ekcert = ""

while 1:
    try:
        line = ser.readline().decode('UTF-8')[0:-2]
    except:
        print("exception during decode")
        continue
    if line == "MFG:reqmac":
        # Write MAC0
        ser.write(b'0xBADBAD00\n')
        # Write MAC1
        ser.write(b'0xDEADBEEF\n')
    if line == "MFG:devicecert":
        print("MFG:devicecert recieved\n")
        with open("c:\\temp\\cert.cer", "rb") as devicecert:
            buf = devicecert.read()
            print("devicecertsize: " + str(len(buf)))
            ser.write(struct.pack('I', len(buf)))
            ser.write(buf)
            sum = 0
            for i in range(len(buf)):
                sum = sum + buf[i]
            print("checksum: " + str(sum))
        continue
    if line == "MFG:ekcertend":
        ekcertmode = False
        print("ekcert capture finished")
        #print(ekcert)
        # ekcert should be passed through limpet to confirm an actual length
        # the properties of the ftpm may change the number from 652.
        ekbase64 = codecs.encode(codecs.decode(ekcert[0:652], 'hex'), 'base64').decode()
        print(ekbase64)
        with open("c:\\temp\\mfgek.txt", "a") as ekfile:
            ekfile.write(ekbase64)
        continue
    if line == "MFG:ekcertstart":
        ekcertmode = True
        ekcert = ""
        print("ekcert capture started")
        continue
    if ekcertmode == True:
        ekcert += line
        continue
    print(line)