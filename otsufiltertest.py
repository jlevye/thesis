#From OpenCV Blog, Otsu's Thresholding

import io
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

os.chdir("Testing")

im1 = cv2.imread("QConspersaTest.tif")
im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)

#Otsu's
ret1, th1 = cv2.threshold(im1, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#After Gaussian filter
blur = cv2.GaussianBlur(im1, (5,5),0)
ret2, th2 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#After opening or erosion or something
kernel=np.ones((10,10),np.uint8)
morpho = cv2.dilate(im1, kernel,iterations=1)

#Plotting
plt.imshow(morpho,"gray")
plt.show()
