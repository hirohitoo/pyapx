#132wrg1.py
#Read set point value at the start
#Read pressure every ~1 sec

import serial, string
from time import sleep
import os
from epics import caput
#ser.close()
ser = serial.Serial('COM10', timeout=2, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0)
    
ser.write("p\n".encode())
sleep(0.2)
out = ''
out = ser.read(ser.inWaiting())
#ser.write(b'\x05')
sleep(0.3)
#out = ''
#out = ser.read(ser.inWaiting())
print("132tn908a.py")
#print("APX:GAS",out.decode().rstrip().split(' ')[0])
#print("BL132:132WRG1SPH",out.decode().rstrip().split(',')[1])
#print("BL132:WRG1SPL",out.decode().split(',')[])
sleep(0.1)
ser.close()
#print("BL132:132WRG1")
while True:
    ser = serial.Serial('COM10', timeout=2, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0)
    ser.write('p\n'.encode())
    sleep(0.3)
    out = ''
    out = ser.read(ser.inWaiting())
#    ser.write(b'\x05')
    sleep(0.3)
#    out = ''
#    out = ser.read(ser.inWaiting())
#    print("BL132:132WRG1STS",out.decode().rstrip().split(',')[0])
    try:
        APX_GAS=out.decode().rstrip().split()[0]
    except:
        APX_GAS='9999'
#    APX_GAS1=out.decode().rstrip().split('')[1]
    cmd='caput APX:GAS '+str(APX_GAS)
    print("APX:GAS ",APX_GAS,end='\r')
#    print(cmd)
#    os.system(cmd)
    try:
        caput('APX:GAS',APX_GAS)
    except:
        caput('APX:GAS','9999')
#    caput('BL132:132WRG1',BL132_132WRG1)
    ser.close()
    sleep(2)
