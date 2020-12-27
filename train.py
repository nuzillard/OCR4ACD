# isolate pixmaps of numbers, bold font, chemical shift values, screen snapshot from ACD
# run only for the creating of .png images with single digits and decimal point inside.
# has to be run 7 times, changing irow, and titles definition lines, below.

import cv2
import numpy as np

# training image
file_in = r"Images\1.png"

# read black and white image
img = cv2.imread(file_in, 0)

# prepare for single chemical shift value pixmap
file_out = "extract.png"

# row index in chemical shift table, start at 1
# run it with irow equal to 1, 2, 3, 4, 11, 15, 16
irow = 1

# list of digit names for single digit image file naming"
# row 1 contains 162.90 and will create files according to these names

titles = ['1', '6', '2', '9', '0'] # row 1 - digits 1, 6, 2, ., 9, 0
# titles = ['1', '1', '5', '5', '0'] # row 2 - new digit 5
# titles = ['1', '2', '7', '0', '1'] # row 3 - new digit 7
# titles = ['1', '1', '6', '4', '9'] # row 4 - new digit 4
# titles = ['1', '5', '8', '7', '0'] # row 11 - new digit 8
# titles = ['1', '3', '2', '9', '2'] # row 15 - new digit 3
# titles = ['blank', '5', '5', '4', '0'] # row 16 - new digit blank

# start column in image for chemical shift value
x1 = 73

# start row in image for chemical shift value indexed by irow
y1 = 56 + 20*(irow-1)

# stop column in image for chemical shift value
x2 = 131

# stop row in image for chemical shift value indexed by irow
y2 = 64 + 20*(irow-1)

# get sub-image for chemical shift at row irow
crop_img = img[y1:y2, x1:x2].copy()

# write sub-image on disk, just for checking 
cv2.imwrite(file_out, crop_img)

# negate image, so that background is 0 and most intense pixel is 255
imneg = 255 - crop_img

pp = 29
trailer = imneg[:, (pp+11):(pp+14)]
trailer_norm = LA.norm(trailer)
if trailer_norm < 1.0:
	pp = 26
	trailer = imneg[:, (pp+11):(pp+14)]
	trailer_norm = LA.norm(trailer)
	if trailer_norm < 1.0:
		pp = 23
point_position = pp

tenth = (point_position+2, point_position+8)
hundredth = (point_position+8, point_position+14)
unit = (point_position-7, point_position-1)
ten = (point_position-13, point_position-7)
hundred = (point_position-19, point_position-13)
intervals = [hundred, ten, unit, tenth, hundredth]
print(intervals)

for ir, r in enumerate(intervals):
	a, b = r
	cur_img = crop_img[:, a:b]
	title = "number_" + titles[ir] + ".png"
	cv2.imwrite(title, cur_img)
