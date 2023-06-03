import cv2

import numpy as np

import pyautogui
import sys

image = pyautogui.screenshot()
#open_cv_image=np.array(img)
#open_cv_image=open_cv_image[:,:,::-1].copy()
cv2.imshow('image',image)