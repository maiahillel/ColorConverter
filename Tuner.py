import sys

sys.path.append('/usr/lib/pymodules/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages')
sys.path.append('/usr/lib/pyshared/python2.7/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

import numpy
import os.path
import cv2
from matplotlib import pyplot as plt
from PyQt4.QtGui import QApplication, QImage, QPainter, QWidget, qRgb

capture = cv2.VideoCapture(0)

if __name__ == '__main__':

    ret, img = capture.read()
    img = cv2.imread('OpenCV_Logo_B.png')     # input
    mask = cv2.imread('OpenCV_Logo_C.png',0)  # mask

    dst_TELEA = cv2.inpaint(img,mask,3,cv2.INPAINT_TELEA)
    dst_NS = cv2.inpaint(img,mask,3,cv2.INPAINT_NS)

    plt.subplot(221), plt.imshow(img)
    plt.title('degraded image')
    plt.subplot(222), plt.imshow(mask, 'gray')
    plt.title('mask image')
    plt.subplot(223), plt.imshow(dst_TELEA)
    plt.title('TELEA')
    plt.subplot(224), plt.imshow(dst_NS)
    plt.title('NS')

    plt.tight_layout()
    plt.show()

