#132turbo.py
#Read set point value at the start
#Read turbo settings every ~1 sec

# pip install crccheck

import serial, string
from time import sleep

from epics import caput, caget
from crccheck.checksum import ChecksumXor8
#ser.close()
#ser = serial.Serial('COM24', timeout=2, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0)

CMD_START="\x48\x48\x48\x49\x49"#"00011"
CMD_STOP="\x48\x48\x48\x49\x48"#"00010"
CMD_PUMPPOWER="\x50\x48\x50\x48"#"2020"
CMD_PUMPSTATS="\x50\x48\x53\x48"#"2050"
CMD_DRIVEFREQ="\x50\x48\x51\x48"#"2030"
CMD_STARTSTOP="\x48\x48\x48\x48\x49"#"00001"
CMD_REMOTESERIAL="\x48\x48\x56\x48\x49"#"00801"
CMD_REMOTE="\x48\x48\x56\x49\x49"#"00811"
CMD_REMOTE="\x48\x48\x56\x49\x40"#"00810"
CMD_PRESSURE="\x48\x48\x56\x48\x40"#"00810"


CMD_START="\x30"+"\x30"+"\x30"+"\x31"+"\x31" #00011
CMD_STOP="\x30"+"\x30"+"\x30"+"\x31"+"\x30" #00010
CMD_PUMPPOWER="\x32"+"\x30"+"\x32"+"\x30" #2020
CMD_PUMPSTATS="\x32"+"\x30"+"\x35"+"\x30" #2050
CMD_DRIVEFREQ="\x32\x30\x33\x30"#"2030"
CMD_STARTSTOP="\x30\x30\x30\x30\x31"#"00001"
CMD_REMOTESERIAL="\x30\x30\x38\x30\x31"#"00801"
CMD_REMOTE="\x30\x30\x38\x31\x31"#"00811"
CMD_REMOTE="\x30\x30\x38\x31\x30"#"00810"
CMD_PRESSURE="\x30\x30\x38\x31\x30"#"00810"

flgAP1Turbo = False
flgAP2Turbo = False
flgL2Turbo = False
flgPREPTurbo = False
flgGASTurbo = False
flgBPTurbo = False
flgHPCTurbo = True
flgHEMTurbo = False

print("APX Turbo pumps")
while True:


	if flgAP1Turbo == True:

		if caget('APX:AP1Turbo_STOP')==1:
			CMD=CMD_STOP
			caput('APX:AP1Turbo_STOP',0)
		elif caget('APX:AP1Turbo_START')==1:
			CMD=CMD_START
			caput('APX:AP1Turbo_START',0)
		else:
			CMD=CMD_PUMPSTATS
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		CMD="\x02"+CMD+chr(checksum)
		serAP1Turbo.write(CMD.encode())
		sleep(0.2)
		out = ''
		out = serAP1Turbo.read(serAP1Turbo.inWaiting())
		print(out[4:-2].decode())
		serAP1Turbo.close()
	
	if flgAP2Turbo == True:
		serAP2Turbo = serial.Serial('COM6', timeout=2, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0)    
		CMD="\x80"+CMD_PUMPSTATS+"\x03"
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		CMD="\x02"+CMD+chr(checksum)
		serAP2Turbo.write(CMD.encode())
		sleep(0.2)
		out = ''
		out = serAP2Turbo.read(serAP2Turbo.inWaiting())
		print(out)

		if caget('APX:AP2Turbo_STOP')==1:
			CMD=CMD_STOP
			caput('APX:AP2Turbo_STOP',0)
		elif caget('APX:AP2Turbo_START')==1:
			CMD=CMD_START
			caput('APX:AP2Turbo_START',0)
		else:
			CMD=CMD_PUMPPOWER
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		CMD="\x02"+CMD+chr(checksum)
		serAP2Turbo.write(CMD.encode())
		sleep(0.2)
		out = ''
		out = serAP2Turbo.read(serAP2Turbo.inWaiting())
		print(out)
		serAP2Turbo.close()

	if flgL2Turbo == True:
		serL2Turbo = serial.Serial('COM4', timeout=2, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0)    
		CMD="\x80"+CMD_PUMPSTATS+"\x03"
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		CMD="\x02"+CMD+chr(checksum)
		serL2Turbo.write(CMD.encode())
		sleep(0.2)
		out = ''
		out = serL2Turbo.read(serL2Turbo.inWaiting())
		print(out[4:-2].decode())
		if caget('APX:L2Turbo_STOP')==1:
			CMD=CMD_STOP
			caput('APX:L2Turbo_STOP',0)
		elif caget('APX:L2Turbo_START')==1:
			CMD=CMD_START
			caput('APX:L2Turbo_START',0)
		else:
			CMD=CMD_PUMPPOWER
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		CMD="\x02"+CMD+chr(checksum)
		serL2Turbo.write(CMD.encode())
		sleep(0.2)
		out = ''
		out = serL2Turbo.read(serL2Turbo.inWaiting())
		print(out[4:-2].decode())
		serL2Turbo.close()

	if flgHEMTurbo == True:
		serHEMTurbo = serial.Serial('COM5', timeout=2, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0)    
		CMD="\x80"+CMD_PUMPSTATS+"\x03"
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		CMD="\x02"+CMD+chr(checksum)
		serHEMTurbo.write(CMD.encode())
		sleep(0.2)
		out = ''
		out = serHEMTurbo.read(serHEMTurbo.inWaiting())
		print(out[6:11].decode())

		if caget('APX:HEMTurbo_STOP')==1:
			CMD=CMD_STOP
			caput('APX:L2Turbo_STOP',0)
		elif caget('APX:HEMTurbo_START')==1:
			CMD=CMD_START
			caput('APX:HEMTurbo_START',0)
		else:
			CMD=CMD_PUMPPOWER
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		CMD="\x02"+CMD+chr(checksum)
		serHEMTurbo.write(CMD.encode())
		sleep(0.2)
		out = ''
		out = serHEMTurbo.read(serHEMTurbo.inWaiting())
		print(out[6:11].decode())
		serHEMTurbo.close()

	if flgPREPTurbo == True:
		if caget('APX:PREPTurbo_STOP')==1:
			CMD=CMD_STOP
			caput('APX:PREPTurbo_STOP',0)
		elif caget('APX:PREPTurbo_START')==1:
			CMD=CMD_START
			caput('APX:PREPTurbo_START',0)
		else:
			CMD=CMD_PUMPPOWER
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		CMD="\x02"+CMD+chr(checksum)
		serPREPTurbo.write(CMD.encode())
		sleep(0.2)
		out = ''
		out = serPREPTurbo.read(serPREPTurbo.inWaiting())
		print(out[4:-2].decode())
		serPREPTurbo.close()

	if flgGASTurbo == True:
		serGASTurbo = serial.Serial('COM26', timeout=2, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0)    
		CMD="\x80"+CMD_PUMPSTATS+"\x03"
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		CMD="\x02"+CMD+chr(checksum)
		serGASTurbo.write(CMD.encode())
		sleep(0.2)
		out = ''
		out = serGASTurbo.read(serGASTurbo.inWaiting())
		print('PUMPSTATS',out[4:-2].decode())


		if caget('APX:GASTurbo_STOP')==1:
			CMD="\x80"+CMD_STOP+"\x03"
			caput('APX:GASTurbo_STOP',0)
		elif caget('APX:GASTurbo_START')==1:
			CMD="\x80"+CMD_START+"\x03"
			caput('APX:GASPTurbo_START',0)
		else:
			CMD="\x80"+CMD_PUMPPOWER+"\x03"
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		CMD="\x02"+CMD+chr(checksum)
		serGASTurbo.write(CMD.encode())
		sleep(0.2)
		out = ''
		out = serGASTurbo.read(serGASTurbo.inWaiting())
		print(out[4:-2].decode())
		serGASTurbo.close()

	if flgBPTurbo == True:
		if caget('APX:BPTurbo_STOP')==1:
			CMD=CMD_STOP
			caput('APX:BPTurbo_STOP',0)
		elif caget('APX:BPTurbo_START')==1:
			CMD=CMD_START
			caput('APX:BPTurbo_START',0)
		else:
			CMD=CMD_PUMPPOWER
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		CMD="\x02"+CMD+chr(checksum)
		serBPTurbo.write(CMD.encode())
		sleep(0.2)
		out = ''
		out = serBPTurbo.read(serBPTurbo.inWaiting())
		print(out[4:-2].decode())
		serBPTurbo.close()

	if flgHPCTurbo == True:
		serHPCTurbo = serial.Serial('COM25', timeout=2, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0)    
		CMD="\x80"+CMD_PUMPSTATS+"\x03"
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		print("checksum1",checksum)
		print(checksum.to_bytes(1,'big'))
		CMD="\x02"+CMD+chr(checksum)
		print("CMD1",CMD)
		print("CMD1",CMD.encode('latin-1'))
		serHPCTurbo.write(CMD.encode('latin-1'))
		sleep(0.2)
		out = ''
		out = serHPCTurbo.read(serHPCTurbo.inWaiting())
		print("HPC PUMPSTATS",out[2:3])
		
		if caget('APX:HPCTurbo_STOP')==1:
			CMD="\x80"+CMD_STOP+"\x03"
			print(CMD)
			caput('APX:HPCTurbo_STOP',0)
		elif caget('APX:HPCTurbo_START')==1:
			CMD="\x80"+CMD_START+"\x03"
			print(CMD)
			caput('APX:HPCTurbo_START',0)
		else:
			CMD="\x80"+CMD_PUMPPOWER+"\x03"
		#CMD="\x80"+CMD+"\x03"
		data=bytearray()
		data.extend(map(ord,CMD))
		checksum = ChecksumXor8.calc(data)
		print("checksum2",checksum)
		print(checksum.to_bytes(1,'big'))
		CMD="\x02"+CMD+chr(checksum) #"\x03"
		print("CMD2",CMD)
		print("CMD2",CMD.encode('latin-1'))
		serHPCTurbo.write(CMD.encode('latin-1'))
		sleep(0.2)
		out = ''
		out = serHPCTurbo.read(serHPCTurbo.inWaiting())
		print("HPC PUMPPOWER",out)
		serHPCTurbo.close()
	sleep(1)
