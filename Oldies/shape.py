# print image size and number of rows

import cv2
import numpy as np

# training image
file_in = r"Images\4.png"

# read black and white image
img = cv2.imread(file_in, 0)

height, width = img.shape

print("height", height)
print("width", width)


y0 = 55
spacing = 20

nrow = (height - y0)//spacing + 1

print("rows", nrow)

file_out = "full_bw.png"
cv2.imwrite(file_out, img)
