import cv2
import numpy as np
from numpy import linalg as LA

def get_char(target, target_width, glyphs, glyphs_widths, glyphs_norms):
#	print(target_width)
	if target_width == 1:
		return '.'
	if target_width not in [5, 6]:
		return 'X'
	target_norm = LA.norm(target)
	cosines = []
	for i, glyph in enumerate(glyphs):
		glyph_width = glyphs_widths[i]
		if target_width != glyph_width:
			cosines.append(0.0)
		else:
			glyph_norm = glyphs_norms[i]
			cosine = np.sum(np.sum(np.multiply(glyph, target)))/(glyph_norm * target_norm)
			cosines.append(cosine)
#	print(cosines)
	imax = np.argmax(np.array(cosines))
	return str(imax)
# end of function get_char
	
	

def get_chem_shift(imneg, glyphs, glyphs_widths, glyphs_norms):
	
# get the vector with the maximum value of each column for the search of spaces between digits
	colmax = np.amax(imneg, 0)

# get number of columns for the image of the current chemical shift value
	numcol = colmax.size

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
#	print("minima:", minis)
	
# print intervals for single digit slicing
	chemshift = ''
	for imin, mini in enumerate(minis[0:-1]):
#		print('[', mini+1, ',', minis[imin+1], '[')
		target = imneg[:, range((mini+1),(minis[imin+1]))]
#		target_name = 'target_' + str(imin) + '.png'
#		cv2.imwrite(target_name, 255-np.array(target, 'uint8'))
		character = get_char(target, (minis[imin+1])-(mini+1), glyphs, glyphs_widths, glyphs_norms)
#		print('***', character)
		chemshift += character
#		print(target)
#		print(glyphs[1])
#		print(LA.norm(target))
#		print(LA.norm(target) * LA.norm(target))
#		print(glyphs_norms[1])
#		print(np.multiply(target, target))
#		print(np.sum(np.sum(np.multiply(glyphs[1], target)))/(glyphs_norms[1] * LA.norm(target)))
#		break
#	print(chemshift)
	return chemshift
		
# end of function get_chem_shift()

# digit glyphs naming
titles = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# get array of digit glyphs, in negative b/w mode
glyphs = []
glyphs_widths = []
for title in titles:
	filename = "number_" + title + ".png"
	glyph = 255 - cv2.imread(filename, 0)
	glyph = np.array(glyph, 'uint16')
	glyphs.append(glyph)
	glyphs_widths.append(glyph.shape[1])
# print(glyphs_widths)

glyphs_norms = []
for glyph in glyphs:
	norme = LA.norm(glyph)
	glyphs_norms.append(norme)

# decoded image
file_in = r"Images\2.png"

# read black and white image
img = cv2.imread(file_in, 0)

# prepare for single chemical shift value pixmap
# file_out = "extract.png"

# start column in image for chemical shift value
x1 = 73

# stop column in image for chemical shift value
x2 = 131

# row index in chemical shift table, start at 1

for irow in range(1, 17):


# start row in image for chemical shift value indexed by irow
	y1 = 55 + 20*(irow-1)

# stop row in image for chemical shift value indexed by irow
	y2 = 64 + 20*(irow-1)

# get sub-image for chemical shift at row irow
	crop_img = img[y1:y2, x1:x2].copy()

# write sub-image on disk, just for checking 
# cv2.imwrite(file_out, crop_img)

# negate image, so that background is 0 and most intense pixel is 255
	imneg = 255 - crop_img

# 
	imneg = np.array(imneg, 'uint16')
	chemshift = get_chem_shift(imneg, glyphs, glyphs_widths, glyphs_norms)
	print(chemshift)
