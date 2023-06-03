#opencv_acquire_streaming_images
#Camera0 Guppy F036C 252215870(DEV_0xA47010F08823E)
#Camera1 Guppy F033B 252219698(DEV_0xA47010F089132)
#Camera2 Guppy F033B 252227729(DEV_0xA47010F08B091)
#Camera3 Guppy F080C 252344840(DEV_0xA47010F0A7A08)

# pip install Pillow
# pip install pip install opencv-python

import cv2
import time
import numpy as np
import threading
from PIL import ImageGrab

from typing import Optional
from time import sleep
from datetime import datetime
#pymba
#from pymba import Vimba
#from pymba import Frame

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
                img_pl = ImageGrab.grab(bbox=(0, 0, 1190, 640)) #x, y, w, h
                img_np = np.array(img_pl)
                #frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
                now = datetime.now()
                dt_string = now.strftime("%Y%m%d %H:%M:%S")
                frame = cv2.putText(img_np,dt_string,(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),1,cv2.LINE_AA)
        #ret,frame=raw.read()    
                img =cv2.imencode('.jpg',frame)[1].tobytes()
                yield(img)
            except KeyboardInterrupt:
                loop_forever = False
            time.sleep(5)
            
           


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
    app.run(host='0.0.0.0', debug=True)        
       
 
