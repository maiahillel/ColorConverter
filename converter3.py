# -*- coding: iso-8859-1 -*-
"""
   MoinMoin - Daltonize ImageCorrection - Effect

   Daltonize image correction algorithm implemented according to
   http://scien.stanford.edu/class/psych221/projects/05/ofidaner/colorblindness_project.htm

   Many thanks to Onur Fidaner, Poliang Lin and Nevran Ozguven for their work
   on this topic and for releasing their complete research results to the public
   (unlike the guys from http://www.vischeck.com/). This is of great help for a
   lot of people!

   Please note:
   Daltonize ImageCorrection needs
   * Python Image Library (PIL) from http://www.pythonware.com/products/pil/
   * NumPy from http://numpy.scipy.org/

   You can call Daltonize from the command-line with
   "daltonize.py C:\image.png"

   Explanations:
       * Normally this module is called from Moin.AttachFile.get_file
       * @param filename, fpath is the filename/fullpath to an image in the attachment
         dir of a page.
       * @param color_deficit can either be
           - 'd' for Deuteranope image correction
           - 'p' for Protanope image correction
           - 't' for Tritanope image correct
   Idea:
       * Since daltonizing an image takes quite some time and we don't want visually
         impaired users to wait so long until the page is loaded, this module has a
         command-line option built-in which could be called as a separate process
         after a file upload of a non visually impaired user in "AttachFile", e.g
         "spawnlp(os.NO_WAIT...)"
       * "AttachFile": If an image attachment is deleted or overwritten by a new version
         please make sure to delete the daltonized images and redaltonize them.
       * But all in all: Concrete implementation of ImageCorrection needs further
         thinking and discussion. This is only a first prototype as proof of concept.

   @copyright: 2007 by Oliver Siemoneit
   @license: GNU GPL, see COPYING for details.

"""
import sys

sys.path.append('/usr/lib/pymodules/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages')
sys.path.append('/usr/lib/pyshared/python2.7/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

import numpy
import os.path
import cv2
from timeit import default_timer as timer
import threading, time

cameraPort = 0
camera = cv2.VideoCapture(cameraPort)
# Transformation matrix for Deuteranope (a form of red/green color deficit)
lms2lmsd = numpy.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]])
# Transformation matrix for Protanope (another form of red/green color deficit)
lms2lmsp = numpy.array([[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]])
# Transformation matrix for Tritanope (a blue/yellow deficit - very rare)
lms2lmst = numpy.array([[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]])
# Colorspace transformation matrices
rgb2lms = numpy.array([[17.8824, 43.5161, 4.11935], [3.45565, 27.1554, 3.86714], [0.0299566, 0.184309, 1.46709]])

lms2rgb = numpy.linalg.inv(rgb2lms)
# transformation matrix include moving back and forth to lms space
lmsd2rgb = numpy.dot(lms2rgb, numpy.dot(lms2lmsd, rgb2lms))
lmsp2rgb = numpy.dot(lms2rgb, numpy.dot(lms2lmsp, rgb2lms))
lmst2rgb = numpy.dot(lms2rgb, numpy.dot(lms2lmst, rgb2lms))

# Daltonize image correction matrix
err2mod = numpy.array([[0, 0, 0], [0.7, 1, 0], [0.7, 0, 1]])
#key = 10
zoom = 1
def get_image():
    # read is the easiest way to get a full image out of a VideoCapture object.
    ret, im = camera.read()
    return im


# def get_image():
# return cv2.imread("/Users/orbarda/Downloads/board.jpg")

def video(color_deficit):
    # Get the requested image correction
    if color_deficit == 'd':
        transmat_deficit = lmsd2rgb
    elif color_deficit == 'p':
        transmat_deficit = lmsp2rgb
    elif color_deficit == 't':
        transmat_deficit = lmst2rgb

    for x in xrange(1, 100000000):
        start = timer()

        cv2_image = get_image()
        resized = cv2.resize(cv2_image, (800, 600))
        x = ((cv2_image.shape[0] / zoom) * zoom / 2.0) - (cv2_image.shape[0] / zoom / 2.0)
        y = ((cv2_image.shape[1] / zoom) * zoom / 2.0) - (cv2_image.shape[1] / zoom / 2.0)
        x1 = cv2_image.shape[0] / zoom
        y1 = cv2_image.shape[1] / zoom
        rect = cv2_image[x:x1, y:y1]
        zoomed = cv2.resize(rect, (800, 600))
        #cv2.imshow('zoom', zoomed)
        RGB = numpy.asarray(cv2.cvtColor(zoomed, cv2.COLOR_BGR2RGB), dtype=float)
        # lightReflectReduction(im)

        ERR = execute(RGB, transmat_deficit)
        #scaledErr = 0.1 * ERR
        dtpn = (ERR + RGB).clip(min=0,max=255)
        #dtpn = dtpn.clip(max=255)
        # dtpn = ERR + RGB
        result = numpy.asarray(cv2.cvtColor(dtpn.astype('uint8'), cv2.COLOR_RGB2BGR), dtype='uint8')
        # cv2.imshow('image', numpy.concatenate((result,resized.astype('uint8')), axis=1))
        cv2.imshow('before', resized.astype('uint8'))
        cv2.imshow('after', result)
        print(timer() - start)
        cv2.waitKey(1)

def lightReflectReduction(imageToSet):
    rows = imageToSet.shape[0]
    cols = imageToSet.shape[1]

    for i in xrange(rows):
        for j in xrange(cols):
            R = imageToSet.item(i, j, 0)
            G = imageToSet.item(i, j, 1)
            B = imageToSet.item(i, j, 2)
            sumR = 0
            sumG = 0
            sumB = 0
            count = 0
            if ((B >= 220) and (G >= 220) and (R >= 220)):

                if (i > 0):
                    sumR += imageToSet.item(i - 1, j, 0)
                    sumG += imageToSet.item(i - 1, j, 1)
                    sumB += imageToSet.item(i - 1, j, 2)
                    count = count + 1
                    if (j > 0):
                        sumR += imageToSet.item(i - 1, j - 1, 0)
                        sumG += imageToSet.item(i - 1, j - 1, 1)
                        sumB += imageToSet.item(i - 1, j - 1, 2)
                        count = count + 1

                if (j > 0):
                    sumR += imageToSet.item(i, j - 1, 0)
                    sumG += imageToSet.item(i, j - 1, 1)
                    sumB += imageToSet.item(i, j - 1, 2)
                    count = count + 1
                    if (i < rows - 1):
                        sumR += imageToSet.item(i + 1, j - 1, 0)
                        sumG += imageToSet.item(i + 1, j - 1, 1)
                        sumB += imageToSet.item(i + 1, j - 1, 2)
                        count = count + 1

                if (i < rows - 1):
                    sumR += imageToSet.item(i + 1, j, 0)
                    sumG += imageToSet.item(i + 1, j, 1)
                    sumB += imageToSet.item(i + 1, j, 2)
                    count = count + 1
                    if (j < cols - 1):
                        sumR += imageToSet.item(i + 1, j + 1, 0)
                        sumG += imageToSet.item(i + 1, j + 1, 1)
                        sumB += imageToSet.item(i + 1, j + 1, 2)
                        count = count + 1

                if (j < cols - 1):
                    sumR += imageToSet.item(i, j + 1, 0)
                    sumG += imageToSet.item(i, j + 1, 1)
                    sumB += imageToSet.item(i, j + 1, 2)
                    count = count + 1
                    if (i > 0):
                        sumR += imageToSet.item(i, j + 1, 0)
                        sumG += imageToSet.item(i, j + 1, 1)
                        sumB += imageToSet.item(i, j + 1, 2)
                        count = count + 1

                imageToSet.itemset((i, j, 0), sumR / count)
                imageToSet.itemset((i, j, 1), sumG / count)
                imageToSet.itemset((i, j, 2), sumB / count)

def execute(RGB, man_matrix):
    #start = timer()
    # http://stackoverflow.com/questions/25922212/element-wise-matrix-multiplication-in-numpy
    # By multiplying 3 matrices we are moving from rgb to lms space, and then calculate the image
    # as seen by a color blind' and finally get back to rgb space
    _RGB = numpy.einsum('ij,klj->kli', man_matrix, RGB)

    #print('calc', timer() - start)

    # Calculate error between images
    error = (RGB - _RGB)

    # Daltonize: calculating the values for each pixel to be add to
    ERR = numpy.einsum('ij,klj->kli', err2mod, error)

    # Save daltonized image
    # im_converted = Image.fromarray(result, mode='RGB')

    return ERR

# def thread1():
#     global key
#     lock = threading.Lock()
#     while True:
#         with lock:
#             key = input()


# threading.Thread(target = thread1).start()

if __name__ == '__main__':
    import sys

    print "Daltonize image correction for color blind users"

    print "Please wait. Daltonizing in progress..."

    colorblindness = {'d': 'Deuteranope',
                      'p': 'Protanope',
                      't': 'Tritanope',}

    # camera.release()
    video('t')
    cv2.destroyAllWindows()
