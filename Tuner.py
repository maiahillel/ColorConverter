import sys

sys.path.append('/usr/lib/pymodules/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages')
sys.path.append('/usr/lib/pyshared/python2.7/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

import numpy
import os.path
import cv2

class Tuner(object):

    #: Window to show results in
    window_name = "Tuner"
    
    def __init__(self, converter):
        
     
        self.converter = converter
        cv2.namedWindow(self.window_name)
        cv2.moveWindow(self.window_name, 300, 180)
        
        cv2.createTrackbar("Adjust Image", self.window_name,
                           100, 100,
                           self.set_adjust)

        # Initialize first showing of the image
        self.update_image()

    def set_adjust(self, setting):

        # self.image.key = setting
        self.converter.key = setting
        # self.update_image()

    def update_image(self):

        image = self.converter.convert()
        #update the image shown on screen
        cv2.imshow(self.window_name, image)
        cv2.waitKey(1)

    def set_image(self, image):
        # first initialization of image onto screen
        self.image = image
        self.update_image()

    def destroy_windows(self):
        cv2.destroyWindow(self.window_name)