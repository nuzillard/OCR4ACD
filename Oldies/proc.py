import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract'
file_in = "1.png"
img = cv2.imread(file_in, -1)
file_out = "extract.png"
x11 = 3
x21 = 41
x12 = 73
x22 = 131
y1 = 52
y2 = 70
crop_img = img[y1:y2, x11:x21].copy()
# crop_img = img[y1:y2, x12:x22].copy()
cv2.imwrite(file_out, crop_img)
s = pytesseract.image_to_string(file_out)
# s = s[:-1]
print(s)
