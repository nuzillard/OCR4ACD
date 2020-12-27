# isolate pixmaps of numbers, bold font, chemical shift values, screen snapshot from ACD
# run only for the creating of .png images with single digits and decimal point inside.
# has to be run 6 types, changing irow, and titles definition lines, below.

import cv2
import numpy as np

# training image
file_in = r"Images\1.png"

# read black and white image
img = cv2.imread(file_in, 0)

# prepare for single chemical shift value pixmap
file_out = "extract.png"

# row index in chemical shift table, start at 1
# run it with irow equal to 1, 2, 3, 4, 11, 15
irow = 1

# list of digit names for single digit image file naming"
# row 1 contains 162.90 and will create files according to these names

titles = ['1', '6', '2', 'point', '9', '0'] # row 1 - digits 1, 6, 2, ., 9, 0
# titles = ['1', '1', '5', 'point', '5', '0'] # row 2 - new digit 5
# titles = ['1', '2', '7', 'point', '0', '1'] # row 3 - new digit 7
# titles = ['1', '1', '6', 'point', '4', '9'] # row 4 - new digit 4
# titles = ['1', '5', '8', 'point', '7', '0'] # row 11 - new digit 8
# titles = ['1', '3', '2', 'point', '9', '2'] # row 15 - new digit 3

# start column in image for chemical shift value
x1 = 73

# start row in image for chemical shift value indexed by irow
y1 = 55 + 20*(irow-1)

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

# get the vector with the maximum value of each column for the search of spaces between digits
colmax = np.amax(imneg, 0)

# get number of columns for the image of the current cemical shift value
numcol = colmax.size

# print the max of each column to see what is going on
for x, v in enumerate(colmax):
	print(x, v)
 
# search from the left of the sub-image where backgound stops
first = 0
for x, v in enumerate(colmax):
	if v:
		first = x
		break

# search from the right of the sub-image where backgound stops
last = 0
for x, v in enumerate(colmax[::-1]):
	if v:
		last = numcol - x
		break

# get the list of column indexes with minimum pixel intensity, starting with first and ending with last
minis = [first-1]
for x in np.arange(first+1, last-1):
	v = colmax[x]
# a local minimum is supposed to happen for pixel values greater than 128
	if v < 128 and v < colmax[x-1] and v < colmax[x+1]:
# new inter-digit space found
		minis.append(x)
minis.append(last)
print("minima:", minis)

# print intervals for single digit slicing
for imin, mini in enumerate(minis[0:-1]):
	print('[', mini+1, ',', minis[imin+1], '[')

# save files for individual digits as png files named "number_X.png"
for imin, mini in enumerate(minis[0:-1]):
	cur_img = crop_img[:, range((mini+1),(minis[imin+1]))]
	title = "number_" + titles[imin] + ".png"
	cv2.imwrite(title, cur_img)

