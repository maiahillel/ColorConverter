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
import numpy
from PIL import Image
import os.path
#import VideoCapture as VC
import cv2

cameraPort = 0
#camera = cv2.VideoCapture(cameraPort)

def get_image():
    # read is the easiest way to get a full image out of a VideoCapture object.
    ret, im = camera.read()
    return im


def video():    
    for x in range(1,10):
      cv2_image = get_image()
      im = cv2.cvtColor(cv2_image,cv2.COLOR_BGR2RGB)
      #im = Image.fromarray(cv2_image)                 
      image = execute(im ,'p')
      #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
      cv2.imshow('image',image)
      cv2.waitKey(10)
      #im.show()

"""
def capture_image():
  cam = VC.Device() # initialize the webcam
  img = cam.getImage() # in my testing the first getImage stays black.
  img = cam.getImage() # capture the current image
  del cam # no longer need the cam. uninitialize
  return img
"""
def execute(im, color_deficit):


    #helpers_available = True
    #try:
    #    import numpy
    #    from PIL import Image
    #except:
    #    helpers_available = False
    #if not helpers_available:
    #    return

    # Get image data
    #im = Image.open(fpath)
    #fpath = "/Users/orbarda/Downloads/IMG_3424.JPG"
    #cv2.imwrite(fpath, image)
    #im = Image.open(fpath)
    #if im.mode in ['1', 'L']: # Don't process black/white or grayscale images
    #    return
    #im = im.copy() 
    #im = im.convert('RGB')
    RGB = numpy.asarray(im, dtype=float)

    # Transformation matrix for Deuteranope (a form of red/green color deficit)
    lms2lmsd = numpy.array([[1,0,0],[0.494207,0,1.24827],[0,0,1]])
    # Transformation matrix for Protanope (another form of red/green color deficit)
    lms2lmsp = numpy.array([[0,2.02344,-2.52581],[0,1,0],[0,0,1]])
    # Transformation matrix for Tritanope (a blue/yellow deficit - very rare)
    lms2lmst = numpy.array([[1,0,0],[0,1,0],[-0.395913,0.801109,0]])
    # Colorspace transformation matrices
    rgb2lms = numpy.array([[17.8824,43.5161,4.11935],[3.45565,27.1554,3.86714],[0.0299566,0.184309,1.46709]])
    lms2rgb = numpy.linalg.inv(rgb2lms)
    # Daltonize image correction matrix
    err2mod = numpy.array([[0,0,0],[0.7,1,0],[0.7,0,1]])

    # Get the requested image correction
    if color_deficit == 'd':
        lms2lms_deficit = lms2lmsd
    elif color_deficit == 'p':
        lms2lms_deficit = lms2lmsp
    elif color_deficit == 't':
        lms2lms_deficit = lms2lmst
    
    # Transform to LMS space
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

    _RGB = numpy.zeros_like(RGB) 
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            _lms = _LMS[i,j,:3]
            _RGB[i,j,:3] = numpy.dot(lms2rgb, _lms)

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
    error = (RGB -_RGB)

    # Daltonize
    ERR = numpy.zeros_like(RGB) 
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            err = error[i,j,:3]
            ERR[i,j,:3] = numpy.dot(err2mod, err)

    dtpn = ERR + RGB
    
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            dtpn[i,j,0] = max(0, dtpn[i,j,0])
            dtpn[i,j,0] = min(255, dtpn[i,j,0])
            dtpn[i,j,1] = max(0, dtpn[i,j,1])
            dtpn[i,j,1] = min(255, dtpn[i,j,1])
            dtpn[i,j,2] = max(0, dtpn[i,j,2])
            dtpn[i,j,2] = min(255, dtpn[i,j,2])

    result = dtpn.astype('uint8')
    
    # Save daltonized image
    #im_converted = Image.fromarray(result, mode='RGB')
    
    return result


if __name__ == '__main__':
    import sys
    print "Daltonize image correction for color blind users"

    print "Please wait. Daltonizing in progress..."

    colorblindness = { 'd': 'Deuteranope',
                       'p': 'Protanope',
                       't': 'Tritanope',}
    
    #cv2_image = get_image()
    cv2_image = cv2.imread("/Users/orbarda/Downloads/IMG_4366smaller.jpg")
    im = cv2.cvtColor(cv2_image,cv2.COLOR_BGR2RGB)
    #im = Image.fromarray(cv2_image)                 
    image = execute(im ,'d')
    #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    #cv2.imshow('image',image)
    #cv2.waitKey(0)
    cv2.imwrite("/Users/orbarda/Downloads/offir2.jpg", image)

    #camera.release()
    cv2.destroyAllWindows()
