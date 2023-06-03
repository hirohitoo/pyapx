import time
import datetime
import csv
from epics import caget

pvnames =["APX:HPC01","APX:HPC100","APX:Theater","BL132:Io","SPEC:mono132","SPEC:gap","SPEC:epu","BL132:Iz","BL132:Id","BL132:Is","BL132:m1yaw_2_LVDT","BL132:m2pit_2_LVDT",
          "BL132:132IG1","BL132:132WRG1","BL132:132WRG1_HIGH","BL132:132WRG1_LOW",
          "SPEC:sgmensz","SPEC:m0top","SPEC:m0bot","SPEC:m0spr","SPEC:m0srl",
          "SPEC:m0pit","SPEC:m0tran","SPEC:m1pit","SPEC:m1vert",
          "SPEC:sgmensw","SPEC:sgmpit","SPEC:sgmhorz","SPEC:exsv_2","SPEC:exsh_2",
          "SPEC:m1yaw_2","SPEC:m1hor_2","SPEC:m2pit_2","SPEC:m2ver_2",
          "APX:AP1","APX:AP2","APX:HPC",
          "APX:V0_SCL","APX:V0_SOP","APX:V1_SCL","APX:V1_SOP","APX:V2_SCL","APX:V2_SOP","APX:V3_SCL","APX:V3_SOP",
          "APX:V4_SCL","APX:V4_SOP","APX:V5_SCL","APX:V5_SOP","APX:V6_SCL","APX:V6_SOP","APX:V7_SCL","APX:V7_SOP",
          "APX:MZ_PV",
          "APX:PiezoX","APX:PiezoY","APX:PiezoZ",
          "APX:AXIS0_ZSRL","APX:AXIS1_INSRL","APX:AXIS2_TRAN","APX:AXIS3_SPRSRL","APX:AXIS4_INSPR","APX:AXIS5_SPRSRL","APX:PREP"]

pvnames0 =["Time","TimeStr"]
pvnames0=pvnames0+pvnames
print('132pylog')
print(pvnames0)
filename1 = '/com/Py/data/'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'
with open(filename1,"a",newline='') as f:
     header=pvnames0+pvnames
     writer=csv.writer(f)
     print(header,end='\r')
     writer.writerow(header)
     f.close()

while True:
#    try:

        pvs =[datetime.datetime.now(),datetime.datetime.now().strftime("%Y%m%d%H%M%S")]
        
        for val in pvnames:
            pvs.append(caget(val))

        with open(filename1,"a",newline='') as f:
            writer =csv.writer(f)#,delimiter=",")
            #writer.writeheader(pvnames0)
            print(pvs,end='\r')
            writer.writerow(pvs)
        time.sleep(30)
#print(pvs)   
#	print("Keyboard Interrupt")

#    except:
#        print("Keyboard Interrupt")
#        break
#with open(filename1,"a") as f:
#writer = csv.writer(f,delimiter=",")
#writer.writerow([time.time(),decoded_bytes])
