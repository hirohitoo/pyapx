#opencv_acquire_streaming_images
#Camera0 Guppy F036C 252215870(DEV_0xA47010F08823E)
#Camera1 Guppy F033B 252219698(DEV_0xA47010F089132)
#Camera2 Guppy F033B 252227729(DEV_0xA47010F08B091)
#Camera3 Guppy F080C 252344840(DEV_0xA47010F0A7A08)

import cv2
import time
#import matplotlib.pyplot as plt
import numpy as np

from typing import Optional
from time import sleep
#pymba
from pymba import Vimba
from pymba import Frame

#from examples.camera._display_frame import display_frame

def display_frame0(frame: Frame, delay: Optional[int] = 1) -> None:
    """
    Displays the acquired frame.
    :param frame: The frame object to display.
    :param delay: Display delay in milliseconds, use 0 for indefinite.
    """
    #print('frame {}'.format(frame.data.frameID))

    # get a copy of the frame data
    image = frame.buffer_data_numpy()
    
    large = cv2.resize(image, (0,0), fx=2, fy=2)
    cropped = large[200:400,400:1040]  # Crop from {x, y, w, h } => [y:y+dy,x:x+dx]

    # convert colour space if desired
    #try:
        #image = cv2.cvtColor(image, PIXEL_FORMATS_CONVERSIONS[frame.pixel_format])
    #except KeyError:
    #    pass
    # Draw a rectangle
    cv2.rectangle(image,     # source image
              (200, 100),          # upper left corner vertex
              (520, 200),         # lower right vcorner vertex
              (255, 255, 255),        # color
              thickness=1,        # line thickness
              lineType=cv2.LINE_8  # line type
    )
    imagevstack=np.vstack((cropped,image))
    imagevstack=cv2.resize(imagevstack,(0,0),fx=0.5,fy=0.5)


def display_frame3(frame: Frame, delay: Optional[int] = 1) -> None:
    """
    Displays the acquired frame.
    :param frame: The frame object to display.
    :param delay: Display delay in milliseconds, use 0 for indefinite.
    """
    #print('frame {}'.format(frame.data.frameID))

    # get a copy of the frame data
    image = frame.buffer_data_numpy()
    
    large = cv2.resize(image, (0,0), fx=2, fy=2)
#    cropped = large[900:1100,760:1400]  # Crop from {x, y, w, h } => [y:y+dy,x:x+dx]

    # convert colour space if desired
    #try:
        #image = cv2.cvtColor(image, PIXEL_FORMATS_CONVERSIONS[frame.pixel_format])
    #except KeyError:
    #    pass
    # Draw a rectangle
    cv2.rectangle(image,     # source image
              (380, 450),          # upper left corner vertex
              (700, 550),         # lower right corner vertex
              (255, 255, 255),        # color
              thickness=1,        # line thickness
              lineType=cv2.LINE_8  # line type
    )
    image=image[200:680,100:740]
    imagevstack=np.vstack((cropped,image))
    imagevstack=cv2.resize(imagevstack,(0,0),fx=0.5,fy=0.5)

    #cv2.imshow('PREPside', image)
    #cv2.imshow('PREPside Cropped', cropped)
   
#    cv2.imshow('PREPside', imagevstack)
#    cv2.waitKey(delay)
#    return imagevstack

if __name__ == '__main__':

    with Vimba() as vimba:
        camera0 = vimba.camera(0)
        camera0.open()
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





                  camera0.arm('SingleFrame')# display_frame0)
                  frame0=camera0.acquire_frame(2000)
                  camera0.disarm()
                  image0=frame0.buffer_data_numpy()

                  large0 = cv2.resize(image0, (0,0), fx=2, fy=2)
                  cropped0 = large0[200:400,400:1040]  # Crop from {x, y, w, h } => [y:y+dy,x:x+dx]

                  # convert colour space if desired
                  #try:
                  #image = cv2.cvtColor(image, PIXEL_FORMATS_CONVERSIONS[frame.pixel_format])
                  #except KeyError:
                  #    pass
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
                  cv2.imshow('PREP',imagehstack03)
                  cv2.waitKey(50)
                  #display_frame0(frame0,0)
                  #display_frame3(frame3,0)
                  #time.sleep(0.5)
               except KeyboardInterrupt:
                  loop_forever = False

        #camera0.stop_frame_acquisition()
        
        #camera3.stop_frame_acquisition()


        camera0.close()
        camera3.close()