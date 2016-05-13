import numpy
import cv2 as cv
from PyQt4.QtGui import *


class IplQImage(QImage):
    def __init__(self,frame):
        iplimage = cv.cv.CreateImageHeader((frame.shape[1], frame.shape[0]), cv.cv.IPL_DEPTH_8U, 3)
        cv.cv.SetData(iplimage, frame.tostring(), frame.dtype.itemsize * 3 * frame.shape[1])

        alpha = cv.cv.CreateMat(iplimage.height, iplimage.width, cv.cv.CV_8UC1)
        cv.cv.Rectangle(alpha, (0, 0), (iplimage.width, iplimage.height), cv.cv.ScalarAll(255), -1)
        rgba = cv.cv.CreateMat(iplimage.height, iplimage.width, cv.cv.CV_8UC4)
        cv.cv.Set(rgba, (1, 2, 3, 4))
        cv.cv.MixChannels([iplimage, alpha],[rgba], [(0, 0),(1, 1),(2, 2),(3, 3)])

        self.__imagedata = rgba.tostring()
        super(IplQImage,self).__init__(self.__imagedata, iplimage.width,iplimage.height, QImage.Format_RGB32)
