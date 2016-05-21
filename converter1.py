# Old Color Converter

import numpy as np
import argparse
import cv2


redPixel = [0,0,255]
greenPixel = [0,250,0]
whitePixel = [255,255,255]
blackPixel = [0,0,0]

lower_white = np.array([180, 195, 195], dtype = "uint8")
upper_white = np.array([255, 255, 255], dtype = "uint8")

lower_green = np.array([0, 140, 0])
upper_green = np.array([180, 220, 175])

lower_red = np.array([0, 0, 135])
upper_red = np.array([255, 255, 255])

cameraPort = 0
camera = cv2.VideoCapture(cameraPort)

def get_image():
    # read is the easiest way to get a full image out of a VideoCapture object.
    ret, im = camera.read()
    return im

def splitNmerge(mask, image):
	splitted = cv2.split(image)
	blue = splitted[0]
	green = splitted[1]
	red = splitted[2]

	blue = cv2.bitwise_or(blue, mask)
	green = cv2.bitwise_or(green, mask)
	red = cv2.bitwise_or(red, mask)

	return cv2.merge([blue,green,red])



def setColor(imageToSet):
	rows = imageToSet.shape[0]
	cols = imageToSet.shape[1]

	for i in xrange(rows):
		for j in xrange(cols):
			B = imageToSet.item(i,j,0)
			G = imageToSet.item(i,j,1)
			R = imageToSet.item(i,j,2)
			if ((B < 180) and (G < 195) and (R < 195)):
				#imageToSet.itemset((i,j,0), whitePixel[0])
				#imageToSet.itemset((i,j,1), whitePixel[1])
				#imageToSet.itemset((i,j,2), whitePixel[2])
			
				if ((G > B) and (G > R) and ( (R - G) >= 15 or (R - G) <= -15) and ((R - B) >= 15 or (R - B) <= -15)):
						imageToSet.itemset((i,j,0), greenPixel[0])
						imageToSet.itemset((i,j,1), greenPixel[1])
						imageToSet.itemset((i,j,2), greenPixel[2])
				else:
					if (((R - G) < 18) and ((R - B) < 18)):
						imageToSet.itemset((i,j,0), blackPixel[0])
						imageToSet.itemset((i,j,1), blackPixel[1])
						imageToSet.itemset((i,j,2), blackPixel[2])
					else:
						imageToSet.itemset((i,j,0), redPixel[0])
						imageToSet.itemset((i,j,1), redPixel[1])
						imageToSet.itemset((i,j,2), redPixel[2])


def video():
	for i in range(0,20):
		image = get_image()
		mask = cv2.inRange(image, lower_white, upper_white)
		nImage = splitNmerge(mask, image)
		setColor(nImage)
		#setColor(im)
		cv2.imshow('image',nImage)
		cv2.waitKey(10)


			

 
#image = cv2.imread("/Users/orbarda/Downloads/IMG_4366smaller.jpg")

#mask = cv2.inRange(image, lower_white, upper_white)
#nImage = splitNmerge(mask, image)
#setColor(nImage)
#mask = cv2.inRange(image, lower_green, upper_green)
#mask = cv2.inRange(nImage, lower_green, upper_green)
#mask = cv2.bitwise_not(mask)
#nImage = splitNmerge(mask, image)
#mask = cv2.inRange(image, lower_black, upper_black)
#nImage = splitNmerge(mask, nImage);
#mask = cv2.inRange(image, lower_red, upper_red)
#nImage = splitNmerge(mask, nImage);
#mask = cv2.inRange(image, lowerRed , upperRed)
#cv2.imwrite("/Users/maiahillel/Downloads/wow.jpg", image)

#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#cv2.imshow('image',mask)
#cv2.waitKey(0)
video()
cv2.destroyAllWindows()





#newImage = image.setTo(redPixel, mask)
