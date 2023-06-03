import nidaqmx
import time
import numpy as np
import pytesseract
import cv2
import string
import re
import win32com.client

from PIL import ImageGrab
from win32 import win32gui
from epics import caget,caput

def int_to_bool_list(num):
	return [bool(num & (1<<n)) for n in range(8)]

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\b_ogasawara.SSRLAD\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

shell=win32com.client.Dispatch('WScript.Shell')

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
chars = '1234567890'
print("132ses.py")
print("SES:Busy","SES:KineticEnergy","SES:Area")
actionlist=[]
openreqlist=[]
openenblist=[]
closereqlist=[]

while True:
	SESKineticEnergy=caget('SES:KineticEnergy')
	SESBusy=0
	text=''
	SESCalOnRQ=caget('SES:CalOn_RQ')
	if SESCalOnRQ ==1:
		#execute
		print('Cal On')
	caput('SES:CalOn_RQ',0)
	SESCalOffRQ=caget('SES:CalOff_RQ')
	if SESCalOffRQ ==1:
		#execute
		print('Cal Off')
	caput('SES:CalOff_RQ',0)
	SESRunRQ=caget('SES:Run_RQ')
	if SESRunRQ ==1:
		try:
    			hwnd = win32gui.FindWindow(None,'SES')
		except:
			#NO windows
			print('1SES is not running')
		else:			
			#Send Key 'Ctrl-G'
			win32gui.SetForegroundWindow(hwnd)
			shell.SendKeys('^G',0)
	caput('SES:Run_RQ',0)

	SESStopRQ=caget('SES:Stop_RQ')  #1=force stop, #2=stop after sequence, #3=stop after scan
	if SESStopRQ ==1:
		#force stop
		try:
    			hwnd = win32gui.FindWindow(None,'SES')			
		except:
			#NO windows
			print('2SES is not running')
		else:
			win32gui.SetForegroundWindow(hwnd)
			shell.SendKeys('^X',0)
			#Send Key 'Ctrl-X'
	elif SESStopRQ ==2:
		try:
    			hwnd = win32gui.FindWindow(None,'SES')
			#Send Key 'Ctrl-Q'
		except:
			#NO windows
			print('3SES is not running')
		else:
			win32gui.SetForegroundWindow(hwnd)
			shell.SendKeys('^Q',0)
			#Send Key 'Ctrl-Q'
		#stop after sequence
	elif SESStopRQ ==3:
		#stop after scan
		try:
    			hwnd = win32gui.FindWindow(None,'SES')	
		except:
			#NO windows
			print('4SES is not running')
		else:
			win32gui.SetForegroundWindow(hwnd)
			shell.SendKeys('^R',0)
			#Send Key 'Ctrl-R'
		caput('SES:Stop_RQ',0)
	
	#hwnd0 = 
	else:
		
		try:
			hwnd0= win32gui.FindWindow(None,'Voltage Calibration')
		except:
			SESBusy=0
			#print("A ",hwnd0)
		else:
#			print("A ",hwnd0)
#			#win32gui.SetForegroundWindow(hwnd0)
			if win32gui.IsWindowVisible(hwnd0):
				SESBusy=1
			#elif win32gui.IsWindowEnabled(hwnd0):
			#	SESBusy=1
			else:
				SESBusy=0
		
			

		
	#ses busy
		#print('Voltage is running.')
		#SESBusy=1
		#caput('SES:BUSY',1)
		
		#slell.SendKeys('E',0)	
	#except:
		#NO windows

	try:
		hwnd = win32gui.FindWindow(None, 'SES')
		win32gui.SetForegroundWindow(hwnd)
		#print('c',hwnd)
		#dimensions = win32gui.GetWindowRect(hwnd)
		#img = ImageGrab.grab(bbox=dimensions)
		#img_gr = img.convert('L')
		#text = pytesseract.image_to_string(img_gr,lang=None)

		try:
			ex=win32gui.FindWindowEx(hwnd,None,"TStatusBar",None)
			
		except:
			text='error'
		#win32gui.SetForegroundWindow(hwnd)
		else:
			SESBusy=1
			win32gui.SetForegroundWindow(hwnd)
			#print('ex',ex)
			dimensions = win32gui.GetWindowRect(ex)
			img = ImageGrab.grab(bbox=dimensions)
			img_gr = img.convert('L')
			text = pytesseract.image_to_string(img_gr,lang=None,config='--psm 7')
			#print('x ',text)

	except:
		text=''
			#SESBusy=0
	caput('SES:BUSY',SESBusy)

	if text.find('Ek =') !=-1:
		print(text[0:100])



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
	SESArea=np.sum(data0)/500
	SESArea=int(np.mean(data0)*0.8)
	caput("SES:Area",SESArea)
	listToStr = ''.join([str(elem) for elem in text])
	vallist=text.split(' ')
		#print(vallist)
		#vallist=strlist[-3].split(' ')
	length=len(text)
		#lastchar=text[length-101:length-1]
		#fnumberlist=vallist[6].split('\\')
		#fnumber=re.sub('[^0-9]','',fnumberlist[-1])
		#print(SESKineticEnergy,SESArea,eval(vallist[2]),eval(vallist[5]),fnumber,vallist[11],end='\r')
		#print(SESKineticEnergy,SESArea,vallist[1],end='\r')
	print(SESBusy,SESKineticEnergy,SESArea,end='\r')
	time.sleep(0.5)
