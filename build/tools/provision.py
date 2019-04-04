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
        #print("checksum: " + str(sum))
        ser.write(struct.pack('I', sum))

def sendstring( string ):
        print("string length: " + str(len(string)))
        ser.write(struct.pack('I', len(string)))
        ser.write(string)
        sum = 0
        for i in range(len(string)):
            sum = sum + string[i]
        #print("checksum: " + str(sum))
        ser.write(struct.pack('I', sum))

def fatalerror( errormsg ):
    print(errormsg)
    print("REBOOTING SYSTEM")
    print("REBOOTING SYSTEM")
    print("REBOOTING SYSTEM")
    print("REBOOTING SYSTEM")


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
    if line == "MFG:smbiosserialreq":
        print("MFG:smbiosserialreq recieved\n")
        sendstring(b'RealSerialNumber123456789\n')
    if line == "MFG:ekcert":
        print("MFG:ekcert recieved\n")
        data = ser.read(4)
        length = data[0] + (data[1] << 8) + (data[2] << 16) + (data[3] << 24)
        ekbytes = ser.read(length)
        data = ser.read(4)
        devicesum = data[0] + (data[1] << 8) + (data[2] << 16) + (data[3] << 24)
        hostsum = 0
        for i in ekbytes:
            hostsum = hostsum + i
        if hostsum != devicesum:
            fatalerror("Invalid EK certificate recieved!")
            continue
        # ekcert should be passed through limpet to confirm an actual length
        # the properties of the ftpm may change the number from 652.
        ekbase64 = codecs.encode(ekbytes, 'base64').decode()
        print("fTPM Endorsement Key Certificate:")
        print(ekbase64)
        with open("c:\\temp\\mfgek.txt", "a") as ekfile:
            ekfile.write(ekbase64)
        continue
    if line == "MFG:ekcertfail":
        fatalerror("Failed to retrieve EK certificate!")
    if line == "MFG:devicecertfail":
        fatalerror("Failed to store device certificate!")
    if line == "MFG:smbiosfail":
        fatalerror("Failed to store smbios values!")
    print(line)