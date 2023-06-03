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
print("132voltmeter2.py")
print("BL132:Io","BL132:Is")

while True:
    with nidaqmx.Task() as task20:
        try:
              task21.ai_channels.add_ai_voltage_chan("Dev1/ai16",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE) 
              data0=task20.read(number_of_samples_per_channel=1000)   
        except:
              data0=[9.999,9.999]
    with nidaqmx.Task() as task21:
        try:
              task21.ai_channels.add_ai_voltage_chan("Dev1/ai17",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
              data1=task21.read(number_of_samples_per_channel=1000)
        except:
              data1=[9.999,9.999] 
#    with nidaqmx.Task() as task2:
#        try:
#              task2.ai_channels.add_ai_voltage_chan("Dev1/ai18",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
#              data2=task2.read(number_of_samples_per_channel=5000)
#        except:
#              data2=[9.999,9.999] 
    
#    with nidaqmx.Task() as task3:
#        task3.ai_channels.add_ai_voltage_chan("Dev1/ai3",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
#        data3=task3.read(number_of_samples_per_channel=256)
    
#    with nidaqmx.Task() as task4:
#        task4.ai_channels.add_ai_voltage_chan("Dev1/ai4",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
#        data4=task4.read(number_of_samples_per_channel=256)
    
#    with nidaqmx.Task() as task5:
#        task5.ai_channels.add_ai_voltage_chan("Dev1/ai5",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
#        data5=task5.read(number_of_samples_per_channel=256)
    
#    with nidaqmx.Task() as task6:
#        task6.ai_channels.add_ai_voltage_chan("Dev1/ai6",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
#        data6=task6.read(number_of_samples_per_channel=256)
    
#    with nidaqmx.Task() as task7:
#        task7.ai_channels.add_ai_voltage_chan("Dev1/ai7",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
#        data7=task7.read(number_of_samples_per_channel=256)
    
    time.sleep(0.2)
#    print('1 Channel 1 Sample Read Raw: ')
    

    
    
#    data = task.read_raw()

#    pp.pprint(data)
        #print("BL132:Iz",statistics.mean(data0)," ","BL132:Io",statistics.mean(data1),end='\r')
    BL132_Io=statistics.mean(data0)
#    BL132_Iz=statistics.mean(data1)
    BL132_Is=statistics.mean(data1)
    print("{:8.3f}".format(BL132_Io),"{:8.3f}".format(BL132_Is),end='\r')
#    print("{:8.3f}".format(BL132_Io),"{:8.3f}".format(BL132_Io),"{:8.3f}".format(BL132_Is),end='\r')    
        #print("BL132:Id",statistics.mean(data2))
        #print("BL132:Is",statistics.mean(data3))
        #print("BL132:m1yaw_2_LVDT",statistics.mean(data4))
        #print("BL132:m2pit_2_LVDT",statistics.mean(data5))
        #print("AI6",statistics.mean(data6))
        #print("AI7",statistics.mean(data7))
    
#    caput("BL132:Iz",statistics.mean(data0))    
    caput("BL132:Io",statistics.mean(data0))
#    caput("BL132:Id",statistics.mean(data2))
#    caput("BL132:Is",statistics.mean(data3))
#    caput("BL132:m1yaw_2_LVDT",statistics.mean(data4))
#    caput("BL132:m2pit_2_LVDT",statistics.mean(data5))
