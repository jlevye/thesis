import io
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

os.chdir("Testing")

im1 = cv2.imread("QConspersaTest.tif")
im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)

# Try eroding (dilating?) first to smooth out the colors
kernel = np.ones((10,10),np.uint8)
out1 = cv2.erode(im1, kernel, iterations=1)
out1 = cv2.dilate(out1, kernel, iterations=1)
#ret,outBad  = cv2.threshold(im1, 127, 255, cv2.THRESH_BINARY)
out2 = cv2.adaptiveThreshold(out1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 67, 0)
out3 = cv2.erode(out2, kernel, iterations=1)
out3 = cv2.dilate(out3, kernel, iterations=1)
# out2 = cv2.adaptiveThreshold(im1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 67, 0)

# plt.subplot(2,2,1),plt.imshow(im1, "gray")
# plt.title("input")
# plt.subplot(2,2,2), plt.imshow(outBad, "gray")
# plt.title("global threshold")
# plt.subplot(2,2,3), plt.imshow(out1, "gray")
# plt.title("mean threshold")
# plt.subplot(2,2,4), plt.imshow(out2,"gray")
# plt.title("gaussian treshold")

plt.subplot(2,2,1),plt.imshow(im1,"gray")
plt.title("original")
plt.subplot(2,2,2),plt.imshow(out2,"gray")
plt.title("opened")
plt.subplot(2,2,3)
plt.title("threshold")
plt.subplot(2,2,4),plt.imshow(out3,"gray")
plt.title("second opening")
plt.show()
