import numpy as np
from PIL import ImageGrab
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
#from textblob import TextBlob


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\b_ogasawara.SSRLAD\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
# Grab some screen
screen =  ImageGrab.grab(bbox=(0,0,800,640))
# Make greyscale
w = screen.convert('L')

# Save so we can see what we grabbed
#w.save('grabbed.png')

text = pytesseract.image_to_string(w)
#correctedText = TextBlob(text).correct()

print(text)