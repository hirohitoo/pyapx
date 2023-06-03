#import pyrga
#import time
import serial, string
from time import sleep
import os
from epics import caput
#ser.close()
while True:
	ser = serial.Serial('COM9', timeout=2, baudrate=19200, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0)
	ser.write('#01RD\r'.encode())
	sleep(0.3)
	out = ''
	out = ser.read(ser.inWaiting())
	sleep(0.3)
	#print(out)
	try:
		APX_PIR=out.decode().rstrip().split(' ')[1]
	except:
		APX_PIR='9999'	
	print("APX:PIR ",APX_PIR,end='\r')
#	try:
#        caput('APX:GAS',APX_GAS)
#	except:
#        caput('APX:GAS','9999')
	ser.close()
	sleep(2)

					





