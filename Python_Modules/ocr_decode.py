"""
OCR system strictly reserved to the analysis of screenshots of 13C NMR chemical shift tables
produced by ACD CNMR predictor.
The images of the single digits and of the space character are needed and were recording during the
OCR training step (see training.py). They are 8x6 8 bits grey scale images (11 images).
They are accessed through the glyphrootname variable, see at the ed of the script
"""
import cv2
import numpy as np
from numpy import linalg as LA
import sys
import os

def get_char(target, glyphs):
	"""
	get_char() returns a single digit as a single character or an empty string
	for the blank character, according to a target 8x6 grey scale image and the collection
	of single character glyphs that represent single digits.
	Input images are negated (white is zero, black is 255).
	"""
#	print(target)
#	print(glyphs[1])
	norms = []
# initialize the list of the norms of the differences between the target and the list of glyphs
	for i, glyph in enumerate(glyphs):
# iterate through glyphs and their indexes, start at 0
		diff = glyph - target
# calculate the difference image of the target and of the current glyph
		diff_norm = LA.norm(diff)
# calculate the L2 norm of the difference image
		norms.append(diff_norm)
# update list of norms of difference images
#	print(norms)
	imin = np.argmin(np.array(norms))
# find the index of the glyph that looks at best with the target
	result = '' if imin == 10 else str(imin)
# get result as an empty string for a blank character and the character itself, otherwise
	return result
# return detected character or empty string


def get_chem_shift(imneg, glyphs):
	"""
	get_chem_shift() returns a character string that represents a chemical shift value
	according to imneg, it negated image, and to the negated glyphs or the individual 
	singlet digit images.
	"""
	pp = 29
# column index of the decimal point is expected to be 29 if the represented value is like xxx.xx
	trailer = imneg[:, (pp+12):(pp+14)]
# extracts the last two colums of the image, assuming it is like xxx.xx
	trailer_norm = LA.norm(trailer)
# get norm of this 2 column image
	if trailer_norm < 1.0:
# the two column image is empty, meaning the value might be like xx.xx
		pp = 26
# the index of the decimal point in a value like xx.xx is 26
		trailer = imneg[:, (pp+12):(pp+14)]
# extracts the last two columns of the image, assuming it is like xx.xx
		trailer_norm = LA.norm(trailer)
# get norm of this 2 column image
		if trailer_norm < 1.0:
# the two column image is empty, meaning the value might be like x.xx
			pp = 23
# the index of the decimal point in a value like x.xx is 23
	point_position = pp
# define position of decimal point
#	print('pp', pp)

	tenth = (point_position+2, point_position+8)
# the limit column indexes for the tenths, y in xxx.yx
	hundredth = (point_position+8, point_position+14)
# the limit column indexes for the hundredths, y in xxx.xy
	unit = (point_position-7, point_position-1)
# the limit column indexes for the units, y in xxy.xx
	ten = (point_position-13, point_position-7)
# the limit column indexes for the tens, y in xyx.xx
	hundred = (point_position-19, point_position-13)
# the limit column indexes for the hundreds, y in yxx.xx
	intervals = [hundred, ten, unit, tenth, hundredth]
# build the vector of pairs of limit column indexes for hunfreds, tens, units, tenths, and hundreds

	chemshift = ''
# initialize value of chemical shift string representation
	for ir, r in enumerate(intervals):
# get limits for image slicing
		a, b = r
# get lower (included) and higher (excluded) column indexes for image slicing
		target = imneg[:, a:b]
# get image of a single extracted character
		character = get_char(target, glyphs)
# get character from image
		chemshift += character
# append current charater to chemical shift representation as string
#		print(chemshift)
#	chemshift = chemshift[:-2] + '.' + chemshift[-2] + chemshift[-1]
	chemshift = chemshift[:-2] + '.' + chemshift[-2:]
# insert decimal point into chemical shift string representation. Always at the same place, hopefully
	return chemshift
# return string representation of the current chemical shift value

def get_glyphs(glyphrootname):
	"""
	get_glyphs() build the list of the negated images of the individual image representation of
	the digit characters and of the blank character
	"""
	titles = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'blank']
# digit glyphs naming
	glyphs = []
# initialize array of digit glyphs, in negative b/w mode
	for title in titles:
# loop through glyph names
		filename = glyphrootname + title + ".png"
# build path to current glyph file
		glyph = 255 - cv2.imread(filename, 0)
# read and negate current glyph
		glyphs.append(glyph)
# update list of glyphs
	return glyphs
# return list of glyphs, 11 8x6 8 bit b/w images

def get_all_shifts(filename, glyphs):
	"""
	get_all_shifts() extracts a list of cemical shift values as strings 
	according to filename, the path to the image of the chemical shift table to analyze,
	and to glyphs, a list of single character images of the decimal digits and of the blank character.
	"""
	all_shifts = []
# initialize list of chemical shifts
#	print('File:',filename)
	img = cv2.imread(filename, 0)
# read black and white image of chemical shift table
	x1 = 73
	x2 = 131
	y0 = 56
	dy = 8
	yspacing = 20
# image sizing constants
	height, width = img.shape
	nrow = (height - y0)//yspacing + 1
# get image size and number of rows, assuming that the lower limit of the image was properly placed (not too low).
	for irow in range(1, nrow+1):
# loop over rows in chemical shift table
		y1 = y0 + yspacing * (irow-1)
# start row in image for chemical shift value indexed by irow
		y2 = y0 + dy + yspacing * (irow-1)
# stop row in image for chemical shift value indexed by irow
		if y2 >= height:
# check_again for possibly bad (too high) number of rows
			break
# all rows already explored, leave loop
		crop_img = img[y1:y2, x1:x2].copy()
# get sub-image for chemical shift at row irow
		cv2.imwrite('bw.png', crop_img)
# for the checking of the last cut image of chemical shift value. for debugging. 
		imneg = 255 - crop_img
# negate image, so that background is 0 and most intense pixel is 255
		chemshift = get_chem_shift(imneg, glyphs)
		all_shifts.append(chemshift)
# get chemical shift at row irow and append to the list of chemical shifts
	return all_shifts
# return the list of chemical shift representations as strings in chemical shift table image

def run(filename):
	head, tail = os.path.split(__file__)
# The single digit glyphs are contained in the BoldFace directory, located in the same directory
# as this python module file
	glyphrootname = os.path.join(head, "Boldface", "number_")
# beginning of the path to single decimal digit images
	glyphs = get_glyphs(glyphrootname)
# get list of single decimal digit glyphs
	all_shifts = get_all_shifts(filename, glyphs)
# get list of chemical shifts from the image to be analyzed
	return all_shifts
# return  list of chemical shifts from the image to be analyzed
	
if __name__ == '__main__':
	if len(sys.argv) == 1:
# no argumnt in command
		filename = os.path.join("Images", "1.png")
# default path to an image of a chemical shift table
	else:
# at least a command line argument
		filename = sys.argv[1]
# the first command line argument is taken as the path to the image of the chemical shift table to be analyzed
	all_shifts = run(filename)
# get list of chemical shifts from the image to be analyzed
	print(filename)
# print path to the image to be analyzed
	for a_shift in all_shifts:
# loop over chemical shifts string representations
		print(a_shift)
# print current chemical shift as a string
