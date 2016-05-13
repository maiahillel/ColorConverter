import sys

sys.path.append('/usr/lib/pymodules/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages')
sys.path.append('/usr/lib/pyshared/python2.7/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

import numpy
import os.path
import cv2
from PyQt4.QtGui import QApplication, QImage, QPainter, QWidget, qRgb

class Tuner(QWidget):

    #: Window to show results in
    window_name = "Tuner"
    
    def __init__(self, converter):
        
        self.situation = 1
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
        # update the image shown on screen

        widget = QWidget.__init__(self)
        widget.setWindowTitle('PyQt - OpenCV Test')
        widget.show()
        # cv2.imshow(self.window_name, image)
        cv2.waitKey(1)

    def build_image(self,im):
        gray_color_table = [qRgb(i, i, i) for i in range(256)]

        if im is None:
            return QImage()

        if im.dtype == numpy.uint8:
            if len(im.shape) == 2:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
                qim.setColorTable(gray_color_table)
                return qim

            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888);
                    return qim.copy()
                elif im.shape[2] == 4:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32);
                    return qim

    def set_image(self, image):
        # first initialization of image onto screen
        self.image = image
        self.update_image()

    def destroy_windows(self):
        cv2.destroyWindow(self.window_name)
        cv2.destroyAllWindows()

