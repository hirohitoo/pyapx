# place index.html in ./templates
# default port #: 5000
# app.run(host='0.0.0.0', port=5000)

import cv2
import numpy

import threading
import time

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

        raw=cv2.VideoCapture(0)
        while True:
            time.sleep(1)
            ret,frame=raw.read()
            frame=frame[200:440,0:640]
            #frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
            img =cv2.imencode('.jpg',frame)[1].tobytes()
            yield(img)

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
#import threading
#import numpy
#import time
#import cv2

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