import trueACD
import os

if __name__ == '__main__':
	curdir = "MyQuercetin"
	inputfilename = os.path.join(curdir, "demo.sdf")
# path of the .sdf file to be supplemented with ACD-predicted chemical shifts
	outputfilename = os.path.join(curdir, "true_acd_demo.sdf")
# path of the .sdf file that is supplemented with ACD-predicted chemical shifts
	images = curdir
# path to the directory that contains the images of chemical shift tables, one per compound
	trueACD.run(inputfilename, outputfilename, images)
# supplement .sdf input file to give .sdf output file according to images of chemical shift tables
