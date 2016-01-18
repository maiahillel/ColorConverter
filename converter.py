

import numpy as np
import argparse
import cv2


redPixel = [0,0,255]
greenPixel = [0,200,0]
whitePixel = [255,255,255]
blackPixel = [0,0,0]

cameraPort = 0
camera = cv2.VideoCapture(cameraPort)

def get_image():
    # read is the easiest way to get a full image out of a VideoCapture object.
    ret, im = camera.read()
    return im



def setColor(imageToSet):
	rows = imageToSet.shape[0]
	cols = imageToSet.shape[1]

	for i in xrange(rows):
		for j in xrange(cols):
			B = imageToSet.item(i,j,0)
			G = imageToSet.item(i,j,1)
			R = imageToSet.item(i,j,2)
			if ((B > 175) and (G > 183) and (R > 183)):
				imageToSet.itemset((i,j,0), whitePixel[0])
				imageToSet.itemset((i,j,1), whitePixel[1])
				imageToSet.itemset((i,j,2), whitePixel[2])
			else:
				if ((G > B) and (G > R)):
					imageToSet.itemset((i,j,0), greenPixel[0])
					imageToSet.itemset((i,j,1), greenPixel[1])
					imageToSet.itemset((i,j,2), greenPixel[2])
				else:
					if (((R - G) < 25) and ((R - B) < 25)):
						imageToSet.itemset((i,j,0), blackPixel[0])
						imageToSet.itemset((i,j,1), blackPixel[1])
						imageToSet.itemset((i,j,2), blackPixel[2])
					else:
						imageToSet.itemset((i,j,0), redPixel[0])
						imageToSet.itemset((i,j,1), redPixel[1])
						imageToSet.itemset((i,j,2), redPixel[2])


def video():
	for i in range(0,50):
		im = get_image()
		setColor(im)
		cv2.imshow('image',im)
		cv2.waitKey(10)


			

 
#image = cv2.imread("/Users/orbarda/Downloads/IMG_4366smaller.jpg")
#cv2.convertTo(image, -1, 2, 0)
#setColor(image)
#im = cv2.imread(get_image())


#lowerRed = np.array([0, 0, 100])
#upperRed = np.array([50, 56, 200 ])
#mask = cv2.inRange(image, lowerRed , upperRed)

#print(mask[10])

#setColor(newim)
#cv2.imwrite("/Users/maiahillel/Downloads/wow.jpg", image)

#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#cv2.imshow('image',image)
#cv2.waitKey(0)
video()
cv2.destroyAllWindows()





#newImage = image.setTo(redPixel, mask)
