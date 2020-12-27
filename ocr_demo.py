"""
PLEASE DO NOT EDIT
"""
import sys
import ocr_decode
	
if __name__ == '__main__':
	if len(sys.argv) == 1:
		filename = r"Images\1.png"
	else:
		filename = sys.argv[1]
	all_shifts = ocr_decode.run(filename)
	print(filename)
	for a_shift in all_shifts:
		print(a_shift)
