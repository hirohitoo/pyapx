#opencv_acquire_streaming_images
#Camera0 Guppy F036C 252215870(DEV_0xA47010F08823E)
#Camera1 Guppy F033B 252219698(DEV_0xA47010F089132)
#Camera2 Guppy F033B 252227729(DEV_0xA47010F08B091)
#Camera3 Guppy F080C 252344840(DEV_0xA47010F0A7A08)

import cv2
import time
import numpy as np
import threading

from typing import Optional
from time import sleep
#pymba
from pymba import Vimba
from pymba import Frame

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
        with Vimba() as vimba:
            camera0 = vimba.camera(0)
            camera0.open()
            camera1 = vimba.camera(1)
            camera1.open()
            camera2 = vimba.camera(2)
            camera2.open()
            camera3 = vimba.camera(3)
            camera3.open()

            loop_forever = True
            while loop_forever:
                try:
        
                    camera3.arm('SingleFrame')# display_frame3)
                    frame3=camera3.acquire_frame(2000)

                    image3=frame3.buffer_data_numpy()
                    camera3.disarm()
                    large3 = cv2.resize(image3, (0,0), fx=2, fy=2)
                    cropped3 = large3[450:650,400:1040]  # Crop from {x, y, w, h } => [y:y+dy,x:x+dx]  dy=200 dx=640
                    # Draw a rectangle
                    cv2.rectangle(image3,     # source image
              (200, 225),          # upper left corner vertex: x/2, y/2
              (520, 325),         # lower right corner vertex: (x+dx)2, (y+dy)/2
              (255, 255, 255),        # color
              thickness=1,        # line thickness
              lineType=cv2.LINE_8  # line type
    )
                    imagevstack3=np.vstack((cropped3,image3))
                    imagevstack3=cv2.resize(imagevstack3,(0,0),fx=0.5,fy=0.5)                  

                    camera2.arm('SingleFrame')
                    frame2=camera2.acquire_frame(2000)

                    image2=frame2.buffer_data_numpy()
                    camera2.disarm()
                    large2 = cv2.resize(image2, (0,0), fx=2, fy=2)
                    cropped2 = large2[450:650,400:1040]  # Crop from {x, y, w, h } => [y:y+dy,x:x+dx]
            # Draw a rectangle
                    cv2.rectangle(image2,     # source image
              (200, 225),          # upper left corner vertex
              (520, 325),         # lower right corner vertex
              (255, 255, 255),        # color
              thickness=1,        # line thickness
              lineType=cv2.LINE_8  # line type
    )

                    imagevstack2=np.vstack((cropped2,image2))
                    imagevstack2=cv2.resize(imagevstack2,(0,0),fx=0.5,fy=0.5)
                 
                    camera1.arm('SingleFrame')
                    frame1=camera1.acquire_frame(2000)

                    image1=frame1.buffer_data_numpy()
                    camera1.disarm()
                    large1 = cv2.resize(image1, (0,0), fx=2, fy=2)
                    cropped1 = large1[450:650,150:790]  # Crop from {x, y, w, h } => [y:y+dy,x:x+dx]
        # Draw a rectangle
                    cv2.rectangle(image2,     # source image
              (75, 225),          # upper left corner vertex
              (395, 325),         # lower right corner vertex
              (255, 255, 255),        # color
                    thickness=1,        # line thickness
                    lineType=cv2.LINE_8  # line type
    )

                    imagevstack1=np.vstack((cropped1,image1))
                    imagevstack1=cv2.resize(imagevstack1,(0,0),fx=0.5,fy=0.5)

                    camera0.arm('SingleFrame')# display_frame0)
                    frame0=camera0.acquire_frame(2000)
                    camera0.disarm()
                    image0=frame0.buffer_data_numpy()

                    large0 = cv2.resize(image0, (0,0), fx=2, fy=2)
                    cropped0 = large0[200:400,400:1040]  # Crop from {x, y, w, h } => [y:y+dy,x:x+dx]

        # Draw a rectangle
                    cv2.rectangle(image0,     # source image
                  (200, 100),          # upper left corner vertex: x/2, y/2
                  (520, 200),         # lower right vcorner vertex: (x+dx)/2,(y+dy)/2     
                  (255, 255, 255),        # color
                  thickness=1,        # line thickness
                  lineType=cv2.LINE_8  # line type
                  )
                    imagevstack0=np.vstack((cropped0,image0))
                    imagevstack0=cv2.resize(imagevstack0,(0,0),fx=0.5,fy=0.5)

                    imagehstack03=np.hstack((imagevstack0,imagevstack3))
                    imagehstack12=np.hstack((imagevstack1,imagevstack2))
                    imagevstack1203=np.vstack((imagehstack03,imagehstack12))
                  #cv2.imshow('PREP',imagevstack1203)
                  #cv2.waitKey(50)
        #ret,frame=raw.read()    
                    img =cv2.imencode('.jpg',imagevstack1203)[1].tobytes()
                    yield(img)
                except KeyboardInterrupt:
                    loop_forever = False
            camera0.close()
            camera1.close()
            camera2.close()
            camera3.close()
           


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
       
 
