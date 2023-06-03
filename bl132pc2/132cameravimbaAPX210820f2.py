#opencv_acquire_streaming_images
#Camera0 Guppy F036C 252215870(DEV_0xA47010F08823E)
#Camera1 Guppy F033B 252219698(DEV_0xA47010F089132)
#Camera2 Guppy F033B 252227729(DEV_0xA47010F08B091)
#Camera3 Guppy F080C 252344840(DEV_0xA47010F0A7A08)

import cv2
import time
from datetime import datetime
import numpy as np

from typing import Optional
from time import sleep
#pymba
from pymba import Vimba
from pymba import Frame

if __name__ == '__main__':

    with Vimba() as vimba:
        camera0 = vimba.camera(0)
        camera0.open()
        camera1 = vimba.camera(1)
        camera1.open()
        camera2 = vimba.camera(2)
        camera2.open()
        camera3 = vimba.camera(3)
        camera3.open()

        
        #camera0.start_frame_acquisition()
        #camera3.start_frame_acquisition()

        loop_forever = True
        while loop_forever:
               try:
                  camera3.arm('SingleFrame')# display_frame3)
                  frame3=camera3.acquire_frame(5000)

                  image3=frame3.buffer_data_numpy()

#                  cv2.imshow('PREPside',image3)
#                  cv2.waitKey(50)
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

#                  cv2.imshow('PREPside',imagevstack3)
#                  cv2.waitKey(50)


                  camera2.arm('SingleFrame')
                  frame2=camera2.acquire_frame(5000)

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
                  frame1=camera1.acquire_frame(5000)

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

#                  cv2.imshow('PREPtop',imagevstack0)
#                  cv2.waitKey(50)

                  imagehstack03=np.hstack((imagevstack0,imagevstack3))
                  imagehstack12=np.hstack((imagevstack1,imagevstack2))
                  imagevstack1203=np.vstack((imagehstack03,imagehstack12))

# Draw time stamp
                  now = datetime.now()
                  dt_string = now.strftime("%Y%m%d %H:%M:%S")
                  imagevstack1203s = cv2.putText(imagevstack1203,dt_string,(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),1,cv2.LINE_AA)

                  cv2.imshow('PREP',imagevstack1203)
                  cv2.waitKey(50)

               except KeyboardInterrupt:
                  loop_forever = False


        camera0.close()
        camera1.close()
        camera2.close()
        camera3.close()