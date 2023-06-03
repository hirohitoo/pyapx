import time
import numpy as np
import pytesseract
#import cv2
#import string
#import re
#import win32com.client

from PIL import ImageGrab
from win32 import win32gui
from epics import caget,caput

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\b_ogasawara.SSRLAD\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
while True:
	try:
		hwnd = win32gui.FindWindow(None, 'SES')
		win32gui.SetForegroundWindow(hwnd)
		#dimensions = win32gui.GetWindowRect(hwnd)
		#img = ImageGrab.grab(bbox=dimensions)
		#img_gr = img.convert('L')
		#text = pytesseract.image_to_string(img_gr,lang=None)

		try:
			ex=win32gui.FindWindowEx(hwnd,None,"TStatusBar",None)
			#print('ex',ex)
		except:
			text='error'
		win32gui.SetForegroundWindow(hwnd)
		dimensions = win32gui.GetWindowRect(ex)
		img = ImageGrab.grab(bbox=dimensions)
		img_gr = img.convert('L')
		text = pytesseract.image_to_string(img_gr,lang=None,config='--psm 7')
		if text.startswith('Region'):
			print('filename=',text)
	except:
		text='error'
	time.sleep(60)