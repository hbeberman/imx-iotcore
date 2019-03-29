#pip install pySerial
import serial
import sys
import codecs
import os
import struct

ser = serial.Serial('COM4', 115200)
ekcertmode = False
ekcert = ""

def sendfile( filepath ):
    with open(filepath, "rb") as f:
        buf = f.read()
        print("file size: " + str(len(buf)))
        ser.write(struct.pack('I', len(buf)))
        ser.write(buf)
        sum = 0
        for i in range(len(buf)):
            sum = sum + buf[i]
        print("checksum: " + str(sum))

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
        sendfile("c:\\temp\\cert.cer")
    if line == "MFG:smbios":
        print("MFG:smbios recieved\n")
        sendfile("c:\\temp\\myboard.smbios")
    if line == "MFG:ekcertstart":
        ekcert = ""
        print("ekcert capture started")
        while 1:
            line = ser.readline().decode('UTF-8')[0:-2]
            if line == "MFG:ekcertend":
                break
            ekcert += line
        print("ekcert capture finished")
        # ekcert should be passed through limpet to confirm an actual length
        # the properties of the ftpm may change the number from 652.
        ekbase64 = codecs.encode(codecs.decode(ekcert[0:652], 'hex'), 'base64').decode()
        print(ekbase64)
        with open("c:\\temp\\mfgek.txt", "a") as ekfile:
            ekfile.write(ekbase64)
        continue
    print(line)