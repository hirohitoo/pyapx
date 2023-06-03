#opencv_acquire_streaming_images

import cv2
import time

vid = cv2.VideoCapture(0)

while True:

    ret, frame = vid.read()
#    frame=frame[0:600,0:800]
    #frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('USB camera', frame)
    time.sleep(1)
    if cv2.waitKey(4) & 0xFF == ord('q'):
        break


vid.release()
cv2.destroyAllWindows()