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
import numpy
import os.path
import cv2
from numba import vectorize
from timeit import default_timer as timer


cameraPort = 0
camera = cv2.VideoCapture(cameraPort)
# Transformation matrix for Deuteranope (a form of red/green color deficit)
lms2lmsd = numpy.array([[1,0,0],[0.494207,0,1.24827],[0,0,1]])
# Transformation matrix for Protanope (another form of red/green color deficit)
lms2lmsp = numpy.array([[0,2.02344,-2.52581],[0,1,0],[0,0,1]])
# Transformation matrix for Tritanope (a blue/yellow deficit - very rare)
lms2lmst = numpy.array([[1,0,0],[0,1,0],[-0.395913,0.801109,0]])
# Colorspace transformation matrices
rgb2lms = numpy.array([[17.8824,43.5161,4.11935],[3.45565,27.1554,3.86714],[0.0299566,0.184309,1.46709]])

lms2rgb = numpy.linalg.inv(rgb2lms)

lmsd2rgb = numpy.dot(lms2rgb, numpy.dot(lms2lmsd, rgb2lms))

lmsp2rgb = numpy.dot(lms2rgb, numpy.dot(lms2lmsp, rgb2lms))

lmst2rgb = numpy.dot(lms2rgb, numpy.dot(lms2lmst, rgb2lms))

# Daltonize image correction matrix
err2mod = numpy.array([[0,0,0],[0.7,1,0],[0.7,0,1]])

def get_image():
   # read is the easiest way to get a full image out of a VideoCapture object.
    ret, im = camera.read()
    return im


def video(color_deficit):
    
    # Get the requested image correction
    if color_deficit == 'd':
        transMat_deficit = lmsd2rgb
    elif color_deficit == 'p':
        transMat_deficit = lmsp2rgb
    elif color_deficit == 't':
        transMat_deficit = lmst2rgb

    for x in range(1,6):
      
      start = timer()
      cv2_image = get_image()
      resized = cv2.resize(cv2_image, (800, 600))
      RGB = numpy.asarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB), dtype=float)
      #lightReflectReduction(im)       
      ERR = execute(RGB ,transMat_deficit)

      scaledErr = 0.1 * ERR

      dtpn = (scaledErr * 5) + RGB
      result = dtpn.astype('uint8')
      cv2.imshow('image',result)
      print(timer() - start)
      cv2.waitKey(1)


def lightReflectReduction(imageToSet):
    rows = imageToSet.shape[0]
    cols = imageToSet.shape[1]
    
    for i in xrange(rows):
      for j in xrange(cols):
        R = imageToSet.item(i,j,0)
        G = imageToSet.item(i,j,1)
        B = imageToSet.item(i,j,2)
        sumR = 0
        sumG = 0
        sumB = 0
        count = 0
        if ((B >= 220) and (G >= 220) and (R >= 220)):
          
          if(i > 0):
            sumR += imageToSet.item(i - 1,j,0)
            sumG += imageToSet.item(i - 1,j,1)
            sumB += imageToSet.item(i - 1,j,2)
            count = count + 1
            if(j > 0):
              sumR += imageToSet.item(i - 1,j - 1,0)
              sumG += imageToSet.item(i - 1,j - 1,1)
              sumB += imageToSet.item(i - 1,j - 1,2)
              count = count + 1
          
          if(j > 0):
            sumR += imageToSet.item(i,j - 1,0)
            sumG += imageToSet.item(i,j - 1,1)
            sumB += imageToSet.item(i,j - 1,2)
            count = count + 1
            if(i < rows - 1):
              sumR += imageToSet.item(i + 1,j - 1,0)
              sumG += imageToSet.item(i + 1,j - 1,1)
              sumB += imageToSet.item(i + 1,j - 1,2)
              count = count + 1
          
          if(i < rows - 1):
            sumR += imageToSet.item(i + 1,j,0)
            sumG += imageToSet.item(i + 1,j,1)
            sumB += imageToSet.item(i + 1,j,2)
            count = count + 1
            if(j < cols - 1):
              sumR += imageToSet.item(i + 1,j + 1,0)
              sumG += imageToSet.item(i + 1,j + 1,1)
              sumB += imageToSet.item(i + 1,j + 1,2)
              count = count + 1

          if(j < cols - 1):
            sumR += imageToSet.item(i,j + 1,0)
            sumG += imageToSet.item(i,j + 1,1)
            sumB += imageToSet.item(i,j + 1,2)
            count = count + 1
            if(i > 0):
              sumR += imageToSet.item(i,j + 1,0)
              sumG += imageToSet.item(i,j + 1,1)
              sumB += imageToSet.item(i,j + 1,2)
              count = count + 1

          imageToSet.itemset((i,j,0), sumR / count)
          imageToSet.itemset((i,j,1), sumG / count)
          imageToSet.itemset((i,j,2), sumB / count) 

def execute(RGB, lms2lms_deficit):

   # Transform to LMS space
    """
    LMS = numpy.zeros_like(RGB)               
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            rgb = RGB[i,j,:3]
            LMS[i,j,:3] = numpy.dot(rgb2lms, rgb)

    # Calculate image as seen by the color blind
    _LMS = numpy.zeros_like(RGB)  
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            lms = LMS[i,j,:3]
            _LMS[i,j,:3] = numpy.dot(lms2lms_deficit, lms)


      """
    
    _RGB = numpy.zeros_like(RGB) 
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            rgb = RGB[i,j,:3]
            _RGB[i,j,:3] = numpy.dot(lms2lms_deficit, rgb)
    #print(timer() - start)

##    # Save simulation how image is perceived by a color blind
##    for i in range(RGB.shape[0]):
##        for j in range(RGB.shape[1]):
##            _RGB[i,j,0] = max(0, _RGB[i,j,0])
##            _RGB[i,j,0] = min(255, _RGB[i,j,0])
##            _RGB[i,j,1] = max(0, _RGB[i,j,1])
##            _RGB[i,j,1] = min(255, _RGB[i,j,1])
##            _RGB[i,j,2] = max(0, _RGB[i,j,2])
##            _RGB[i,j,2] = min(255, _RGB[i,j,2])
##    simulation = _RGB.astype('uint8')
##    im_simulation = Image.fromarray(simulation, mode='RGB')
##    simulation_filename = "%s-%s-%s" % ('daltonize-simulation', color_deficit, filename)
##    simulation_fpath = os.path.join(head, simulation_filename)
##    im_simulation.save(simulation_fpath)

    # Calculate error between images
    error = (RGB - _RGB)

    # Daltonize
    ERR = numpy.zeros_like(RGB) 
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            err = error[i,j,:3]
            #err = [error.item(i,j,0), error.item(i,j,1), error.item(i,j,2)]
            ERR[i,j,:3] = numpy.dot(err2mod, err)

    
    """
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            dtpn[i,j,0] = max(0, dtpn[i,j,0])
            dtpn[i,j,0] = min(255, dtpn[i,j,0])
            dtpn[i,j,1] = max(0, dtpn[i,j,1])
            dtpn[i,j,1] = min(255, dtpn[i,j,1])
            dtpn[i,j,2] = max(0, dtpn[i,j,2])
            dtpn[i,j,2] = min(255, dtpn[i,j,2])
      
    """
    
    # Save daltonized image
    #im_converted = Image.fromarray(result, mode='RGB')
    
    return ERR


if __name__ == '__main__':
    import sys
    print "Daltonize image correction for color blind users"

    print "Please wait. Daltonizing in progress..."

    colorblindness = { 'd': 'Deuteranope',
                       'p': 'Protanope',
                       't': 'Tritanope',}
    

    #camera.release()
    video('p')
    cv2.destroyAllWindows()

