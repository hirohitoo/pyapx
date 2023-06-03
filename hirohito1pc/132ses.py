import nidaqmx
import time
import numpy

from epics import caget,caput

def int_to_bool_list(num):
    return [bool(num & (1<<n)) for n in range(8)]

print("132ses.py")
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
	BL132PhotonEnergy=caget('BL132:PhotonEnergy')
	#BL132WaveLength
	#BL132Power
	#BL132PhotonFlux
	#APXFluence
	APXFootPrint=0.05*0.05

	with nidaqmx.Task() as task0:
		task0.di_channels.add_ci_freq_chan("Dev5/ctr1",name_to_assign_to_channel='/Dev5/PFI4',min_freq=2.0, max_freq=5000000,edge=Edge.RISING)
		#read_task.ci_channels.all.ci_count_edges_term = '/Dev5/PFI4'
		data0=task0.read(number_of_samples_per_channel=1)   
		SESArea=data0[0]*1.08
		caput("SES:Area",SESArea)
	print("SES:Area",SESArea,'SES:KineticEnergy',SESKineticEnergy)

	time.sleep(0.2)
