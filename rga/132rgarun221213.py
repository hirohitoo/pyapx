import pyrga
import time
import datetime
import csv
from epics import caget,caput

if __name__ == "__main__":
# initialize client with non-default noise floor setting
	RGA = pyrga.RGAClient("COM1", noise_floor=4)
# check filament status and turn it on if necessary
	if caget("APX:Rga_State")==1:
		if not RGA.get_filament_status():
			RGA.turn_on_filament()
		if RGA.get_cdem_voltage()==0:
			RGA.set_cdem_voltage(980)	
	else:
		RGA.turn_off_filament()
		RGA.set_cdem_voltage(0)	
# read partial pressures of air constituent
	MASSES = {		
		18: "Rga0",
		28: "Rga1",
		32: "Rga2",
		44: "Rga3",
		0: "Rga4",
		0: "Rga5",
	}
#for m, i in MASSES.items():
	
	filename1 = '/com/Py/rga/m'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'
	headerstr=['#','Time','TimeStr','Rga0m','Rga0i','Rga1m','Rga1i','Rga2m','Rga2i','Rga3m','Rga3i','Rga4m','Rga4i','Rga5m','Rga5i']
	with open(filename1,"w",newline='') as f:
		writer =csv.writer(f)
		writer.writerow(headerstr)
		f.close()
#	for i in MASSES.items()[0]:
#		headerstr=headerstr+',mass'+str(i)+',ppress'+str(i)
		
	while True:
		pvs =[time.time(),datetime.datetime.now().strftime("%Y%m%d%H%M%S")]
		if caget("APX:Rga_State")==1:# and caget("APX:MZ_PV")=355.7:
			#pvs[]
			if not RGA.get_filament_status():
				RGA.turn_on_filament()
			if RGA.get_cdem_voltage()==0:
				RGA.set_cdem_voltage(980)

			j=0
			for m, i in MASSES.items():
				pvs.append(str(m))
				if m==0:
					pvs.append(str(0))
				else:
					pv=str(RGA.read_mass(m))
					caput("APX:Rga"+str(j),pv)				
					pvs.append(pv)
					j=j+1

			print(pvs)
        	#print("partial pressure of element {} is {} Torr".format(i, RGA.read_mass(m)))


		else: 
			print("Idling")
			if RGA.get_filament_status():
				RGA.turn_off_filament()
				RGA.set_cdem_voltage(0)	
			for m, i in MASSES.items():
				pvs.append(str(m))
				pvs.append(str(0))
			time.sleep(10)

			
		print(RGA.get_emission_current(),RGA.get_cdem_voltage())
		print(pvs)
		with open(filename1,"a",newline='') as f:
			writer =csv.writer(f)
			writer.writerow(pvs)
	f.close()





