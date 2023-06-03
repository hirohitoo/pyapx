import sys
import re
import time
import shutil
import numpy as np
from collections import Counter
from io import StringIO
from datetime import datetime



#Data type
#SES Detector --> SES
#SES Signal --> SESsignal0, SESsignal1
#Description
#SIG Signal
#TAG
#SUM or SNG
#XA1 
#XA2
#n1c4 --> ZOB
#n2c1 --> Io
#n2c2 --> Ises
#n2c3 --> Idc
#Signal --> [ZOB, I0, Ises, Idc]
#Yeild --> [Auger, Total]


# Specify dataset
#print('Sample name:',''.join(sys.argv[1:2])) #Sample name
#print('Date from:',' '.join(sys.argv[2:4])) #Date from
#print(('Date to:',' '.join(sys.argv[4:6])) #Date to
#Argv_Sample=''.join(sys.argv[1:2])
#Argv_DateTime_from=' '.join(sys.argv[2:4])
#Argv_DateTime_to=' '.join(sys.argv[4:6])
#XPS_Sample=Argv_Sample
#XPS_DateTime_from=Argv_DateTime_from
#XPS_DateTime_to=Argv_DateTime_to

DirSeparator='//'
XPS_datafolder='P://b_ogasawara//bl13-0//bl13-2//dt_SES100//'
XPS_ExperimentNumer='2022//BL132'
XPS_exportflder='T://data//'
XPS_Sample='export'
DateTime_from='2022-12-10 00:00:00' #Use YYYY-MM-DD hh:mm:ss"
DateTime_to='2022-12-30 23:00:00'
XPS_DateTime_from='2022-12-01 00:00:00'
XPS_DateTime_to='2022-12-30 23:00:00'

XAS_Sample=XPS_Sample
XAS_DateTime_from=XPS_DateTime_from #'2022-05-27 00:00:00'
XAS_DateTime_to=XPS_DateTime_to #'2022-05-28 23:00:00'
#XAS_X
#XAS_Io
#XAS_Ix
#XAS_Is
XAS_datafolder='P://b_ogasawara//bl13-0//bl13-2//dt_SPEC//'
SPECDAT_FILE='P://b_ogasawara//bl13-0//bl13-2//dt_SPEC//specdata2022f1b.dat'
XAS_ExperimentNumer='specdata2022f1b'
XAS_FileNumber_from='3000'
XAS_FileNumber_to='3500'
XAS_prefix=''


XPS_prefix=XPS_datafolder+XPS_ExperimentNumer
print('XAS folder',XPS_prefix)
XAS_prefix=XAS_datafolder
print('XAS folder',XAS_prefix)

Plt_Flag=False

#FILES_XPS=XPS_FILES
#print(FILES_XPS)
#XPS_Sample='Sample'
#XPS_Sample='Sample'

#List xps files in DIR_NAME and filter using Datetime_from and Datetime_to
import pandas as pd
import os
import glob
DIR_NAME=XPS_prefix
FILES = glob.glob(os.path.join(DIR_NAME, '*.txt'))
columns=['Name']
EDF=pd.DataFrame(FILES,columns=columns)
print(len(FILES),'XPS files were found on the server.')
x=[]
x1=[]
x2=[]
for FILE_NAME in FILES:
  filename_w_ext = os.path.basename(FILE_NAME)
  filename, file_extension = os.path.splitext(filename_w_ext)
  x.append(pd.Timestamp(filename[-14:-10]+'-'+filename[-10:-8]+'-'+filename[-8:-6]+' '+filename[-6:-4]+':'+filename[-4:-2]+':'+filename[-2:]))
  x1.append('xps')
  x2.append
EDF['Timestr']=x
EDF['Type']=x1
EDF['Time']=datatime.strptime(x,"%Y-%m-%d %H:%M:%S")
EDF = EDF.set_index(EDF['Time'])
#print((EDF['Timestamp']))
#EDF.set_index('Timestamp')
DateTime_from_num=datetime.strptime(DateTime_from,"%Y-%m-%d %H:%M:%S").timestamp()
DateTime_to_num=datetime.strptime(DateTime_to,"%Y-%m-%d %H:%M:%S").timestamp()
FILES=EDF.Name.loc[DateTime_from_num:DateTime_to_num].tolist()
print (DIR_NAME)
print(len(FILES),XPS_Sample,'files were donwloaded.')
#print (EDF)


#List xas files in DIR_NAME and filter using Datetime_from and Datetime_to
import pandas as pd
import os
import glob
DIR_NAME=XAS_prefix
XASFILES = glob.glob(os.path.join(DIR_NAME, '*.csv'))
#columns=['Name']
#EDF=pd.DataFrame(XASFILES,columns=columns)
print(len(XASFILES),'XAS files were found on the server.')
x=[]
x1=[]
x2=[]
x3=[]
x4=[]
namelst=[]
for FILE_NAME in XASFILES:
  filename_w_ext = os.path.basename(FILE_NAME)
  file_mtime = os.path.getmtime(FILE_NAME)
  filename, file_extension = os.path.splitext(filename_w_ext)
#  x.append((time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(time.ctime(file_mtime)))))
#  x.append(pd.Timestamp(filename[-14:-10]+'-'+filename[-10:-8]+'-'+filename[-8:-6]+' '+filename[-6:-4]+':'+filename[-4:-2]+':'+filename[-2:]))
  x1.append('xas')
  #file_tobj=time.strptime(file_mtime)
  #print(time.ctime(file_mtime))
  T_stamp=time.strftime("%Y%m%d%H%M%S",time.strptime(time.ctime(file_mtime)))
#  x.append(time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(time.ctime(file_mtime))))
  x.append(os.path.getctime(FILE_NAME))
  x2.append('A'+T_stamp+'_SIG')
  x3.append('A'+T_stamp+'_TAG')
#  x2.append('A'+T_stamp+'_'+filename_w_ext)
  #print(T_stamp)
  namelst.append(FILE_NAME)

#print(EDF['Name'])
EDF=pd.DataFrame(namelst,columns=['Name'])
#print(x)
EDF['Time']=x
#print(EDF['Time'])
EDF['Type']=x1
EDF['NameOut']=x2
EDF['TagOut']=x3

DateTime_from_num=datetime.strptime(DateTime_from,"%Y-%m-%d %H:%M:%S").timestamp()
DateTime_to_num=datetime.strptime(DateTime_to,"%Y-%m-%d %H:%M:%S").timestamp()
print(DateTime_from,DateTime_from_num,DateTime_to,DateTime_to_num)
EDF = EDF.set_index(EDF['Time'])

XASFILES=EDF.Name.loc[DateTime_from_num:DateTime_to_num].tolist()
#print('XASFILES',XASFILES)
XASOUTFILES=EDF.NameOut.loc[DateTime_from_num:DateTime_to_num].tolist()
XASTAGOUTFILES=EDF.TagOut.loc[DateTime_from_num:DateTime_to_num].tolist()
print(len(XASFILES),XAS_Sample,'files were downloaded.')

#Start downloading XAS files
DIR_NAME=XPS_prefix
NEW_DIR_NAME=os.path.join(XPS_exportflder,XAS_Sample)
try:
  os.mkdir(NEW_DIR_NAME)
except OSError as error: 
  print(error)

i=0
for FILE_NAME in XASFILES:
    INPUT_FILE = XASFILES[i]
    OUTPUT_FILE = NEW_DIR_NAME+'//'+XASOUTFILES[i]+'.csv'
    TAGOUTPUT_FILE = NEW_DIR_NAME+'//'+XASTAGOUTFILES[i]+'.csv'
    g2=open(TAGOUTPUT_FILE,"w")
    g3=open(OUTPUT_FILE,"w")
    #print(INPUT_FILE[-8:-4])#.isdigit())
    #print(INPUT_FILE,OUTPUT_FILE)
    # Estimate when the scan was finished.
    # print(FILE_NAME,os.path.getctime(INPUT_FILE),os.path.getmtime(INPUT_FILE))
    spec_start_time=os.path.getctime(INPUT_FILE)
    spec_end_time=os.path.getmtime(INPUT_FILE)
    i=i+1

    idx1="#S "+FILE_NAME[-8:-4]
#    print(idx1)
    idx2="#L "
    idx3="#N "
    idx4="\n "
    with open(SPECDAT_FILE,'r') as g1:
        g1lines=g1.readlines()
        tagcopy=False
        datacopy=False
#        print(g1lines)
        for line in g1lines:
            if idx1 in line.strip():
                tagcopy = True
                datacopy = True
#                print(idx1)
                tag0="Scan,"+line.strip()[3:]
                print(TAGOUTPUT_FILE)
                g2.write(tag0)
                g2.write('\n')
                continue
            elif "#L " in line.strip():
                #datacopy = tagcopy
                tagcopy = False
                if datacopy == True:
                    g3.write(line)
                continue
            elif "#N " in line.strip():
                if datacopy == True:
                     numpnts=line.strip()[3:]
                     print(numpnts)
                     numpntsidx=0
            elif line[0]=='\n':
                datacopy = False
#               print(idx3)
                continue
            elif tagcopy:
                if "#D" in line.strip():
                    tag00= datetime.strptime(line.strip()[3:],'%a %b %d %H:%M:%S %Y')
                    tag01= datetime.strftime(tag00,"%Y%m%d%H%M%S")
                    tag0="TimeStr,"+tag01 #+line.strip()[3:]  %a %b %H:%M:%S %Y
                    g2.write(tag0)
                    g2.write('\n')
                if "#T" in line.strip():
                    tag0="Dwell,"+line.strip()[3:]
                    g2.write(tag0)
                    g2.write('\n')
                if "#P0" in line.strip():
                    list0=list(line.strip()[4:].split(" "))
                    #print(list0)
                if "#P1" in line.strip():
                    list0=list0+list(line.strip()[4:].split(" "))
                    #print(list0)
                if "#P2" in line.strip():
                    list0=list0+list(line.strip()[4:].split(" "))
                    #print(list0)
                if "#P3" in line.strip():
                    list0=list0+list(line.strip()[4:].split(" "))
                    #print(list0)
                if "#P4" in line.strip():
                    list0=list0+list(line.strip()[4:].split(" "))
                    #print(list0)
                if "#P5" in line.strip():
                    list0=list0+list(line.strip()[4:].split(" "))
                    #print(list0)
                if "#P6" in line.strip():
                    list0=list0+list(line.strip()[4:].split(" "))
                    #print(list0)
                    list1=['epu','gap','m0bot','m0top','m0srl','m0spr','m0pit','m0tran','bpmvert','m1vert','m1pit','sgmensz','sgmpit','sgmensw','m1bend','vsample','spare1','spare2','m1yaw_2','m2pit_2','m3pit','m2pit_3','m3horz','m1hor_2','m2ver_2','m2ver_3','spare3','spare4','spare6','spare8','sgmensy','spare5','exsv_1','exsh_1','exsv_2','exsh_2','sgmhorz','exsv_3','exsh_3','coapdet','rotsamp','cryo_y','mono133','mono132','mono131','dac0','dac1','dac2','dac3']
                    for x0 in range(len(list0)):
                        g2.write(list1[x0])
                        g2.write(',')
                        g2.write(list0[x0])
                        g2.write('\n')
                    g2.write('Start time,')
                    g2.write(str(spec_start_time))
                    g2.write('\n')
                    g2.write('End time,')
                    g2.write(str(spec_end_time))
                    g2.write('\n')
                continue                
            elif datacopy:
                 g3.write(str(spec_start_time+numpntsidx*(spec_end_time-spec_start_time)))
                 g3.write(',')
                 g3.write(line)
                 print(spec_start_time+numpntsidx*(spec_end_time-spec_start_time))
                 numpntsidx=numpntsidx+1
                 continue
    g2.close()
    g3.close()
#End downloading XAS files   

#Start downloading XPS files
#Convert all Scienta .txt data in DIR_NAME
#DIR_NAME=prefix
#FILES = glob.glob(os.path.join(DIR_NAME, '*.txt'))
DIR_NAME=XPS_prefix
NEW_DIR_NAME=os.path.join(XPS_exportflder,XPS_Sample)
try:
  os.mkdir(NEW_DIR_NAME)
except OSError as error: 
  print(error)

for FILE_NAME in FILES:
    INPUT_FILE = os.path.join(DIR_NAME, FILE_NAME)    
    REGION_NUM='1'  #xps region number
    SECT_NAME='[Data ' + REGION_NUM + ']'
    OUTPUT_FILE = INPUT_FILE+'_'+ REGION_NUM+'.csv'

    os.chdir(DIR_NAME)
# Estimate when the scan was performed.
    start_time=os.path.getctime(INPUT_FILE)
    end_time=os.path.getmtime(INPUT_FILE)
    print(FILE_NAME,os.path.getctime(INPUT_FILE),os.path.getmtime(INPUT_FILE))

    with open(INPUT_FILE,'r') as g:
        region_counts = Counter(g.read().split())
    
    if region_counts.get('[Data'):
        xmax=region_counts.get('[Data')+1
    else:
        xmax=0

    if xmax >0:
        x = 1
        for x in range(1,xmax):  
            with open(INPUT_FILE, 'r') as f:
                if 'string3' in locals():
                    del string3
                if 'string2' in locals():
                    del string2
                if 'string4' in locals():
                    del string4
                for i in re.split(r'\n\n+', f.read()):
                    REGION_NUM="%d" % x
                    SECT_NAME='[Data ' + REGION_NUM + ']'
                    if i.startswith(SECT_NAME):
                        string=i
                    SECT_NAME2='[Info ' + REGION_NUM + ']'
                    if i.startswith(SECT_NAME2):
                        string2=i                
                    SECT_NAME3='[Run Mode Information ' + REGION_NUM + ']'
                    if i.startswith(SECT_NAME3):
                        string3=i
                    SECT_NAME4='[Signal ' + REGION_NUM + ']'
                    if i.startswith(SECT_NAME4):
                        string4=i

                string=string.split("\n", 1)[1]
                if 'string2' in locals():
                    string2=string2.split("\n", 1)[1]
                    array_from_string = [s.split('  ') for s in string2.split('\n ')]
                    n2=np.array(array_from_string)         
                if 'string3' in locals():
                    string3=string3.split("\n", 1)[1]
                    array_from_string = [s.split('  ') for s in string3.split('\n ')]
                    n3=np.array(array_from_string)
            
                if 'string4' in locals():
                    string4=string4.split("\n", 1)[1]
                    array_from_string = [s.split('  ') for s in string4.split('\n ')]
                    n4=np.array(array_from_string)
             
                WAV_NAME=os.path.splitext(os.path.split(FILE_NAME)[1])[0]
                OUTPUT_FILE=os.path.splitext(os.path.split(FILE_NAME)[0])[0]+'/'+WAV_NAME+'_'+ REGION_NUM+'.csv'
                array_from_string = [s.split('  ') for s in string.split('\n ')]
                n1=np.array(array_from_string)         
      

   #         print(string2)
   #         print(string3)

                HEADER=' '+WAV_NAME+'_X'

                data=[]
                data1=[]
                data2=[]
                for k in range(1,n1.shape[1]):
                    HEADER=HEADER+'  '+WAV_NAME+'_R'+ REGION_NUM +'_S'+str(k)
                    data=np.genfromtxt(StringIO(string))              
                    if 'string2' in locals():
                        info=string2.split('\n')             
                    if 'string2' in locals():
                        runmode=string3.split('\n')            
#                   signal=np.genfromtxt(StringIO(string4))              
                    string1=np.array2string(data)
            print(info.index("Time per Spectrum Channel=")
#            print(runmode)
#            print(signal)
                header_a=[]  
                header_a.append(WAV_NAME+'_X')
                for k in range(1,n1.shape[1]):
                    header_a.append(WAV_NAME+'_R'+ REGION_NUM +'_S'+str(k))
                headersum_a=[]
                headersum_a.append(WAV_NAME+'_Sum_X')
                headersum_a.append(WAV_NAME+'_'+ REGION_NUM +'_Sum')
                headertag_a=[]
                headertag_a.append('tag')
                headertag_a.append('value')
#            print(string1)
                data1=np.sum(data[:,1:n1.shape[1]],axis=1)

                data2=np.column_stack((data[:,0],np.sum(data[:,1:n1.shape[1]],axis=1)))
 
#            print(string1)
                string2=np.array2string(np.swapaxes(data2,1,0))
                XPS_FILE=NEW_DIR_NAME+'/'+WAV_NAME+'_'+ REGION_NUM+'.csv'
                XPSSUM_FILE=NEW_DIR_NAME+'/'+WAV_NAME+'_'+REGION_NUM+'_SUM.csv'
                XPSTAG_FILE=NEW_DIR_NAME+'/'+WAV_NAME+'_'+REGION_NUM+'_TAG.csv'
                XPSSIG_FILE=NEW_DIR_NAME+'/'+WAV_NAME+'_'+REGION_NUM+'_SIG.csv'

                data01=[]
                data21=[]
                for elem in data01:
                    if elem:
                        data01.append(elem)
#            data=np.array(data01)
                for elem in data21:
                    if elem:
                        data21.append(elem)
#            data2=np.array(data21)
                data3=["sample_name=","sample_temperature=","sample_temperature_scale=","sample_pressure=","sample_pressure_scale=torr","sample_environment=","sample_position=","x_scale=","x_0=","y_scale=","y_0=","t_scale=","t_0=","i_energy=","i_flux=","i_size="]
                data3.extend(info)
                data3.extend(runmode)
                data3.append('Start Time='+str(start_time))
                data3.append('End Time='+str(end_time))
                dataframe4=pd.DataFrame(data3)[0].str.split("=",n=1,expand=True)
#            pd.DataFrame(data).to_csv(os.path.splitext(os.path.split(FILE_NAME)[0])[0]+DirSeparator+WAV_NAME+'_'+ REGION_NUM+'.csv',index=False,header=header_a)
#            pd.DataFrame(data2).to_csv(os.path.splitext(os.path.split(FILE_NAME)[0])[0]+DirSeparator+WAV_NAME+'_'+ REGION_NUM+'_SUM.csv',index=False,header=headersum_a)
                pd.DataFrame(data).to_csv(XPS_FILE,index=False,header=header_a,line_terminator='\n')
                pd.DataFrame(data2).to_csv(XPSSUM_FILE,index=False,header=headersum_a,line_terminator='\n')
                pd.DataFrame(dataframe4).to_csv(XPSTAG_FILE,index=False,header=headertag_a,line_terminator='\n')