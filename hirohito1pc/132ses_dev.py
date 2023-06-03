#import pprint
import nidaqmx
import statistics
import time

from epics import caput

#print(caget("BL132:Iz"))  
#print(caget("BL132:Io"))
#print(caget("BL132:Id"))
#print(caget("BL132:Is"))
#print(caget("BL132:m1yaw_2_LVDT"))
#print(caget("BL132:m2pit_2_LVDT"))
print("132voltmeter1.py")
print("BL132:Iz","BL132:Io","BL132:Is")

while True:
#    with nidaqmx.Task() as task0:
#        task0.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE) 
#        data0=task0.read(number_of_samples_per_channel=256)   
    try:
    	hwnd = win32gui.FindWindow('Voltage', None)
    except:
	#NO windows
    else:
        #There is WINDOW
    finally:
	#CAPUT here

    time.sleep(0.2)
#    print('1 Channel 1 Sample Read Raw: ')
    

    
    
#    data = task.read_raw()

#    pp.pprint(data)
        #print("BL132:Iz",statistics.mean(data0)," ","BL132:Io",statistics.mean(data1),end='\r')
#    BL132_Ses=statistics.mean(data1)


#    print("{:8.3f}".format(BL132_Iz),"{:8.3f}".format(BL132_Io),"{:8.3f}".format(BL132_Is),end='\r')    
        #print("BL132:Id",statistics.mean(data2))
        #print("BL132:Is",statistics.mean(data3))
        #print("BL132:m1yaw_2_LVDT",statistics.mean(data4))
        #print("BL132:m2pit_2_LVDT",statistics.mean(data5))
        #print("AI6",statistics.mean(data6))
        #print("AI7",statistics.mean(data7))
    
#    caput("BL132:Iz",statistics.mean(data0))    
#    caput("BL132:Io",statistics.mean(data1))
#    caput("BL132:Id",statistics.mean(data2))
#    caput("BL132:Is",statistics.mean(data3))
#    caput("BL132:m1yaw_2_LVDT",statistics.mean(data4))
#    caput("BL132:m2pit_2_LVDT",statistics.mean(data5))