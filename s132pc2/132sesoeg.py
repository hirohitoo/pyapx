import nidaqmx
import time
import numpy as np
#from nidaqmx.constants import PFI4, 100khzTimebase 

from epics import caget,caput

def int_to_bool_list(num):
    return [bool(num & (1<<n)) for n in range(8)]

print("132ses.py")
print("SES:KineticEnergy","SES:Area")
actionlist=[]
openreqlist=[]
openenblist=[]
closereqlist=[]

while True:
	SESCalOnRQ=caget('SES:CalOn_RQ')
	SESCalOffRQ=caget('SES:CalOff_RQ')
	SESRunRQ=caget('SES:Run_RQ')
	SESStopRQ=caget('SES:Stop_RQ')  #1=force stop, #2=stop after sequence, #3=stop after scan
	SESKineticEnergy=caget('SES:KineticEnergy')
#	BL132PhotonEnergy=caget('BL132:PhotonEnergy')
	#BL132WaveLength
	#BL132Power
	#BL132PhotonFlux
	#APXFluence
	APXFootPrint=0.05*0.05

	with nidaqmx.Task() as task0:
		task0.ci_channels.add_ci_count_edges_chan("Dev5/ctr1")#,meas_time=1.0)#,name_to_assign_to_channel='PFI4')#,edge=Edge.RISING,initial_count=0,count_direction=CountDirection.COUINT_UP)
		task0.ci_channels[0].ci_count_edges_term="PFI4"
#		task0.ci_channels[0].ci_prescaler=8
		#task0.ci_channels[0].ci_count_edges_term="100kHzTimebase"
		task0.start()
		#task0.ci_channels.add_ci_count_edges_chan("Dev5/ctr1",name_to_assign_to_channel='/Dev5/PFI4',min_val=2.0, max_val=5000000,edge=Edge.RISING)
		#read_task.ci_channels.all.ci_count_edges_term = 'PFI4'
		data0=task0.read(5000)   
		SESArea=data0[0]#*1.08
		SESArea=np.sum(data0)/5000
		SESArea=np.mean(data0)*0.08
		caput("SES:Area",SESArea)
		print(SESKineticEnergy,SESArea,end='\r')

	time.sleep(0.2)
