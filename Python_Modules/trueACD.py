"""
The User has to change the inputfilename, outputfilename and Images paths at the end of the script.
Input and output files are .sdf files.
The output file is produced from the input file by supplementation with chemical shifts values,
formatted for ACD database creation, obtained by snapshots of chemical shift tables
produced by the ACD CNMR predictor.
Chemical shift value recognition from images relies on a collection of single digit (and of space character)
images that are located to the place indicated by the glyphrootname variable (see end of script).
"""
from rdkit import Chem
import ocr_decode
import os

def acd_string_format(s):
	"""
	formats strings that are more than 200 characters long to fit with the way
	ACD formats long strings in sdf values
	"""
	limit = 200
# maximum length of a line
	lens = len(s)
# get length of string sent by the caller
	if lens <= limit:
# is it a small string?
		return s
# nothing to do for strings with less then 200 characters (included)
	lensm1 = lens-1
# lensm1 is lens minus one
	ranges = [(x*limit, (x+1)*limit) for x in range(lensm1 // limit)]
# calulates ranges at pairs of character indexes for string slicing
	ranges.append( (ranges[-1][1], lens) )
# update ranges with the indexes of the last (most probably incomplete) slice
	return '\n'.join(s[r[0]:r[1]] for r in ranges)
# get the list of slices, joins with newlines and return the result to the caller

def proc_one(mol, chemshifts):
	"""
	proc_one() supplements molecule mol with chemical shift data from list chemshifts
	"""
	if not mol.HasProp('NMRSHIFTDB2_ASSIGNMENT'):
# there is no previous nmrshiftdb assignment from which the indexes of C atoms may be drawn
		old_pairs = [ [str(a.GetIdx()+1), ''] for a in mol.GetAtoms() if a.GetAtomicNum() == 6 ]
# build a list of pairs made of a C atom index and a placeholder (empty) string as chemical shift
	else:
# there is a previous nmrshiftdb assignment from which the indexes of C atoms may be drawn
		text = mol.GetProp('NMRSHIFTDB2_ASSIGNMENT')[:-2]
# get NMRSHIFTDB2_ASSIGNMENT string with the trailing ' \' removed
		lines = text.split(' \\\n')
# get the list of lines of NMRSHIFTDB2_ASSIGNMENT value
		old_pairs = [line.split(', ') for line in lines]
# get the list of pairs made of C atom index and of its nmrshiftdb2-predicted chemical shift
	if len(old_pairs) != len(chemshifts):
# the number of known C atoms and the number of their new chemical shifts are different
		print('Bad length', len(old_pairs), 'carbons', len(chemshifts), 'shifts')
# something went wrong somewhere
		return
# return molecule unchanged
	new_pairs = [ [old_pair[0], newcs]for (old_pair, newcs) in zip(old_pairs, chemshifts)]
# build the new list of pairs made of a C atom index and of its chemical shift from the decoding of the
# ACD-generated image of chemical shifts table
	new_lines = [', '.join(pair) for pair in new_pairs]
	new_text = ' \\\n'.join(new_lines) + ' \\'
# build value for the new TRUE_ACD_ASSIGNMENT tag, with the same format as for NMRSHIFTDB2_ASSIGNMENT
	mol.SetProp('TRUE_ACD_ASSIGNMENT', new_text)
# set mol property named TRUE_ACD_ASSIGNMENT with its freshly determined value. Just for the eyes.
	acd_line = acd_string_format(';'.join([str(i)+':'+pair[0]+'|'+pair[1] for (i, pair) in enumerate(new_pairs)]))
# format ACD chemical shift assignment for reading by the ACD database import mechanism.
	mol.SetProp('CNMR_SHIFTS', acd_line)
# modify mol for reading of ACD-predicted chemical shifts by the ACD database import mechanism. Looks stupid, isn't it?

def run(inputfilename, outputfilename, images):
	"""
	proc_all() supplements .sdf input file to give .sdf output file
	with chemical shifts formatted for ACD database import, according to
	images of chemical shift tables.
	"""
	supplier = Chem.SDMolSupplier(inputfilename)
# get handle to input .sdf file
	writer = Chem.SDWriter(outputfilename)
# get handle to output .sdf file
	for imol, mol in enumerate(supplier, start=1):
# iterate through molecules in input files, indexed by imol, start at 1
		print(imol)
# print index of currently processed molecule
		imgpath = os.path.join(images, str(imol) + ".png")
# build path to the image associated with the current molecule
		if os.path.exists(imgpath):
# the image of the chemical shift table exists for the current molecule
			chemshifts = ocr_decode.run(imgpath)
# get list of chemical shifts from the image using the ocr_decode module
			proc_one(mol, chemshifts)
# insert chemical shifts from table image into the current molecule
		writer.write(mol)
# write the current molecule to output file
	writer.flush()
# complete writing of the output file


if __name__ == '__main__':
	curdir = "Quercetin"
	inputfilename = os.path.join(curdir, "demo.sdf")
# path of the .sdf file to be supplemented with ACD-predicted chemical shifts
	outputfilename = os.path.join(curdir, "true_acd_demo.sdf")
# path of the .sdf file that is supplemented with ACD-predicted chemical shifts
	images = curdir
# path to the directory that contains the images of chemical shift tables, one per compound
	run(inputfilename, outputfilename, images)
# supplement .sdf input file to give .sdf output file according to images of chemical shift tables
