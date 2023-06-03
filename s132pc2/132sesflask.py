import nidaqmx
import time
import numpy as np
import pytesseract
import cv2
import string
import re
import win32com.client
import threading

from PIL import ImageGrab
from win32 import win32gui
from epics import caget,caput

def int_to_bool_list(num):
	return [bool(num & (1<<n)) for n in range(8)]

text='???'
fnumber=0

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\b_ogasawara.SSRLAD\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

shell=win32com.client.Dispatch('WScript.Shell')

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
chars = '1234567890'
print("132ses.py")
print("SES:KineticEnergy","SES:Area")
actionlist=[]
openreqlist=[]
openenblist=[]
closereqlist=[]

def ses():	
#	while True:
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
    			hwnd = win32gui.FindWindow('SES', None)
		except:
			#NO windows
			print('1SES is not running')
		else:			
			#Send Key 'Ctrl-G'
			win32gui.SetForegroundWindow(hwnd)
			slell.SendKeys('^G',0)
	caput('SES:Run_RQ',0)

	SESStopRQ=caget('SES:Stop_RQ')  #1=force stop, #2=stop after sequence, #3=stop after scan
	if SESStopRQ ==1:
		#force stop
		try:
			hwnd = win32gui.FindWindow('SES', None)			
		except:
			#NO windows
			print('2SES is not running')
		else:
			win32gui.SetForegroundWindow(hwnd)
			slell.SendKeys('^X',0)
			#Send Key 'Ctrl-X'
	elif SESStopRQ ==2:
		try:
			hwnd = win32gui.FindWindow('SES', None)
			#Send Key 'Ctrl-Q'
		except:
			#NO windows
			print('3SES is not running')
		else:
			win32gui.SetForegroundWindow(hwnd)
			slell.SendKeys('^Q',0)
			#Send Key 'Ctrl-Q'
		#stop after sequence
	elif SESStopRQ ==3:
		#stop after scan
		try:
			hwnd = win32gui.FindWindow('SES', None)	
		except:
			#NO windows
			print('4SES is not running')
		else:
			win32gui.SetForegroundWindow(hwnd)
			slell.SendKeys('^R',0)
			#Send Key 'Ctrl-R'
	caput('SES:Stop_RQ',0)

	SESKineticEnergy=caget('SES:KineticEnergy')
	try:
		hwnd = win32gui.FindWindow('Voltage', None)		
	except:
		#NO windows
		caput('SES:BUSY',0)
	else:
		#ses busy
		caput('SES:BUSY',1)
		#win32gui.SetForegroundWindow(hwnd)
		#slell.SendKeys('E',0)

	#	BL132PhotonEnergy=caget('BL132:PhotonEnergy')
	#BL132WaveLength
	#BL132Power
	#BL132PhotonFlux
	#APXFluence
	APXFootPrint=0.05*0.05
	hwnd = win32gui.FindWindow('SES',None)
	win32gui.SetForegroundWindow(hwnd)
	dimensions = win32gui.GetWindowRect(hwnd)
	try:
		
		
		#img = ImageGrab.grab(bbox=dimensions)
		#img_gr = img.convert('L')
		#text = pytesseract.image_to_string(img_gr,lang=None)

		try:
			ex=win32gui.FindWindowEx(hwnd,None,"TStatusBar",None)
			#print('ex',ex)
		except:
			text='error'
		#win32gui.SetForegroundWindow(hwnd)
		dimensions = win32gui.GetWindowRect(ex)
		#img = ImageGrab.grab(bbox=dimensions)
		img_gr = img.convert('L')
		text = pytesseract.image_to_string(img_gr,lang=None)
		#print('text',text)

	except:
		text='error'

	#with nidaqmx.Task() as task0:
#		task0.ci_channels.add_ci_count_edges_chan("Dev5/ctr1")#,meas_time=1.0)#,name_to_assign_to_channel='PFI4')#,edge=Edge.RISING,initial_count=0,count_direction=CountDirection.COUINT_UP)
#		task0.ci_channels[0].ci_count_edges_term="PFI4"
	#	#task0.ci_channels[0].ci_count_edges_term="100kHzTimebase"
	#	task0.start()
	#	#task0.ci_channels.add_ci_count_edges_chan("Dev5/ctr1",name_to_assign_to_channel='/Dev5/PFI4',min_val=2.0, max_val=5000000,edge=Edge.RISING)
	#	#read_task.ci_channels.all.ci_count_edges_term = 'PFI4'
	#	data0=task0.read(5000)   
	#	SESArea=data0[0]#*1.08
	#	SESArea=np.sum(data0)/500
		#	SESArea=int(np.mean(data0)*0.8)
		#	caput("SES:Area",SESArea)
		#	listToStr = ''.join([str(elem) for elem in text])
			#vallist=text.split(' ')
		
			#length=len(text)
		
			#fnumberlist=vallist[6].split('\\')
			#fnumber=re.sub('[^0-9]','',fnumberlist[-1])
			#print(SESKineticEnergy,SESArea,eval(vallist[2]),eval(vallist[5]),fnumber,vallist[11],end='\r')
		#print(SESKineticEnergy,SESArea,text,end='\r')
	vallist=text.split(' ')
		
			#length=len(text)
	fnumber=0
	if len(vallist)>6:
		fnumberlist=vallist[6].split('\\')
		fnumber=re.sub('[^0-9]','',fnumberlist[-1])
	else:
		fnumber=0		
	print('x')
	time.sleep(0.4)
	return 'text'

class Camera(object):
	thread = None
	frame = None
	last_access = 0

	def __init__(self):
		if Camera.thread is None:
			Camera.last_access = time.time()
			Camera.thread = threading.Thread(target=self._thread)
			Camera.thread.start()

		while self.get_frame() is None:
			time.sleep(0)

	def get_frame(self):
		'''Get the current frame.'''
		Camera.last_access = time.time()
		return Camera.frame

	@staticmethod
	def frames():
		'''Create a new frame every 1 seconds.'''
        

		loop_forever = True
		while loop_forever:
			try:	
				hwnd = win32gui.FindWindow(None,'Ses.exe')			
				try:
					ex=win32gui.FindWindowEx(hwnd,None,'TStatusBar',None)
			#print('ex',ex)
				except:
					ex=hwnd
		#win32gui.SetForegroundWindow(hwnd)
		#		print(ex)
				win32gui.SetForegroundWindow(hwnd)
				dimensions=win32gui.GetWindowRect(hwnd)#,&rcView)
				#win32gui.GetWindowRect(ex,&rcView)
				
				#dimensions = MapWindowPoints(HWND_DESKTOP, hwnd, (LPPOINT)&rcView, 2);
				img = ImageGrab.grab(bbox=dimensions)
				#img_gr = img.convert('L')
				#text = pytesseract.image_to_string(img_gr,lang=None)
				#print('text',text)
				dimensions=(0,0,150,150)
				img_pl = ImageGrab.grab()#(bbox=(50,50,150,150),all_screens=False) #x, y, w, h
				img_np = np.array(img_pl)
                		#frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
				#now = datetime.now()
				#dt_string = now.strftime("%Y%m%d %H:%M:%S")
				frame=img_np
                		#frame = cv2.putText(img_np,dt_string,(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),1,cv2.LINE_AA)
        			#ret,frame=raw.read()    
				img =cv2.imencode('.jpg',frame)[1].tobytes()
				yield(img)
			except KeyboardInterrupt:
				loop_forever = False
			time.sleep(2)
            
           


	@classmethod
	def _thread(cls):
		'''As long as there is a connection and the thread is running, reassign the current frame.'''
		print('Starting camera thread.')


		frames_iter = cls.frames()
		for frame in frames_iter:
			Camera.frame = frame
			if time.time() - cls.last_access > 10:
				frames_iter.close()
				print('Stopping camera thread due to inactivity.')
				break

		cls.thread = None

from flask import Response
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int('80'),debug=True)   
