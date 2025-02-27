import cv2
import pytesseract
from pytesseract import Output
img = cv2.imread('img/example1.jpg')
custom_config = r'-l tha --oem 1 --psm 6'

data = pytesseract.image_to_data(img,config=custom_config, output_type=Output.DICT)
keys = list(data.keys())
totalBox = len(data['text'])
for i in range(totalBox):
    (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)

print(''.join(data['text']))