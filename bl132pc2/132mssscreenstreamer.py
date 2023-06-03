import cv2
import time
import numpy as np
import threading
import mss
#from PIL import ImageGrab

from typing import Optional
from time import sleep
from datetime import datetime

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
        '''Create a new frame every 2 seconds.'''
        monitor ={'top':40,'left':0,'width':800,'height':640}
        with mss.mss() as sct:
            while True:
                time.sleep(2)
                raw = sct.grab(monitor)
                img_np = np.array(raw)
                # Add time stamp
                now = datetime.now()
                dt_string = now.strftime("%Y%m%d %H:%M:%S")
                img_np2 = cv2.putText(img_np,dt_string,(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),1,cv2.LINE_AA)
                # Use numpy and opencv to convert the data to JPEG. 
                img = cv2.imencode('.jpg', img_np2)[1].tobytes()
                yield(img)
        #loop_forever = True
        #while loop_forever:
        #    time.sleep(2)
        #    try:
        #        img_pl = ImageGrab.grab(bbox=(0, 0, 700, 700)) #x, y, w, h
        #        img_np = np.array(img_pl)
        #        #frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        #        now = datetime.now()
        #        dt_string = now.strftime("%Y%m%d %H:%M:%S")
        #        frame = cv2.putText(img_np,dt_string,(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),1,cv2.LINE_AA)
        #ret,frame=raw.read()    
        #        img =cv2.imencode('.jpg',frame)[1].tobytes()
                yield(img)
            except KeyboardInterrupt:
                loop_forever = False
           
            
           


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
       
 
