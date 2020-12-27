import pytesseract
import sys

filename = sys.argv[1]
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract'
s = pytesseract.image_to_string(filename)
s = s[:-2]
print(s)

