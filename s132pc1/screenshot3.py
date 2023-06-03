import numpy as np
import cv2
import time
from PIL import ImageGrab


img = ImageGrab.grab(bbox=(0, 0, 1000, 1100)) #x, y, w, h
img_np = np.array(img)
frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
cv2.imshow("frame", frame)

cv2.waitKey(10000)
cv2.destroyAllWindows()