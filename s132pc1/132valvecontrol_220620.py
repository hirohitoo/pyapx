import nidaqmx
import time
import numpy

from epics import caget,caput

def int_to_bool_list(num):
    return [bool(num & (1<<n)) for n in range(8)]

print("132valvecontrol.py")
print("IV0 IV1 IV2 IV3 IV4 IV5 IV6 IV7 RQ")
print("C O C O C O C O C O C O C O C O")
actionlist=[]
openreqlist=[]
openenblist=[]
closereqlist=[]

while True:
	try:
		sum=int(numpy.logical_not(bool(int(caget("APX:V0_OPEN_ACT")))))+int(numpy.logical_not(bool(int(caget("APX:V1_OPEN_ACT")))))*2
		sum=sum+int(numpy.logical_not(bool(int(caget("APX:V2_OPEN_ACT")))))*4+int(numpy.logical_not(bool(int(caget("APX:V3_OPEN_ACT")))))*8
		sum=sum+int(numpy.logical_not(bool(int(caget("APX:V4_OPEN_ACT")))))*16+int(numpy.logical_not(bool(int(caget("APX:V5_OPEN_ACT")))))*32
		sum=sum+int(numpy.logical_not(bool(int(caget("APX:V6_OPEN_ACT")))))*64+int(numpy.logical_not(bool(int(caget("APX:V7_OPEN_ACT")))))*128
	except:
		time.sleep(0.1)
	#print("132valvecontrol1","ACT",sum)
	#print(''.join(str(openreqlist)))
	#print(''.join(str(openenblist)))
	#print(''.join(str(closereqlist)))

	with nidaqmx.Task() as task0:
		task0.di_channels.add_di_chan("Dev4/port1/line0:7") 
		data0=task0.read(number_of_samples_per_channel=1)   
		try:
			caput("APX:V0_SCL",int(numpy.logical_not(int_to_bool_list(data0[0]))[0]))
			caput("APX:V1_SCL",int(numpy.logical_not(int_to_bool_list(data0[0]))[1]))
			caput("APX:V2_SCL",int(numpy.logical_not(int_to_bool_list(data0[0]))[2]))
			caput("APX:V3_SCL",int(numpy.logical_not(int_to_bool_list(data0[0]))[3]))
			caput("APX:V4_SCL",int(numpy.logical_not(int_to_bool_list(data0[0]))[4]))
			caput("APX:V5_SCL",int(numpy.logical_not(int_to_bool_list(data0[0]))[5]))
			caput("APX:V6_SCL",int(numpy.logical_not(int_to_bool_list(data0[0]))[6]))
			caput("APX:V7_SCL",int(numpy.logical_not(int_to_bool_list(data0[0]))[7]))
		except:
			time.sleep(0.1)
	with nidaqmx.Task() as task1:
		task1.di_channels.add_di_chan("Dev4/port0/line0:7") 
		data1=task1.read(number_of_samples_per_channel=1)
		try:
			caput("APX:V0_SOP",int(numpy.logical_not(int_to_bool_list(data1[0]))[0]))
			caput("APX:V1_SOP",int(numpy.logical_not(int_to_bool_list(data1[0]))[1]))
			caput("APX:V2_SOP",int(numpy.logical_not(int_to_bool_list(data1[0]))[2]))
			caput("APX:V3_SOP",int(numpy.logical_not(int_to_bool_list(data1[0]))[3]))
			caput("APX:V4_SOP",int(numpy.logical_not(int_to_bool_list(data1[0]))[4]))
			caput("APX:V5_SOP",int(numpy.logical_not(int_to_bool_list(data1[0]))[5]))
			caput("APX:V6_SOP",int(numpy.logical_not(int_to_bool_list(data1[0]))[6]))
			caput("APX:V7_SOP",int(numpy.logical_not(int_to_bool_list(data1[0]))[7]))
		except:
			time.sleep(0.1)
#	print("SCL",int(numpy.logical_not(int_to_bool_list(data0[0]))[0]),int(numpy.logical_not(int_to_bool_list(data0[0]))[1]),int(numpy.logical_not(int_to_bool_list(data0[0]))[2]),int(numpy.logical_not(int_to_bool_list(data0[0]))[3]),int(numpy.logical_not(int_to_bool_list(data0[0]))[4]),int(numpy.logical_not(int_to_bool_list(data0[0]))[5]),int(numpy.logical_not(int_to_bool_list(data0[0]))[6]),int(numpy.logical_not(int_to_bool_list(data0[0]))[7]))
#	print("SOP",int(numpy.logical_not(int_to_bool_list(data1[0]))[0]),int(numpy.logical_not(int_to_bool_list(data1[0]))[1]),int(numpy.logical_not(int_to_bool_list(data1[0]))[2]),int(numpy.logical_not(int_to_bool_list(data1[0]))[3]),int(numpy.logical_not(int_to_bool_list(data1[0]))[4]),int(numpy.logical_not(int_to_bool_list(data1[0]))[5]),int(numpy.logical_not(int_to_bool_list(data1[0]))[6]),int(numpy.logical_not(int_to_bool_list(data1[0]))[7]))
	print(int(numpy.logical_not(int_to_bool_list(data0[0]))[0]),int(numpy.logical_not(int_to_bool_list(data1[0]))[0]),
              int(numpy.logical_not(int_to_bool_list(data0[0]))[1]),int(numpy.logical_not(int_to_bool_list(data1[0]))[1]),
              int(numpy.logical_not(int_to_bool_list(data0[0]))[2]),int(numpy.logical_not(int_to_bool_list(data1[0]))[2]),
              int(numpy.logical_not(int_to_bool_list(data0[0]))[3]),int(numpy.logical_not(int_to_bool_list(data1[0]))[3]),
              int(numpy.logical_not(int_to_bool_list(data0[0]))[4]),int(numpy.logical_not(int_to_bool_list(data1[0]))[4]),
              int(numpy.logical_not(int_to_bool_list(data0[0]))[5]),int(numpy.logical_not(int_to_bool_list(data1[0]))[5]),
              int(numpy.logical_not(int_to_bool_list(data0[0]))[6]),int(numpy.logical_not(int_to_bool_list(data1[0]))[6]),
              int(numpy.logical_not(int_to_bool_list(data0[0]))[7]),int(numpy.logical_not(int_to_bool_list(data1[0]))[7]),sum,end='\r')

	with nidaqmx.Task() as task2:
		task2.do_channels.add_do_chan("Dev4/port2/line0:7")
		data2=task2.write(sum)

	time.sleep(2)
